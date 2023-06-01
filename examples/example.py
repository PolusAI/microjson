from microjson import MicroJSON, GeoJSON
import json

# load the microjson file
with open('examples/json/sample_microjson.json') as f:
    data = json.load(f)

# validate the microjson file
microjsonobj = MicroJSON.parse_obj(data)
print("done validating: {}".format(microjsonobj))

# load the geojson file
with open('examples/json/sample_geometrycollection.json') as f:
    data = json.load(f)

# validate the geojson file
geojsonobj = GeoJSON.parse_obj(data)

print("done validating: {}".format(geojsonobj))

# load the microjson file
with open('examples/json/sample_geojson.json') as f:
    data = json.load(f)

# validate the microjson file
geojsonobj = GeoJSON.parse_obj(data)
print("done validating: {}".format(geojsonobj))
