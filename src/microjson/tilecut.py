import os
from .microjson2vt.microjson2vt import microjson2vt
from microjson.tilemodel import TileModel
from microjson import MicroJSON
import json
from pydantic import ValidationError

from typing import List, Union
from pathlib import Path
import logging
from vt2pbf import vt2pbf
# import mapbox_vector_tile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def getbounds(microjson_file: str) -> List[float]:
    """
    Get the max and min bounds for coordinates of the MicroJSON file
    
    Args:
        microjson_file (str): Path to the MicroJSON file

    Returns:
        List[float]: List of the bounds [minx, miny, maxx, maxy]
    """
    with open(microjson_file, 'r') as file:
        data = json.load(file)
    
    # get the bounds
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    if 'features' in data:
        for feature in data['features']:
            if 'geometry' in feature:
                if feature['geometry']['type'] == 'Polygon':
                    for ring in feature['geometry']['coordinates']:
                        for coord in ring:
                            minx = min(minx, coord[0])
                            miny = min(miny, coord[1])
                            maxx = max(maxx, coord[0])
                            maxy = max(maxy, coord[1])
                if feature['geometry']['type'] == 'MultiPolygon':
                    for polygon in feature['geometry']['coordinates']:
                        for ring in polygon:
                            for coord in ring:
                                minx = min(minx, coord[0])
                                miny = min(miny, coord[1])
                                maxx = max(maxx, coord[0])
                                maxy = max(maxy, coord[1])
    return [minx, miny, maxx, maxy]


class TileHandler:
    """
    Class to handle the generation of tiles from MicroJSON data
    """
    tile_json: TileModel
    pbf: bool
    id_counter: int
    id_set: set

    def __init__(self, tileobj: TileModel, pbf: bool = False):
        """
        Initialize the TileHandler with a TileJSON configuration and optional
        PBF flag
       
        Args:
        tileobj (TileModel): TileJSON configuration
        pbf (bool): Flag to indicate whether to encode the tiles in PBF

        """
        # read the tilejson file to string
        self.tile_json = tileobj
        self.pbf = pbf
        self.id_counter = 0
        self.id_set = set()

    def microjson2tiles(self,
                        microjson_data_path: Union[str, Path],
                        validate: bool = False
                        ) -> List[str]:
        """
        Generate tiles in form of JSON or PBF files from MicroJSON data.

        Args:
            microjson_data_path (Union[str, Path]): Path to the MicroJSON data file
            validate (bool): Flag to indicate whether to validate the MicroJSON data

        Returns:
            List[str]: List of paths to the generated tiles
        """
        def save_tile(tile_data, z, x, y, tiles_path_template):
            """
            Save a single tile to a file based on the template path.

            Args:
                tile_data: The tile data to save
                z: The zoom level of the tile
                x: The x coordinate of the tile
                y: The y coordinate of the tile
                tiles_path_template: The template path for the tiles

            Returns:
                str: The path to the saved tile
            """
            # Format the path template with actual tile coordinates
            tile_path = str(tiles_path_template).format(z=z, x=x, y=y)
            os.makedirs(os.path.dirname(tile_path), exist_ok=True)

            # Save the tile data (this assumes tile_data is already in the
            # correct format, e.g., PBF or JSON)
            with open(
                tile_path,
                'wb' if tile_path.endswith('.pbf') else 'w') as f:
                f.write(tile_data)
            
            # return the path to the saved tile
            return tile_path

        def convert_id_to_int(data) -> dict:
            """
            Convert all id fields in the data to integers

            Args:
                data: The data to convert

            Returns:
                dict: The data with all id fields converted to integers
            """
        

            # check if data is a list
            if isinstance(data, list):
                for item in data:
                    convert_id_to_int(item)
                return data
            # check if data is a dict
            elif isinstance(data, dict):
                for key, value in data.items():
                    if key == 'id':
                        if value is None:
                            data[key] = self.id_counter
                            self.id_counter += 1
                        else:
                            data[key] = int(value)
                        while data[key] in self.id_set:
                            self.id_counter += 1
                            data[key] = self.id_counter
                        self.id_set.add(data[key])
                    if isinstance(value, dict):
                        convert_id_to_int(value)
                    if isinstance(value, list):
                        for item in value:
                            convert_id_to_int(item)
                return data
            else:
                return int(data)
            
        # Load the MicroJSON data
        with open(microjson_data_path, 'r') as file:
            microjson_data = json.load(file)
        
        # Validate the MicroJSON data
        if validate:
            try:
                MicroJSON.model_validate(microjson_data)
            except ValidationError as e:
                logger.error(f"MicroJSON data validation failed: {e}")
                return []
        
        # TODO currently only supports one tile layer
        # calculate maxzoom and minzoom from layer and global tilejson

        maxzoom = min(self.tile_json.maxzoom, 
                      self.tile_json.vector_layers[0].maxzoom)
        minzoom = max(self.tile_json.minzoom,
                      self.tile_json.vector_layers[0].minzoom)

        # Options for geojson2vt from TileJSON
        options = {
            'maxZoom': maxzoom,  # max zoom in the final tileset
            'indexMaxZoom': self.tile_json.maxzoom,  # max zoom in the initial tile index
            'indexMaxPoints': 0,  # max number of points per tile, set to 0 for no restriction
            'bounds': self.tile_json.bounds
        }

        # Convert GeoJSON to intermediate vector tiles
        tile_index = microjson2vt(microjson_data, options)

        # Placeholder for the tile paths
        generated_tiles = []

        # get tilepath from tilejson self.tile_json.tiles
        # extract the folder from the filepath
        tilefolder = Path(self.tile_json.tiles[0]).parent


        for tileno in tile_index.tiles:
            atile = tile_index.tiles[tileno]
            x, y, z = atile["x"], atile["y"], atile["z"]
            # if z is less than minzoom, or greater than maxzoom, skip the tile
            if z < minzoom or z > maxzoom:
                continue
            tile_data = tile_index.get_tile(z, x, y)

            # convert all id to int, as there is a bug in the geojson2vt
            # library
            tile_data = convert_id_to_int(tile_data)

            # add name to the tile_data
            tile_data["name"] = "tile"
            if self.pbf:
                # Using mapbox_vector_tile to encode tile data to PBF
                encoded_data = vt2pbf(tile_data)
            else:
                encoded_data = json.dumps(tile_data)

            generated_tiles.append(save_tile(
                encoded_data, z, x, y, self.tile_json.tiles[0]))

        return generated_tiles
        