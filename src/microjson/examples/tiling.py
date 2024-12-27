from microjson.tilewriter import TileWriter, getbounds
from pathlib import Path
from microjson.tilemodel import TileJSON, TileModel, TileLayer
import os
from microjson.polygen import generate_polygons


def main():
    # clear the tiles directory
    os.system("rm -rf tiles")

    # create the tiles directory
    os.makedirs("tiles")

    # Define your vector layers with appropriate settings
    vector_layers = [
        TileLayer(
            id="polygon-layer",
            fields={"id": "String", "polytype": "String"},
            minzoom=0,
            maxzoom=10,
            description="Layer containing polygon data",
            fieldranges={
                "id": [1, 99999999]
            },
            fieldenums={
                "polytype": ["Type1", "Type2", "Type3", "Type4"]
            },
        )
    ]

    # Create a microjson file with random polygons
    GRID_SIZE = 10000
    CELL_SIZE = 100
    MIN_VERTICES = 10
    MAX_VERTICES = 100
    meta_types = {
        "id": "str",
        "num_vertices": "int",
    }
    meta_values_options = {
        "polytype": ["Type1", "Type2", "Type3", "Type4"]
    }
    microjson_data_path = "tiles/microjson_data.json"
    generate_polygons(
        GRID_SIZE,
        CELL_SIZE,
        MIN_VERTICES,
        MAX_VERTICES,
        meta_types,
        meta_values_options,
        microjson_data_path
    )

    # get bounds
    maxbounds = getbounds(microjson_data_path)
    # set min to 0
    maxbounds[0] = 0
    maxbounds[1] = 0

    center = [0,
              (maxbounds[0] + maxbounds[2]) / 2,
              (maxbounds[1] + maxbounds[3]) / 2]

    # Instantiate TileModel with your settings
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
        center=center,
        vector_layers=vector_layers
    )

    # Create the root model with your TileModel instance
    tileobj = TileJSON(root=tile_model)

    # export to tilejson
    os.makedirs("tiles", exist_ok=True)
    with open("tiles/metadata.json", "w") as f:
        f.write(tileobj.model_dump_json(indent=2))

    # Initialize the TileHandler
    handler = TileWriter(tile_model, pbf=True)
    handler.microjson2tiles(microjson_data_path, validate=False)


if __name__ == "__main__":
    main()
