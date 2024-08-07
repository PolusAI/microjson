import os
from geojson2vt.geojson2vt import geojson2vt
from geojson2vt import utils as g2vt_utils
from tile import TileJSON
from model import MicroJSON
import json
from pydantic import ValidationError

from typing import List, Dict, Union
import json
from pathlib import Path
import logging
from shapely.geometry import shape
from vt2pbf import vt2pbf
# import mapbox_vector_tile


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def getbounds(microjson_file : str) -> List[int]:
    """
    Get the max and min bounds for coordinates of the MicroJSON file
    :param microjson_file: Path to the MicroJSON file
    :return: List of max and min bounds for the coordinates
    Format: [minx, miny, maxx, maxy]
    """
    with open(microjson_file, 'r') as file:
        data = json.load(file)
    
    # get the bounds
    minx, miny, maxx, maxy = float('inf'), float('inf'), float('-inf'), float('-inf')
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
    tile_json: TileJSON
    pbf: bool = False
    id_counter = 10001
    id_set = set()

    def __init__(self, tileobj: TileJSON, pbf: bool = False):
        """
        Initialize the TileHandler with a TileJSON configuration and optional PBF flag
        :param tilejson_path: Path to the TileJSON configuration file
        :param pbf: Flag to indicate whether to generate PBF files
        :param tilefolder: Path to the folder where the generated tiles should be saved"""
        # read the tilejson file to string
        self.tile_json = TileJSON.model_validate(tileobj).root
        self.pbf = pbf


    def microjson2tiles(self,
                        microjson_data_path: Union[str, Path],
                        validate: bool = False
                        ) -> List[str]:
        """
        Generate tiles in form of JSON or PBF files from MicroJSON data.
        :param microjson_data_path: Path to the MicroJSON data.
        :return: List of paths to the generated tiles.
        """
        def save_tile(tile_data, z, x, y, tiles_path_template):
            """
            Save a single tile to a file based on the template path.
            """
            # Format the path template with actual tile coordinates
            tile_path = str(tiles_path_template).format(z=z, x=x, y=y)
            os.makedirs(os.path.dirname(tile_path), exist_ok=True)

            # Save the tile data (this assumes tile_data is already in the correct format, e.g., PBF or JSON)
            with open(tile_path, 'wb' if tile_path.endswith('.pbf') else 'w') as f:
                f.write(tile_data)
            
            # return the path to the saved tile
            return tile_path
        
        def convert_geometry_to_shape(data):
            # Helper function to convert all geometry to shape
            type_mapping = {
                    1: "Point",
                    2: "LineString",
                    3: "Polygon",
                    4: "MultiPoint",
                    5: "MultiLineString",
                    6: "MultiPolygon",
                    7: "GeometryCollection"
                }

            # loop over features
            if 'features' in data:
                for feature in data['features']:
                    # check number of coordinates
                    if len(feature['geometry'][0]) <4 and feature['geometry']['type'] == 'Polygon':
                        # mark for deletion
                        feature['geometry'] = None
                        continue                    

                    geodict = {
                        "type": type_mapping[feature['type']],
                        "coordinates": feature['geometry']
                    }
                    feature['geometry'] = shape(geodict)
                
                # remove all features with None geometry
                data['features'] = [feature for feature in data['features'] if feature['geometry'] is not None]

            return data
        

        def convert_id_to_int(data):
            # Helper function to convert all id to int

            # check if data is a list
            if isinstance(data, list):
                for item in data:
                    convert_id_to_int(item)
                return data
            # check if data is a dict
            elif isinstance(data, dict):
            # helper function to convert all id to int
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
                mjmodel = MicroJSON.model_validate(microjson_data)
            except ValidationError as e:
                logger.error(f"MicroJSON data validation failed: {e}")
                return
        

        # Options for geojson2vt might come from the TileJSON or can be set statically here
        options = {
            'maxZoom': self.tile_json.maxzoom,
            'indexMaxZoom': self.tile_json.maxzoom, # max zoom in the initial tile index
            'indexMaxPoints': 0 # max number of points per tile, set to 0 for no restriction
            
        }

        # Convert GeoJSON to intermediate vector tiles
        tile_index = geojson2vt(microjson_data, options)

        # Placeholder for the tile paths
        generated_tiles = []

        # get tilepath from tilejson self.tile_json.tiles, extract the folder from the filepath
        tilefolder = Path(self.tile_json.tiles[0]).parent


        for tileno in tile_index.tiles:
            atile = tile_index.tiles[tileno]
            x, y, z = atile["x"], atile["y"], atile["z"]
            tile_data = tile_index.get_tile(z, x, y)

            # convert all id to int, as there is a bug in the geojson2vt library
            tile_data = convert_id_to_int(tile_data)

            # convert all geometry to shape
            #tile_data = convert_geometry_to_shape(tile_data)

            # add name to the tile_data
            tile_data["name"] = "tile"
            if self.pbf:
                # Using mapbox_vector_tile to encode tile data to PBF
                # encoded_data = mapbox_vector_tile.encode(tile_data)
                encoded_data = vt2pbf(tile_data)
                # encoded_data = mapbox_vector_tile.encode(tile_data)
            else:
                encoded_data = json.dumps(tile_data)

            generated_tiles.append(save_tile(
                encoded_data, z, x, y, self.tile_json.tiles[0]))

        return generated_tiles
        

    def save_tiles(self, tiles: List[Dict], zoom: int):
        for tile in tiles:
            tile_data = tile["data"]
            if self.pbf:
                tile_data = self.microjson2pbf(tile_data)
            # Save to file or database as needed
            # Example file saving
            with open(f"tile_{zoom}.json", "w") if not self.pbf else open(f"tile_{zoom}.pbf", "wb") as file:
                file.write(json.dumps(tile_data) if not self.pbf else tile_data)

    def pbf2json(self, pbf_data: bytes) -> Dict:
        """
        Convert a PBF binary to JSON
        :param pbf_data: PBF binary data
        :return: JSON data
        """
        tile = mapbox_vector_tile.decode(pbf_data)

        return tile

        # vt-json to geojson
        

