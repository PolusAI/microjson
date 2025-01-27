from microjson.tilewriter import (
    TileWriter,
    getbounds,
    extract_fields_ranges_enums
)
from pathlib import Path
from microjson.tilemodel import TileJSON, TileModel, TileLayer
import os
from microjson.polygen import generate_polygons
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("microjson_data_path", nargs='?',
                        default="",
                        help="Path to the MicroJSON data file")
    args = parser.parse_args()

    if args.microjson_data_path:
        microjson_data_path = args.microjson_data_path
        do_generate = False

        # Extract fields, ranges, enums from the provided MicroJSON
        field_names, field_ranges, field_enums = extract_fields_ranges_enums(
            microjson_data_path)

        # Create a TileLayer including the extracted fields
        vector_layers = [
            TileLayer(
                id="extracted-layer",
                fields=field_names,
                minzoom=0,
                maxzoom=10,
                description="Layer with extracted fields",
                fieldranges=field_ranges,
                fieldenums=field_enums,
            )
        ]
    else:
        microjson_data_path = "example.json"
        do_generate = True

    # clear the tiles directory
    os.system("rm -rf tiles")

    # create the tiles directory
    os.makedirs("tiles")

    if do_generate:
        # Create a microjson file with random polygons
        GRID_SIZE = 10000
        CELL_SIZE = 100
        MIN_VERTICES = 10
        MAX_VERTICES = 100
        meta_types = {
            "num_vertices": "int",
        }
        meta_values_options = {
            "polytype": ["Type1", "Type2", "Type3", "Type4"]
        }

        vector_layers = [
            TileLayer(
                id="polygon-layer",
                fields={"id": "String", "polytype": "String"},
                minzoom=0,
                maxzoom=10,
                description="Layer containing polygon data",
                fieldranges={
                    "num_vertices": [10, 100]
                },
                fieldenums={
                    "polytype": ["Type1", "Type2", "Type3", "Type4"]
                },
            )
        ]

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
    maxbounds = getbounds(microjson_data_path, square=True)

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
