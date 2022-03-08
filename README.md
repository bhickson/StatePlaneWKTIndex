# State Plane WKT Index
Uses a Esri-hosted StatePlane Zone (NAD83) polygon file to search epsg.io for matches to the zone number and pulls the wkt projection information. Useful for cases where you want to match a local dataset to the best local state plane projection for reprojection.

Uses the service here for the zone polygons 
https://hub.arcgis.com/datasets/esri::usa-state-plane-zones-nad83/about

and searches against https://epsg.io for the zone numbers
