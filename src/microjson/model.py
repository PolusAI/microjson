"""MicroJSON and GeoJSON models, defined manually using pydantic."""
from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist


Coordinates = conlist(float, min_items=2, max_items=3)


class GeoAbstract(BaseModel):
    """Abstract base class for all GeoJSON objects"""
    bbox: Optional[List[float]] = Field(None, min_items=4)


class Point(GeoAbstract):
    """A GeoJSON Point object"""
    type: Literal["Point"]
    coordinates: Coordinates


class MultiPoint(GeoAbstract):
    """A GeoJSON MultiPoint object"""
    type: Literal["MultiPoint"]
    coordinates: List[Coordinates]


class LineString(GeoAbstract):
    """A GeoJSON LineString object"""
    type: Literal["LineString"]
    coordinates: List[Coordinates]


class MultiLineString(GeoAbstract):
    """A GeoJSON MultiLineString object"""
    type: Literal["MultiLineString"]
    coordinates: List[List[Coordinates]]


class Polygon(GeoAbstract):
    """A GeoJSON Polygon object"""
    type: Literal["Polygon"]
    coordinates: List[List[Coordinates]]


class MultiPolygon(GeoAbstract):
    """A GeoJSON MultiPolygon object"""
    type: Literal["MultiPolygon"]
    coordinates: List[List[List[Coordinates]]]


GeometryBaseType = Union[Point,
                         MultiPoint,
                         LineString,
                         MultiLineString,
                         Polygon,
                         MultiPolygon]


class GeometryCollection(GeoAbstract):
    """A GeoJSON GeometryCollection object"""
    type: Literal["GeometryCollection"]
    geometries: List[GeometryBaseType]


GeometryType = Union[Point,
                     MultiPoint,
                     LineString,
                     MultiLineString,
                     Polygon,
                     MultiPolygon,
                     GeometryCollection,
                     type(None)
                     ]


class Feature(GeoAbstract):
    """A GeoJSON Feature object"""
    type: Literal["Feature"]
    geometry: GeometryType = Field(...,
                                   description="""The geometry of the
                                   feature""")
    properties: Optional[Dict] = Field(...,
                                       description="""Properties of the
                                       feature""")
    id: Optional[Union[StrictStr, StrictInt]]


class ValueRange(BaseModel):
    """A range of values for MicroJSON quantitative properties"""
    min: float
    max: float


class FeatureCollection(GeoAbstract):
    """A GeoJSON FeatureCollection object"""
    type: Literal["FeatureCollection"]
    features: List[Feature]


class GeoJSON(BaseModel):
    """The root object of a GeoJSON file"""
    __root__: Union[Feature, FeatureCollection, GeometryType]


class Unit(Enum):
    """A unit of measurement"""
    ANGSTROM = 'angstrom'
    ATTOMETER = 'attometer'
    CENTIMETER = 'centimeter'
    DECIMETER = 'decimeter'
    EXAMETER = 'exameter'
    FEMTOMETER = 'femtometer'
    FOOT = 'foot'
    GIGAMETER = 'gigameter'
    HECTOMETER = 'hectometer'
    INCH = 'inch'
    KILOMETER = 'kilometer'
    MEGAMETER = 'megameter'
    METER = 'meter'
    MICROMETER = 'micrometer'
    MILE = 'mile'
    MILLIMETER = 'millimeter'
    NANOMETER = 'nanometer'
    PARSEC = 'parsec'
    PETAMETER = 'petameter'
    PICOMETER = 'picometer'
    TERAMETER = 'terameter'
    YARD = 'yard'
    YOCTOMETER = 'yoctometer'
    YOTTAMETER = 'yottameter'
    ZEPTOMETER = 'zeptometer'
    ZETTAMETER = 'zettameter'
    PIXEL = 'pixel'
    RADIAN = 'radian'
    DEGREE = 'degree'


class AxisType(Enum):
    """The type of an axis"""
    CARTESIAN = 'cartesian'
    ANGULAR = 'angular'
    TEMPORAL = 'temporal'
    SPECTRAL = 'spectral'


class Axis(BaseModel):
    """An axis of a coordinate system"""
    name: StrictStr
    type: Optional[AxisType]
    unit: Optional[Unit]
    pixels_per_unit: Optional[float]
    description: Optional[str]


class CoordinateSystem(BaseModel):
    """A coordinate system for MicroJSON coordinates"""
    axes: List[Axis]
    transformation_matrix: Optional[List[List[float]]]


class Properties(BaseModel):
    """Metadata properties of a MicroJSON feature"""
    descriptive: Optional[Dict[str, str]]
    numerical: Optional[Dict[str, float]]
    multi_numerical: Optional[Dict[str, List[float]]]


class MicroFeature(Feature):
    """A MicroJSON feature, which is a GeoJSON feature with additional
    metadata"""
    coordinatesystem: Optional[List[Axis]]
    ref: Optional[Union[StrictStr, StrictInt]]
    properties: Properties


class MicroFeatureCollection(FeatureCollection):
    """A MicroJSON feature collection, which is a GeoJSON feature
    collection with additional metadata"""
    coordinatesystem: Optional[CoordinateSystem]
    value_range: Optional[Dict[str, ValueRange]]
    descriptive_fields: Optional[List[str]]


class MicroJSON(BaseModel):
    """The root object of a MicroJSON file"""
    __root__: Union[MicroFeature,
                    MicroFeatureCollection,
                    GeometryType]
