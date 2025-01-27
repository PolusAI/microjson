"""MicroJSON Roundtrip for GeoJSON, generated automatically
by datamodel-codegen from models exported from
Pydantic models"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic.v1 import BaseModel, Field


class Type(Enum):
    point = 'Point'


class Point(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type = Field(..., title='Type')
    coordinates: List[float] = Field(...,
                                     max_length=3,
                                     min_length=2,
                                     title='Coordinates')


class Type1(Enum):
    multi_point = 'MultiPoint'


class MultiPoint(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type1 = Field(..., title='Type')
    coordinates: List[List[float]] = Field(..., title='Coordinates')


class Type2(Enum):
    line_string = 'LineString'


class LineString(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type2 = Field(..., title='Type')
    coordinates: List[List[float]] = Field(..., title='Coordinates')


class Type3(Enum):
    multi_line_string = 'MultiLineString'


class MultiLineString(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type3 = Field(..., title='Type')
    coordinates: List[List[List[float]]] = Field(..., title='Coordinates')


class Type4(Enum):
    polygon = 'Polygon'


class Polygon(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type4 = Field(..., title='Type')
    coordinates: List[List[List[float]]] = Field(..., title='Coordinates')


class Type5(Enum):
    multi_polygon = 'MultiPolygon'


class MultiPolygon(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type5 = Field(..., title='Type')
    coordinates: List[List[List[List[float]]]] = Field(...,
                                                       title='Coordinates')


class Type6(Enum):
    geometry_collection = 'GeometryCollection'


class GeometryCollection(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type6 = Field(..., title='Type')
    geometries: List[
        Union[Point,
              MultiPoint,
              LineString,
              MultiLineString,
              Polygon,
              MultiPolygon]
    ] = Field(..., title='Geometries')


class Properties(BaseModel):
    descriptive: Optional[Dict[str, str]] = Field(None, title='Descriptive')
    numerical: Optional[Dict[str, float]] = Field(None, title='Numerical')
    multiNumerical: Optional[Dict[str, List[float]]] = Field(
        None, title='Multi Numerical'
    )


class Unit(Enum):
    angstrom = 'angstrom'
    attometer = 'attometer'
    centimeter = 'centimeter'
    decimeter = 'decimeter'
    exameter = 'exameter'
    femtometer = 'femtometer'
    foot = 'foot'
    gigameter = 'gigameter'
    hectometer = 'hectometer'
    inch = 'inch'
    kilometer = 'kilometer'
    megameter = 'megameter'
    meter = 'meter'
    micrometer = 'micrometer'
    mile = 'mile'
    millimeter = 'millimeter'
    nanometer = 'nanometer'
    parsec = 'parsec'
    petameter = 'petameter'
    picometer = 'picometer'
    terameter = 'terameter'
    yard = 'yard'
    yoctometer = 'yoctometer'
    yottameter = 'yottameter'
    zeptometer = 'zeptometer'
    zettameter = 'zettameter'
    pixel = 'pixel'
    radian = 'radian'
    degree = 'degree'


class Axe(Enum):
    x = 'x'
    y = 'y'
    z = 'z'
    r = 'r'
    theta = 'theta'
    phi = 'phi'


class Multiscale(BaseModel):
    axes: List[Axe] = Field(..., title='Axes')
    units: Optional[List[Unit]] = None
    pixelsPerUnit: Optional[List[float]] = Field(
        None, alias='pixelsPerUnit', title='Pixelsperunit'
    )


class Type7(Enum):
    feature = 'Feature'


class MicroFeature(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type7 = Field(..., title='Type')
    geometry: Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        GeometryCollection,
    ] = Field(
        ...,
        description='The geometry of the feature',
        title='Geometry',
    )
    properties: Properties
    id: Optional[Union[str, int]] = Field(None, title='Id')
    multiscale: Optional[Multiscale] = None
    ref: Optional[Union[str, int]] = Field(None, title='Ref')


class Feature(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type7 = Field(..., title='Type')
    geometry: Union[
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        GeometryCollection,
    ] = Field(
        ...,
        description='The geometry of the feature',
        title='Geometry',
    )
    properties: Dict[str, Any] = Field(
        ...,
        description='Properties of the feature',
        title='Properties',
    )
    id: Optional[Union[str, int]] = Field(None, title='Id')


class Type9(Enum):
    feature_collection = 'FeatureCollection'


class MicroFeatureCollection(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4, title='Bbox')
    type: Type9 = Field(..., title='Type')
    features: List[Feature] = Field(..., title='Features')
    multiscale: Optional[Multiscale] = None


class MicroJSON(BaseModel):
    __root__: Union[
        MicroFeature,
        MicroFeatureCollection,
        Point,
        MultiPoint,
        LineString,
        MultiLineString,
        Polygon,
        MultiPolygon,
        GeometryCollection,
    ] = Field(...,
              description='The root object of a MicroJSON file',
              title='MicroJSON')
