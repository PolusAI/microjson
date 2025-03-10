# Original code from geojson2vt
# Copyright (c) 2015, Mapbox
# ISC License terms apply; see LICENSE file for details.

# Modifications by PolusAI, 2024

import math
from abc import ABC, abstractmethod
from .simplify import simplify
from .feature import Slice, create_feature

# converts Microjson feature into an intermediate projected JSON vector format
# with simplification data


def convert(data, options):
    """
    wrapper around AbstractProjector.convert
    """
    projector = options.get('projector')
    bounds = options.get('bounds')
    if projector is None:
        projector = CartesianProjector(
            options.get('bounds')) if bounds is not None else \
            MercatorProjector()

    return projector.convert(data, options)


class AbstractProjector(ABC):
    """
    Abstract class for projectors.
    Concrete classes should implement the project_x and project_y methods.

    """
    def __init__(self, bounds):
        self.bounds = bounds

    @abstractmethod
    def project_x(self, x):
        pass

    @abstractmethod
    def project_y(self, y):
        pass

    def convert(self, data, options):
        features = []
        if data.get('type') == 'FeatureCollection':
            for i in range(len(data.get('features'))):
                self.convert_feature(
                    features,
                    data.get('features')[i],
                    options, i)
                # check that geometry is not empty
                if len(features[-1].get('geometry')) == 0:
                    # remove feature with index i
                    features.pop()

        elif data.get('type') == 'Feature':
            self.convert_feature(features, data, options)
        else:
            # single geometry or a geometry collection
            self.convert_feature(features, {"geometry": data}, options)
        return features

    def convert_feature(self, features, geojson, options, index=None):
        if geojson.get('geometry', None) is None:
            return

        coords = geojson.get('geometry').get('coordinates')

        if coords is not None and len(coords) == 0:
            return

        type_ = geojson.get('geometry').get('type')
        tolerance = math.pow(options.get(
            'tolerance') / ((1 << options.get('maxZoom')) * options.get(
                'extent')), 2)
        geometry = Slice([])
        id_ = geojson.get('id')
        if options.get('promoteId', None) is not None and geojson.get(
            'properties', None) is not None and 'promoteId' in geojson.get(
                'properties'):
            id_ = geojson['properties'][options.get('promoteId')]
        elif options.get('generateId', False):
            id_ = index if index is not None else 0

        if type_ == 'Point':
            self.convert_point(coords, geometry)
        elif type_ == 'MultiPoint':
            for p in coords:
                self.convert_point(p, geometry)
        elif type_ == 'LineString':
            self.convert_line(coords, geometry, tolerance, False)
        elif type_ == 'MultiLineString':
            if options.get('lineMetrics'):
                # explode into linestrings to be able to track metrics
                for line in coords:
                    geometry = Slice([])
                    self.convert_line(line, geometry, tolerance, False)
                    features.append(
                        create_feature(
                            id_,
                            'LineString',
                            geometry,
                            geojson.get('properties')))
                return
            else:
                self.convert_lines(coords, geometry, tolerance, False)
        elif type_ == 'Polygon':
            self.convert_lines(coords, geometry, tolerance, True)
        elif type_ == 'MultiPolygon':
            for polygon in coords:
                newPolygon = []
                self.convert_lines(polygon, newPolygon, tolerance, True)
                geometry.append(newPolygon)
        elif type_ == 'GeometryCollection':
            for singleGeometry in geojson['geometry']['geometries']:
                self.convert_feature(features, {
                    "id": str(id_),
                    "geometry": singleGeometry,
                    "properties": geojson.get('properties')
                }, options, index)
            return
        else:
            raise Exception('Input data is not a valid GeoJSON object.')

        features.append(create_feature(
            id_, type_, geometry, geojson.get('properties')))

    def convert_point(self, coords, out):
        out.append(self.project_x(coords[0]))
        out.append(self.project_y(coords[1]))
        out.append(0)

    def convert_line(self, ring, out, tolerance, isPolygon):
        x0, y0 = None, None
        size = 0

        for j in range(len(ring)):
            x = self.project_x(ring[j][0])
            y = self.project_y(ring[j][1])

            out.append(x)
            out.append(y)
            out.append(0)

            if j > 0:
                if isPolygon:
                    size += (x0 * y - x * y0) / 2  # area
                else:
                    size += math.sqrt(
                        math.pow(x - x0, 2) + math.pow(y - y0, 2))  # length
            x0 = x
            y0 = y

        # last = len(out) - 3
        dosimplify = False
        if dosimplify:
            simplified_line = simplify(
                [[x, y] for x, y in zip(out[0::3], out[1::3])],
                tolerance)  # New call
            out.clear()  # clear existing data
            # check if simplified_line has at least 3 points
            if len(simplified_line) < 3:
                return
            for x, y in simplified_line:
                out.append(x)
                out.append(y)
                out.append(0)

    def convert_lines(self, rings, out, tolerance, isPolygon):
        for i in range(len(rings)):
            geom = Slice([])
            self.convert_line(rings[i], geom, tolerance, isPolygon)
            out.append(geom)


class CartesianProjector(AbstractProjector):
    def project_x(self, x):
        return (x - self.bounds[0]) / (self.bounds[2] - self.bounds[0])

    def project_y(self, y):
        return (y - self.bounds[1]) / (self.bounds[3] - self.bounds[1])


class MercatorProjector(AbstractProjector):
    def project_x(self, x):
        return x / 360. + 0.5

    def project_y(self, y):
        sin = math.sin(y * math.pi / 180.)
        if sin == 1.:
            return 0.
        if sin == -1.:
            return 1.
        y2 = 0.5 - 0.25 * math.log((1. + sin) / (1. - sin)) / math.pi
        return 0 if y2 < 0. else (1. if y2 > 1. else y2)
