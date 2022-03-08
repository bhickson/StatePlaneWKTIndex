import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import geopandas as gpd

esri_StatePlaneZone_service = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_State_Plane_Zones_NAD83/FeatureServer/0/query?f=geojson&where=1=1&outFields=*"
geojson = json.loads(requests.get(esri_StatePlaneZone_service).content)

zones = gpd.GeoDataFrame.from_features(geojson["features"], crs="EPSG:4326")

def getWKT(zone_num):
    if len(zone_num) < 4:
        zone_num = "0" + str(zone_num)
    resp = requests.get(f"https://epsg.io/?q={zone_num}")
    html_parse = BeautifulSoup(resp.content)
    ul_results = html_parse.find(class_="results")\

    all_li = [li for li in ul_results.find_all(name="li") if type(li) == bs4.element.Tag]
    found = False
    
    wkts = {}
    codes = {}
    for li in all_li:
        a = li.find(name="a")
        code = a["href"].replace("/","")
        if code not in codes and str(code).startswith("10"):
            codes[code] = a
            
    if len(codes)>2:
        raise ValueError("Unexpected number of results")

    for code, a in codes.items():
        wkt = requests.get("https://epsg.io/"+ code + ".wkt").content
        if "feet" in a.text.strip().lower():
            wkts["Feet"] = wkt.decode("UTF-8")
        else:
            wkts["Meters"] = wkt.decode("UTF-8")

    if "Meters" not in wkts.keys() and len(wkts.keys()) == 1:
        wkts["Meters"] = None
    
    return pd.Series([wkts["Feet"], wkts["Meters"]])

zones[["StatePlaneFeet", "StatePlaneMeters"]] = zones.FIPSZONE.apply(lambda z: getWKT(z))

# write to GeoJson
with open("C:/Users/BenjaminH/Downloads/StatePlaneZoneNAD83_WKTIndex.geojson", "w") as dst:
    dst.write(zones.to_json(indent=4))
# write to GeoPackage
zones.to_file("./StatePlaneZoneNAD83_WKTIndex.gpkg", driver="GPKG")