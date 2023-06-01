
from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, Field, conlist


Coordinates = conlist(float, min_items=2, max_items=3)


class Point(BaseModel):
    type: str = Field("Point", description="Type, must be Point")
    coordinates: Coordinates = Field(..., description="The coordinates of the point")


class MultiPoint(BaseModel):
    type: str = Field("MultiPoint", description="Type, must be MultiPoint")
    coordinates: List[Coordinates] = Field(..., description="The coordinates of the MultiPoint")


class LineString(BaseModel):
    type: str = Field("LineString", description="Type, must be LineString")
    coordinates: List[Coordinates] = Field(..., description="The coordinates of the LineString")


class MultiLineString(BaseModel):
    type: str = Field("MultiLineString", description="Type, must be MultiLineString")
    coordinates: List[List[Coordinates]] = Field(..., description="The coordinates of the MultiLineString")


class Polygon(BaseModel):
    type: str = Field("Polygon", description="Type, must be Polygon")
    coordinates: List[List[Coordinates]] = Field(..., description="The coordinates of the Polygon")


class MultiPolygon(BaseModel):
    type: str = Field("MultiPolygon", description="Type, must be MultiPolygon")
    coordinates: List[List[List[Coordinates]]] = Field(..., description="The coordinates of the MultiPolygon")


Geometry = Union[Point, 
                 MultiPoint, 
                 LineString, 
                 MultiLineString, 
                 Polygon, 
                 MultiPolygon]


class GeometryCollection(BaseModel):
    type: str = Field("GeometryCollection", description="The type of the object, must be GeometryCollection")
    geometries: List[Geometry] = Field(..., description="The list of geometries in the collection")


class Feature(BaseModel):
    type: str = Field("Feature", description="The type of the object, must be Feature")
    geometry: Geometry = Field(..., description="The geometric data of the feature")
    properties: Optional[Dict] = Field(None, description="The properties associated with the collection")


class FeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="The type of the object, must be FeatureCollection")
    features: List[Feature] = Field(..., description="The list of features in the collection")
    properties: Optional[Dict] = Field(None, description="The properties associated with the collection")


class GeoJSON(BaseModel):
    """The root object of a GeoJSON file"""
    __root__: Union[Feature, FeatureCollection, Geometry, GeometryCollection]


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
    axes: List[Literal["x", "y", "z", "r", "theta", "phi"]] = Field(..., description="The coordinate system of the coordinates")
    units: List[Unit] = Field(..., description="The units of the coordinates")
    pixelsPerUnit: List[float] = Field(..., description="The number of pixels per unit")


class MicroFeature(BaseModel):
    type: str
    properties: Optional[Dict]
    geometry: Geometry
    coordinatesystem: Coordinatesystem


class MicroFeatureCollection(BaseModel):
    type: str
    features: List[Feature]
    coordinatesystem: Coordinatesystem


class MicroGeometry(BaseModel):
    geometry: Geometry
    coordinatesystem: Coordinatesystem


class MicroGeometryCollection(BaseModel):
    geometries: GeometryCollection
    coordinatesystem: Coordinatesystem


class MicroJSON(BaseModel):
    """The root object of a MicroJSON file"""
    __root__: Union[MicroFeature, 
                    MicroFeatureCollection, 
                    MicroGeometry, 
                    MicroGeometryCollection]
