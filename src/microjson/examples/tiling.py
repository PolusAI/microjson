from microjson.tilecut import TileHandler, getbounds
from pathlib import Path
from microjson.tilemodel import TileJSON, TileModel, TileLayer
import json
import os

#clear the tiles directory
os.system("rm -rf tiles")

# Define your vector layers with appropriate settings
vector_layers = [
    TileLayer(
        id="polygon-layer",
        fields={"id": "str", "description": "str"},  # You can specify field types here
        minzoom=0,
        maxzoom=10,
        description="Layer containing polygon data"
    )
]

microjson_data_path = "non_overlapping_polygons.geojson"

# get bounds
maxbounds = getbounds(microjson_data_path)
# set min to 0
maxbounds[0] = 0
maxbounds[1] = 0

center = [0, (maxbounds[0] + maxbounds[2]) / 2, (maxbounds[1] + maxbounds[3]) / 2]

# Instantiate TileModel with the specifics of your data
tile_model = TileModel(
    tilejson="3.0.0",
    tiles=[Path("tiles/{z}/{x}/{y}.pbf")],  # Local path or URL
    name="Example Tile Layer",
    description="A TileJSON example incorporating MicroJSON data",
    version="1.0.0",
    attribution="Polus AI",
    minzoom=0,
    maxzoom=7,
    bounds=maxbounds,
    center= center,  # Example center coordinates and zoom level
    vector_layers=vector_layers
)

# Create the root model with your TileModel instance
tileobj = TileJSON(root=tile_model)

# export to tilejson
os.makedirs("tiles", exist_ok=True)
with open("tiles/metadata.json", "w") as f:
        f.write(tileobj.model_dump_json(indent=2))        


# Define the paths to the TileJSON configuration and the MicroJSON data
# tilejson_path = "tests/json/tilejson/valid/fullexample.json"
#microjson_data_path = "jsonfortiling.json"

# Initialize the TileHandler
handler = TileHandler(tileobj, pbf=True)
geojson2vt_options = {
    'extent': 4096,
    'debug': 0,
    'indexMaxZoom': 0,
    'indexMaxPoints': 100000,
    'indexMaxTiles': 100000,
    'tolerance': 3,
}
handler.microjson2tiles(microjson_data_path, validate=False)

