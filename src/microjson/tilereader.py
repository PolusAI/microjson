from typing import Any
from microjson.tilehandler import TileHandler
import mapbox_vector_tile  # type: ignore
import json
import os


class TileReader(TileHandler):
    """
    Class to read tiles and generate MicroJSON data
    """

    def tiles2microjson(self,
                        zlvl: int = 0) -> dict[str, Any]:
        """
        Generate MicroJSON data from tiles in form of JSON or PBF files.
        Get the TileJSON configuration and the PBF flag from the class
        attributes.
        Check that zlvl is within the maxzoom and minzoom of the tilejson
        Get the bounds from the tilejson and use to generate the MicroJSON
        data, by reading the tiles at the specified zoom level and
        extracting the geometries from the tiles.

        Args:
            zlvl (int): The zoom level of the tiles to read

        Returns:
            dict: The generated MicroJSON data
        """

        # check if zlvl is within the maxzoom and minzoom of the tilejson
        if (self.tile_json.minzoom is None or
                zlvl < self.tile_json.minzoom or
                self.tile_json.maxzoom is None or
                zlvl > self.tile_json.maxzoom):
            return {}

        # get the bounds from the tilejson
        bounds = self.tile_json.bounds
        if bounds is None:
            return {}

        minx = float(bounds[0])
        miny = float(bounds[1])
        maxx = float(bounds[2])
        maxy = float(bounds[3])
        ntiles = 2 ** zlvl
        xstep = (maxx - minx) / ntiles
        ystep = (maxy - miny) / ntiles
        xstarts = [minx + x * xstep for x in range(ntiles)]
        ystarts = [miny + y * ystep for y in range(ntiles)]
        xstops = [minx + (x + 1) * xstep for x in range(ntiles)]
        ystops = [miny + (y + 1) * ystep for y in range(ntiles)]

        # reverse the ystarts and ystops
        # ystarts = ystarts[::-1]
        # ystops = ystops[::-1]

        def project(coord, xmin, ymin, xmax, ymax,
                    extent=4096):
            return [
                (coord[0] / extent * (xmax - xmin) + xmin),
                (coord[1] / extent * (ymax - ymin) + ymin)
            ]

        # get the tilepath from the tilejson
        tilepath = str(self.tile_json.tiles[0])

        # initialize the microjson data
        microjson_data = {
            "type": "FeatureCollection",
            "features": []
        }

        # read the tiles and extract the geometries
        for x in range(ntiles):
            for y in range(ntiles):
                xstart = xstarts[x]
                xstop = xstops[x]
                ystart = ystarts[y]
                ystop = ystops[y]
                # format path template with tile coordinates
                tile_file = tilepath.format(z=zlvl, x=x, y=y)

                if not os.path.exists(str(tile_file)):
                    continue

                with open(
                        str(tile_file),
                        'rb' if str(tile_file).endswith('.pbf') else 'r') as f:
                    tile_data = f.read()

                # decode the tile data
                if self.pbf:
                    tile_data = mapbox_vector_tile.decode(
                        tile_data,
                        default_options={
                            "geojson": True,
                            "y_coord_down": True})
                else:
                    tile_data = json.loads(tile_data)

                # dump to file
                # filename = f"tilevt11_{x}_{y}_{zlvl}.json"

                # with open(filename, "w") as f:
                #    json.dump(tile_data, f)

                tile_data = tile_data['geojsonLayer']

                # extract the geometries
                if 'features' in tile_data.keys():
                    for feature in tile_data['features']:
                        # Transform the coordinates to the global coordinate
                        # system please note that the coordinates may be in
                        # up to 5 nested lists transform the coordinates in
                        # place
                        if 'geometry' in feature:
                            geom = feature['geometry']
                            coord = geom['coordinates']
                            if 'type' in geom:
                                if geom['type'] == 'Point':
                                    geom['coordinates'] = project(
                                        coord, xstart, ystart, xstop, ystop)
                                elif geom['type'] == 'LineString':
                                    geom['coordinates'] = [
                                        project(coord, xstart, ystart, xstop,
                                                ystop)
                                        for coord in geom['coordinates']
                                    ]
                                elif geom['type'] == 'Polygon':
                                    geom['coordinates'] = [
                                        [
                                            project(coord, xstart, ystart,
                                                    xstop, ystop)
                                            for coord in ring
                                        ]
                                        for ring in geom['coordinates']
                                    ]
                                elif geom['type'] == 'MultiPolygon':
                                    geom['coordinates'] = [
                                        [
                                            [
                                                project(coord, xstart, ystart,
                                                        xstop, ystop)
                                                for coord in ring
                                            ]
                                            for ring in poly
                                        ]
                                        for poly in geom['coordinates']
                                    ]
                                else:
                                    continue

                            # add the feature to the microjson data
                            microjson_data['features'].append(  # type: ignore
                                feature)

        return microjson_data
