"""MicroJSON and GeoJSON models, defined manually using pydantic."""
from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, Field, StrictInt, StrictStr, conlist, RootModel
from microjson.provenance import Workflow
from microjson.provenance import WorkflowCollection
from microjson.provenance import Artifact
from microjson.provenance import ArtifactCollection

Coordinates = conlist(float, min_length=2, max_length=3)


class GeoAbstract(BaseModel):
    """Abstract base class for all GeoJSON objects"""

    bbox: Optional[List[float]] = Field(None, min_length=4)


class Point(GeoAbstract):
    """A GeoJSON Point object"""

    type: Literal["Point"]
    coordinates: Coordinates  # type: ignore


class MultiPoint(GeoAbstract):
    """A GeoJSON MultiPoint object"""

    type: Literal["MultiPoint"]
    coordinates: List[Coordinates]  # type: ignore


class LineString(GeoAbstract):
    """A GeoJSON LineString object"""

    type: Literal["LineString"]
    coordinates: List[Coordinates]  # type: ignore


class MultiLineString(GeoAbstract):
    """A GeoJSON MultiLineString object"""

    type: Literal["MultiLineString"]
    coordinates: List[List[Coordinates]]  # type: ignore


class Polygon(GeoAbstract):
    """A GeoJSON Polygon object"""

    type: Literal["Polygon"]
    coordinates: List[List[Coordinates]]  # type: ignore


class MultiPolygon(GeoAbstract):
    """A GeoJSON MultiPolygon object"""

    type: Literal["MultiPolygon"]
    coordinates: List[List[List[Coordinates]]]  # type: ignore


GeometryBaseType = Union[
    Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon
]


class GeometryCollection(GeoAbstract):
    """A GeoJSON GeometryCollection object"""

    type: Literal["GeometryCollection"]
    geometries: List[GeometryBaseType]


GeometryType = Union[  # type: ignore
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
    type(None),
]


class Feature(GeoAbstract):
    """A GeoJSON Feature object"""

    type: Literal["Feature"]
    geometry: GeometryType = Field(  # type: ignore
        ...,
        description="""The geometry of the
                                   feature""",
    )  # type: ignore
    properties: Dict = Field(..., description="""Properties of the feature""")
    id: Optional[Union[StrictStr, StrictInt]] = None


class ValueRange(BaseModel):
    """A range of values for MicroJSON quantitative properties"""

    min: float
    max: float


class FeatureCollection(GeoAbstract):
    """A GeoJSON FeatureCollection object"""

    type: Literal["FeatureCollection"]
    features: List[Feature]


class GeoJSON(RootModel):
    """The root object of a GeoJSON file"""

    root: Union[Feature, FeatureCollection, GeometryType]  # type: ignore


class Unit(Enum):
    """A unit of measurement"""

    ANGSTROM = "angstrom"
    ATTOMETER = "attometer"
    CENTIMETER = "centimeter"
    DECIMETER = "decimeter"
    EXAMETER = "exameter"
    FEMTOMETER = "femtometer"
    FOOT = "foot"
    GIGAMETER = "gigameter"
    HECTOMETER = "hectometer"
    INCH = "inch"
    KILOMETER = "kilometer"
    MEGAMETER = "megameter"
    METER = "meter"
    MICROMETER = "micrometer"
    MILE = "mile"
    MILLIMETER = "millimeter"
    NANOMETER = "nanometer"
    PARSEC = "parsec"
    PETAMETER = "petameter"
    PICOMETER = "picometer"
    TERAMETER = "terameter"
    YARD = "yard"
    YOCTOMETER = "yoctometer"
    YOTTAMETER = "yottameter"
    ZEPTOMETER = "zeptometer"
    ZETTAMETER = "zettameter"
    PIXEL = "pixel"
    RADIAN = "radian"
    DEGREE = "degree"


class AxisType(Enum):
    """The type of an axis"""

    CARTESIAN = "cartesian"
    ANGULAR = "angular"
    TEMPORAL = "temporal"
    SPECTRAL = "spectral"


class Axis(BaseModel):
    """An axis of a coordinate system"""

    name: StrictStr
    type: Optional[AxisType] = None
    unit: Optional[Unit] = None
    pixels_per_unit: Optional[float] = None
    description: Optional[str] = None


class CoordinateSystem(BaseModel):
    """A coordinate system for MicroJSON coordinates"""

    axes: List[Axis]
    transformation_matrix: Optional[List[List[float]]] = None


class Properties(BaseModel):
    """Metadata properties of a MicroJSON feature"""

    string: Optional[Dict[str, str]] = None
    numeric: Optional[Dict[str, float]] = None
    multi_numeric: Optional[Dict[str, List[float]]] = None


class MicroFeature(Feature):
    """A MicroJSON feature, which is a GeoJSON feature with additional
    metadata"""

    coordinatesystem: Optional[List[Axis]] = None
    ref: Optional[Union[StrictStr, StrictInt]] = None
    properties: Properties  # type: ignore


class MicroFeatureCollection(FeatureCollection):
    """A MicroJSON feature collection, which is a GeoJSON feature
    collection with additional metadata"""

    coordinatesystem: Optional[CoordinateSystem] = None
    value_range: Optional[Dict[str, ValueRange]] = None
    descriptive_fields: Optional[List[str]] = None
    properties: Optional[Properties] = None
    id: Optional[Union[StrictStr, StrictInt]] = None
    provenance: Optional[Union[Workflow,
                               WorkflowCollection,
                               Artifact,
                               ArtifactCollection]] = None


class MicroJSON(RootModel):
    """The root object of a MicroJSON file"""

    root: Union[MicroFeature,  # type: ignore
                MicroFeatureCollection,
                GeometryType]
