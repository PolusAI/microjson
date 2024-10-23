# Original code from geojson2vt
# Copyright (c) 2015, Mapbox
# ISC License terms apply; see LICENSE file for details.

# Modifications by PolusAI, 2024

from .simplify import simplify


def create_tile(features, z, tx, ty, options):
    features = features if features is not None else []
    tolerance = 0 if z == options.get(
        'maxZoom') else options.get(
            'tolerance') / \
        ((1 << z) * options.get('extent'))
    tile = {
        "features": [],
        "numPoints": 0,
        "numSimplified": 0,
        "numFeatures": len(features),
        "source": None,
        "x": tx,
        "y": ty,
        "z": z,
        "transformed": False,
        "minX": 2,
        "minY": 1,
        "maxX": -1,
        "maxY": 0
    }
    for feature in features:
        add_feature(tile, feature, tolerance, options)
    return tile


def add_feature(tile, feature, tolerance, options):
    geom = feature.get('geometry')
    type_ = feature.get('type')
    simplified = []

    tile['minX'] = min(tile['minX'], feature['minX'])
    tile['minY'] = min(tile['minY'], feature['minY'])
    tile['maxX'] = max(tile['maxX'], feature['maxX'])
    tile['maxY'] = max(tile['maxY'], feature['maxY'])

    if type_ == 'Point' or type == 'MultiPoint':
        for i in range(0, len(geom), 3):
            simplified.append(geom[i])
            simplified.append(geom[i + 1])
            tile['numPoints'] += 1
            tile['numSimplified'] += 1

    elif type_ == 'LineString':
        add_line(simplified, geom, tile, tolerance, False, False)

    elif type_ == 'MultiLineString' or type_ == 'Polygon':
        for i in range(len(geom)):
            add_line(simplified, geom[i], tile,
                     tolerance, type_ == 'Polygon', i == 0)

    elif type_ == 'MultiPolygon':
        for k in range(len(geom)):
            polygon = geom[k]
            for i in range(len(polygon)):
                add_line(simplified, polygon[i], tile, tolerance, True, i == 0)

    if len(simplified) > 0:
        tags = feature.get('tags')

        if type_ == 'LineString' and options.get('lineMetrics'):
            tags = {}
            for key in feature.get('tags'):
                tags[key] = feature['tags'][key]
            tags['mapbox_clip_start'] = geom.start / geom.size
            tags['mapbox_clip_end'] = geom.end / geom.size

        tileFeature = {
            "geometry": simplified,
            "type": 3 if type_ == 'Polygon' or type_ == 'MultiPolygon' else (
                2 if type_ == 'LineString' or type_ == 'MultiLineString' else 1),
            "tags": tags
        }
        current_id = feature.get('id', None)
        if current_id is not None:
            tileFeature['id'] = current_id
        tile['features'].append(tileFeature)


def add_line(result, geom, tile, tolerance, is_polygon, is_outer):
    sq_tolerance = tolerance * tolerance
    # Convert geom to list of [x, y] pairs
    coords = [[geom[i], geom[i+1]] for i in range(0, len(geom), 3)]

    if tolerance > 0:
        simplified_coords = simplify(coords, sq_tolerance)
    else:
        simplified_coords = coords

    # flatten the simplified coords to a 1D list of x, y, 0 values
    ring = []
    for i in range(len(simplified_coords)):
        ring.append(simplified_coords[i][0])
        ring.append(simplified_coords[i][1])
        tile["numPoints"] += 1

    if is_polygon:
        rewind(ring, is_outer)
    
    result.append(ring)


def rewind(ring, clockwise):
    area = 0
    ringl = len(ring)
    j = ringl - 2
    for i in range(0, ringl, 2):
        area += (ring[i] - ring[j]) * (ring[i + 1] + ring[j + 1])
        j = i
    if (area > 0) == clockwise:
        for i in range(0, ringl, 2):
            x = ring[i]
            y = ring[i + 1]
            ring[i] = ring[ringl - 2 - i]
            ring[i + 1] = ring[ringl - 1 - i]
            ring[ringl - 2 - i] = x
            ring[ringl - 1 - i] = y
