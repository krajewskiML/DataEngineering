import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area[name = "San Francisco"];
(way(area);>;);
out;
"""
response = requests.get(overpass_url, params={"data": overpass_query})
data = response.json()
with open("all_streets_overpass.json", "w") as fout:
    json.dump(data, fout)
# load downloaded data
# with open("all_streets_overpass.json", "r") as fin:
#     data = json.load(fin)
# transform response to geojson format
nodes = [element for element in data["elements"] if element["type"] == "node"]
valid_street_types = [
    "motorway",
    "trunk",
    "primary",
]  # TODO: fiszu i tygrysi ustalcie pls jakie drogi bierzemy
streets = [
    element
    for element in data["elements"]
    if element["type"] == "way" and "tags" in element and "highway" in element["tags"]
    # and element["tags"]["highway"] in valid_street_types #TODO: jak będą dobrane typy dróg to odkomentujcie
]

nodes_stripped = {
    node["id"]: [node["lon"], node["lat"]]
    for node in nodes
    if -123 < node["lon"] < -122
    and 37 < node["lat"] < 38  # could also use max\min lat and lon of trees
}
geojson_dict = {
    "type": "FeatureCollection",
    "name": "roads",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [nodes_stripped[idx] for idx in street["nodes"]],
            },
        }
        for street in streets
        if all(node in nodes_stripped for node in street["nodes"])
    ],
}

with open("all_streets_overpass.geojson", "w") as fout:
    json.dump(geojson_dict, fout)
