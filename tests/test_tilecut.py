# Generate a MicroJSON file using the polygon generator
import os
import random
import shutil
import string
import microjson as mj
import pytest
from microjson.tilecut import getbounds, TileHandler
from microjson.polygen import assign_meta_types_and_values, generate_polygons


@pytest.fixture
def tempfolder():
    tempfolder = "tmp{}".format("".join(
        random.choices(string.ascii_lowercase, k=6)))
    os.makedirs(tempfolder, exist_ok=True)
    yield tempfolder
    shutil.rmtree(tempfolder, ignore_errors=True)


def test_tilecut(tempfolder):
    # Create a large temporary MicroJSON file using the polygon generator
    # Create folder with random name, a string of 6 characters
    microjson_data_path = f"{tempfolder}/polygons.json"
    # Parameters
    GRID_SIZE = 200000      # Total size of the grid
    CELL_SIZE = 500        # Size of each cell
    MIN_VERTICES = 5       # Minimum number of vertices per polygon
    MAX_VERTICES = 32      # Maximum number of vertices per polygon
    N_VARIANTS = 40         # Number of possible values for each meta key
    N_KEYS = 10            # Number of meta keys

    # Assign data types and generate 4 values for each meta key
    meta_types, meta_values_options = assign_meta_types_and_values(
        N_KEYS, N_VARIANTS)

    # Generate the feature collection
    feature_collection = generate_polygons(
        GRID_SIZE,
        CELL_SIZE,
        MIN_VERTICES,
        MAX_VERTICES,
        meta_types,
        meta_values_options,
        microjson_data_path
    )

    # Check that the feature collection was created
    assert len(feature_collection) > 0

    # check that the file exists and is not empty
    assert os.path.exists(microjson_data_path)
    assert os.path.getsize(microjson_data_path) > 0

    # Create a TileJSON configuration
    vector_layers = [
        mj.tilemodel.TileLayer(
            id="polygon-layer",
            fields={"id": "str", "description": "str"},
            minzoom=0,
            maxzoom=10,
            description="Layer containing polygon data",
        )
    ]

    maxbounds = getbounds(microjson_data_path)
    maxbounds[0] = 0
    maxbounds[1] = 0

    center = [0,
              (maxbounds[0] + maxbounds[2]) / 2,
              (maxbounds[1] + maxbounds[3]) / 2]

    tileobj = mj.tilemodel.TileJSON(
        tilejson="3.0.0",
        tiles=[tempfolder + "/tiles/{z}/{x}/{y}.pbf"],
        name="Example Tile Layer",
        description="A TileJSON example incorporating MicroJSON data",
        version="1.0.0",
        attribution="Polus AI",
        minzoom=0,
        maxzoom=7,
        bounds=maxbounds,
        center=center,
        vector_layers=vector_layers,
    )

    # create the tiles directory in the tempfolder
    os.makedirs(f"{tempfolder}/tiles", exist_ok=True)
    # dump the tilejson to a file
    with open(f"{tempfolder}/tiles/metadata.json", "w") as f:
        f.write(tileobj.model_dump_json(indent=2))

    # Check that the TileJSON file was created
    assert os.path.exists(f"{tempfolder}/tiles/metadata.json")
    assert os.path.getsize(f"{tempfolder}/tiles/metadata.json") > 0

    # Initialize the TileHandler
    handler = TileHandler(tileobj, pbf=True)

    # Cut the MicroJSON file into tiles
    tiles = handler.microjson2tiles(microjson_data_path)

    # Check that the tiles were created
    assert len(tiles) > 0
