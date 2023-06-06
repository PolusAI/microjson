from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist


Coordinates = conlist(float, min_items=2, max_items=3)


class GeoAbstract(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_items=4)


class Point(GeoAbstract):
    type: Literal["Point"]
    coordinates: Coordinates


class MultiPoint(GeoAbstract):
    type: Literal["MultiPoint"]
    coordinates: List[Coordinates]


class LineString(GeoAbstract):
    type: Literal["LineString"]
    coordinates: List[Coordinates]


class MultiLineString(GeoAbstract):
    type: Literal["MultiLineString"]
    coordinates: List[List[Coordinates]]


class Polygon(GeoAbstract):
    type: Literal["Polygon"]
    coordinates: List[List[Coordinates]]


class MultiPolygon(GeoAbstract):
    type: Literal["MultiPolygon"]
    coordinates: List[List[List[Coordinates]]]


GeometryBaseType = Union[Point,
                         MultiPoint,
                         LineString,
                         MultiLineString,
                         Polygon,
                         MultiPolygon]


class GeometryCollection(GeoAbstract):
    type: Literal["GeometryCollection"]
    geometries: List[GeometryBaseType]


GeometryType = Union[Point,
                     MultiPoint,
                     LineString,
                     MultiLineString,
                     Polygon,
                     MultiPolygon,
                     GeometryCollection]


class Feature(GeoAbstract):
    type: Literal["Feature"]
    geometry: Optional[GeometryType] = Field(...,
                                             description="""The geometric data
                                             of the feature""")
    properties: Optional[Dict] = Field(...,
                                       description="""Properties of the
                                       feature""")
    id: Optional[Union[StrictStr, StrictInt]]


class FeatureCollection(GeoAbstract):
    type: Literal["FeatureCollection"]
    features: List[Feature]


class GeoJSON(BaseModel):
    """The root object of a GeoJSON file"""
    __root__: Union[Feature, FeatureCollection, GeometryType]


class Unit(Enum):
    PIXEL = 'pixel'
    METER = 'meter'
    DECIMETER = 'decimeter'
    CENTIMETER = 'centimeter'
    MILLIMETER = 'millimeter'
    MICROMETER = 'micrometer'
    NANOMETER = 'nanometer'
    PICOMETER = 'picometer'
    RADIAN = 'radian'
    DEGREE = 'degree'


class Coordinatesystem(BaseModel):
    axes: List[Literal["x", "y", "z", "r", "theta", "phi"]] = Field(
        ..., description="The coordinate system of the coordinates"
    )
    units: List[Unit] = Field(..., description="The units of the coordinates")
    pixelsPerUnit: List[float] = Field(
        ..., description="The number of pixels per unit"
    )


class MicroPoint(Point):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiPoint(MultiPoint):
    coordinatesystem: Optional[Coordinatesystem]


class MicroLineString(LineString):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiLineString(MultiLineString):
    coordinatesystem: Optional[Coordinatesystem]


class MicroPolygon(Polygon):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiPolygon(MultiPolygon):
    coordinatesystem: Optional[Coordinatesystem]


class MicroGeometryCollection(GeometryCollection):
    coordinatesystem: Optional[Coordinatesystem]


class MicroFeature(Feature):
    coordinatesystem: Optional[Coordinatesystem]


class MicroFeatureCollection(FeatureCollection):
    coordinatesystem: Optional[Coordinatesystem]


MicroGeometryType = Union[MicroPoint,
                          MicroMultiPoint,
                          MicroLineString,
                          MicroMultiLineString,
                          MicroPolygon,
                          MicroMultiPolygon,
                          MicroGeometryCollection]


class MicroJSON(BaseModel):
    """The root object of a MicroJSON file"""
    __root__: Union[MicroFeature,
                    MicroFeatureCollection,
                    MicroGeometryType]
