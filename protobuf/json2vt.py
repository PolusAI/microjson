from geojson2vt.geojson2vt import geojson2vt
from geojson2vt import utils as g2vt_utils
from vt2pbf import vt2pbf
import json
# get json file from tests/json/microjson/valid/fullexample.json
json_file = "protobuf/18_1283_W_OD_82_encoding_1_14_3.json"
#json_file = "tests/json/geojson/valid/feature/with-number-id.json"
#json_file = "tests/json/microjson/valid/metadata-full.json"

data = g2vt_utils.get_json(json_file)
# convert to vt
options: dict = {
    "generateId": False
} 
tile_index = geojson2vt(data, options)
x, y, z = 0, 0, 0
vt = tile_index.get_tile(z, x, y)
print(vt)
# save to a file
with open("protobuf/vt{}-{}-{}.json".format(z, x, y), "w") as f:
    json.dump(tile_index.tiles, f)
# convert into a binary protocol buffer
pbf = vt2pbf(vector_tile=vt)
# save to a file
with open("protobuf/vt{}-{}-{}.pbf".format(z, x, y), "wb") as f:
    f.write(pbf)

