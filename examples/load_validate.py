import microjson.model as mj
import json

# load the microjson file
with open('tests/json/microjson/valid/fullexample.json') as f:
    data = json.load(f, strict=True)

# validate the microjson file
microjsonobj = mj.MicroJSON.parse_obj(data)
print("done validating: {}".format(microjsonobj))

# load the geojson file
with open('tests/json/geojson/valid/featurecollection/basic.json') as f:
    data = json.load(f, strict=True)

# validate the geojson file
geojsonobj = mj.GeoJSON.parse_obj(data)

print("done validating: {}".format(geojsonobj))
