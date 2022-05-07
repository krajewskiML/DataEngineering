import requests
import json
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area[name = "San Francisco"];
(way(area)["highway"~"^(motorway|trunk|primary)$"];>;);
out;
"""
response = requests.get(overpass_url, 
                        params={'data': overpass_query})
data = response.json()
with open("first_overpass.json", 'w') as fout:
    json.dump(data, fout)
a = 9