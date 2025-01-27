import os
from .microjson2vt.microjson2vt import microjson2vt
from .tilehandler import TileHandler
from microjson import MicroJSON
import json
from pydantic import ValidationError

from typing import List, Union
from pathlib import Path
import logging
from shapely.geometry import Polygon
from .vt2pbf import vt2pbf

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def getbounds(microjson_file: str, square: bool = False) -> List[float]:
    """
    Get the max and min bounds for coordinates of the MicroJSON file

    Args:
        microjson_file (str): Path to the MicroJSON file
        square (bool): Flag to indicate whether to return square bounds

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
    if square:
        maxx = max(maxx - minx, maxy - miny) + minx
        maxy = max(maxx - minx, maxy - miny) + miny
    return [minx, miny, maxx, maxy]


def geojson2vt_to_shapely(geometry_data):
    # Extract coordinates and type

    geom_type = geometry_data['type']

    # Based on the `type` field, determine the geometry shape
    if geom_type == 3:  # 3 usually represents Polygon in such data formats
        coordinates = geometry_data['geometry'][0]  # Only take outer ring
        geometry_data['geometry'] = Polygon(coordinates)
    else:
        raise ValueError("Unsupported geometry type")

    return geometry_data


def extract_fields_ranges_enums(microjson_file: str):
    """
    Extract field names, ranges, and enums from the provided MicroJSON
    file.
    Returns:
        tuple: (dict with field names and types,
                dict of field ranges,
                dict of field enums)
    """
    import json

    def get_json_type(value):
        if value is None:
            # Set to String if None
            return 'String'
        if isinstance(value, bool):
            return 'Boolean'
        if isinstance(value, (int, float)):
            return 'Number'
        if isinstance(value, dict):
            return 'Object'
        if isinstance(value, list):
            return 'Array'
        return 'String'

    with open(microjson_file, 'r') as file:
        data = json.load(file)

    field_names: dict[str, str] = {}
    field_ranges = {}
    field_enums: dict[str, set[str]] = {}

    for feature in data.get('features', []):
        props = feature.get('properties', {})
        for key, val in props.items():
            if key not in field_names.keys():
                field_names[key] = get_json_type(val)
            if isinstance(val, (int, float)):
                if key not in field_ranges:
                    field_ranges[key] = [val, val]
                else:
                    field_ranges[key][0] = min(field_ranges[key][0], val)
                    field_ranges[key][1] = max(field_ranges[key][1], val)
            if isinstance(val, str):
                if key not in field_enums:
                    field_enums[key] = set()
                field_enums[key].add(val)

    return field_names, field_ranges, field_enums


class TileWriter (TileHandler):

    def microjson2tiles(self,
                        microjson_data_path: Union[str, Path],
                        validate: bool = False
                        ) -> List[str]:
        """
        Generate tiles in form of JSON or PBF files from MicroJSON data.

        Args:
            microjson_data_path (Union[str, Path]): Path to the
            MicroJSON data file
            validate (bool): Flag to indicate whether to validate
            the MicroJSON data

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
                'wb' if tile_path.endswith('.pbf') else 'w'
            ) as f:
                f.write(tile_data)

            # return the path to the saved tile
            return tile_path

        def convert_id_to_int(data) -> int | dict | list:
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
                      self.tile_json.vector_layers[0].maxzoom)  # type: ignore
        minzoom = max(self.tile_json.minzoom,
                      self.tile_json.vector_layers[0].minzoom)  # type: ignore

        # Options for geojson2vt from TileJSON
        options = {
            'maxZoom': maxzoom,  # max zoom in the final tileset
            'indexMaxZoom': self.tile_json.maxzoom,  # tile index max zoom
            'indexMaxPoints': 0,  # max number of points per tile, 0 if none
            'bounds': self.tile_json.bounds
        }

        # Convert GeoJSON to intermediate vector tiles
        tile_index = microjson2vt(microjson_data, options)

        # Placeholder for the tile paths
        generated_tiles = []

        # get tilepath from tilejson self.tile_json.tiles
        # extract the folder from the filepath

        for tileno in tile_index.tiles:
            atile = tile_index.tiles[tileno]
            x, y, z = atile["x"], atile["y"], atile["z"]
            # if z is less than minzoom, or greater than maxzoom, skip the tile
            if z < minzoom or z > maxzoom:
                continue
            tile_data = tile_index.get_tile(z, x, y)

            for item in tile_data['features']:
                if 'id' in item:
                    item['id'] = int(item['id'])

            # add name to the tile_data
            tile_data["name"] = "tile"
            if self.pbf:
                # Using vt2pbf to encode tile data to PBF
                encoded_data = vt2pbf(tile_data)
            else:

                encoded_data = json.dumps(tile_data)

            generated_tiles.append(save_tile(
                encoded_data, z, x, y, self.tile_json.tiles[0]))

        return generated_tiles
