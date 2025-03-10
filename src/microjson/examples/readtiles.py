import json
from microjson.tilereader import TileReader
from microjson.tilemodel import TileModel


def main():
    # Load a TileJSON metadata file from the 'tiles' folder
    with open('tiles/metadata.json', 'r') as f:
        tilejson_data = json.load(f)

    # Construct a TileModel from the parsed data
    tile_model = TileModel.model_validate(tilejson_data)

    # Initialize the TileReader (pass pbf=True if using PBF tiles)
    reader = TileReader(tile_model, pbf=True)

    # Read zoom level 0 (adjust as needed)
    microjson_data = reader.tiles2microjson(zlvl=0)

    print("Generated MicroJSON data for zoom level 0:")
    print(microjson_data)

    # save the microjson data to a file
    with open('tiles/microjson_data_read.json', 'w') as f:
        json.dump(microjson_data, f)


if __name__ == "__main__":
    main()
