# Original code from geojson2vt
# Copyright (c) 2015, Mapbox
# ISC License terms apply; see LICENSE file for details.

# Modifications by PolusAI, 2024


def transform_tile(tile, extent):
    if tile.get('transformed', None):
        return tile

    z2 = 1 << tile.get('z')
    tx = tile.get('x')
    ty = tile.get('y')

    for feature in tile.get('features', []):
        geom = feature.get('geometry')
        type_ = feature.get('type')

        feature['geometry'] = []

        if type_ == 1:
            for j in range(0, len(geom), 2):
                feature['geometry'].append(transform_point(
                    geom[j], geom[j + 1], extent, z2, tx, ty))
        else:
            for j in range(len(geom)):
                ring = []
                for k in range(0, len(geom[j]), 2):
                    ring.append(transform_point(
                        geom[j][k], geom[j][k + 1], extent, z2, tx, ty))
                feature['geometry'].append(ring)

    tile['transformed'] = True
    return tile


def transform_point(x, y, extent, z2, tx, ty):
    return [
        round(extent * (x * z2 - tx), 0),
        round(extent * (y * z2 - ty), 0)
    ]
