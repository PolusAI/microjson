from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, Field, StrictInt, StrictStr
from geojson.Feature import GeojsonFeature
from geojson.FeatureCollection import GeojsonFeaturecollection
from geojson.Geometry import GeojsonGeometry
from geojson.GeometryCollection import GeojsonGeometrycollection
from geojson.LineString import GeojsonLinestring
from geojson.MultiLineString import GeojsonMultilinestring
from geojson.MultiPoint import GeojsonMultipoint
from geojson.MultiPolygon import GeojsonMultipolygon
from geojson.Point import GeojsonPoint
from geojson.Polygon import GeojsonPolygon


class GeoJSONAuto(BaseModel):
    __root__: Union[
        GeojsonFeature,
        GeojsonFeaturecollection,
        GeojsonGeometry,
        GeojsonGeometrycollection,
    ]


class Unit(Enum):
    PIXEL = "pixel"
    METER = "meter"
    DECIMETER = "decimeter"
    CENTIMETER = "centimeter"
    MILLIMETER = "millimeter"
    MICROMETER = "micrometer"
    NANOMETER = "nanometer"
    PICOMETER = "picometer"
    RADIAN = "radian"
    DEGREE = "degree"


class Coordinatesystem(BaseModel):
    axes: List[Literal["x", "y", "z", "r", "theta", "phi"]] = Field(
        ..., description="The coordinate system of the coordinates"
    )
    units: List[Unit] = Field(..., description="The units of the coordinates")
    pixelsPerUnit: List[float] = Field(
        ..., description="The number of pixels per unit"
    )


class MicroFeature(BaseModel):
    type: Literal["Feature"]
    properties: Optional[Dict]
    geometry: Optional[GeojsonGeometry]
    coordinatesystem: Optional[Coordinatesystem]
    id: Optional[Union[StrictStr, StrictInt]]


class MicroFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"]
    features: List[GeojsonFeature]
    coordinatesystem: Optional[Coordinatesystem]


class MicroPoint(GeojsonPoint):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiPoint(GeojsonMultipoint):
    coordinatesystem: Optional[Coordinatesystem]


class MicroLineString(GeojsonLinestring):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiLineString(GeojsonMultilinestring):
    coordinatesystem: Optional[Coordinatesystem]


class MicroPolygon(GeojsonPolygon):
    coordinatesystem: Optional[Coordinatesystem]


class MicroMultiPolygon(GeojsonMultipolygon):
    coordinatesystem: Optional[Coordinatesystem]


class MicroGeometryCollection(GeojsonGeometrycollection):
    coordinatesystem: Optional[Coordinatesystem]


MicroGeometryType = Union[MicroPoint,
                          MicroMultiPoint,
                          MicroLineString,
                          MicroMultiLineString,
                          MicroPolygon,
                          MicroMultiPolygon,
                          MicroGeometryCollection]


class MicroJSONAuto(BaseModel):
    """The root object of a MicroJSON file"""
    __root__: Union[MicroFeature,
                    MicroFeatureCollection,
                    MicroGeometryType]
