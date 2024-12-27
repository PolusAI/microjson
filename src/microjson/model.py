"""MicroJSON and GeoJSON models, defined manually using pydantic."""
from typing import Any, List, Optional, Union, Dict, Literal, TypeVar
from enum import Enum
from pydantic import BaseModel, StrictInt, StrictStr, RootModel
from .provenance import Workflow
from .provenance import WorkflowCollection
from .provenance import Artifact
from .provenance import ArtifactCollection
from geojson_pydantic import Feature, FeatureCollection, GeometryCollection
from geojson_pydantic import Point, MultiPoint, LineString, MultiLineString
from geojson_pydantic import Polygon, MultiPolygon


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

Props = TypeVar("Props", bound=Union[Dict[str, Any], BaseModel])


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

    SPACE = "space"
    TIME = "time"
    CHANNEL = "channel"


class Axis(BaseModel):
    """An axis of a coordinate system

    Args:
        name (StrictStr): The name of the axis
        type (Optional[AxisType]): The type of the axis
        unit (Optional[Unit]): The unit of the axis
        description (Optional[str]): A description of the axis
    """

    name: StrictStr
    type: Optional[AxisType] = None
    unit: Optional[Unit] = None
    description: Optional[str] = None


class CoordinateTransformation(BaseModel):
    """Coordinate transformation abstract class
    harmonized with the OME model"""


class Identity(CoordinateTransformation):
    """Identity transformation for coordinates

    Args:
        type (Literal["identity"]): The type of the transformation
    """

    type: Literal["identity"] = "identity"


class Translation(CoordinateTransformation):
    """Translation transformation

    Args:
        type (Literal["translation"]): The type of the transformation
        translation (List[float]): The translation vector
    """

    type: Literal["translation"] = "translation"
    translation: List[float]


class Scale(CoordinateTransformation):
    """Scale transformation

    Args:
        type (Literal["scale"]): The type of the transformation
        scale (List[float]): The scale vector
    """

    type: Literal["scale"] = "scale"
    scale: List[float]


class Multiscale(BaseModel):
    """A coordinate system for MicroJSON coordinates

    Args:
        axes (List[Axis]): The axes of the coordinate system
        coordinateTransformations (Optional[List[CoordinateTransformation]]):
            A list of coordinate transformations
        transformationMatrix (Optional[List[List[float]]):
            The transformation matrix
    """

    axes: List[Axis]
    coordinateTransformations: Optional[List[CoordinateTransformation]] = None
    transformationMatrix: Optional[List[List[float]]] = None


class MicroFeature(Feature):
    """A MicroJSON feature, which is a GeoJSON feature with additional
    metadata

    Args:
        multiscale (Optional[Multiscale]): The coordinate system of the feature
        ref (Optional[Union[StrictStr, StrictInt]]):
            A reference to the parent feature
        parentId (Optional[Union[StrictStr, StrictInt]]):
            A reference to the parent feature
        featureClass (Optional[str]): The class of the feature
    """

    multiscale: Optional[Multiscale] = None
    ref: Optional[Union[StrictStr, StrictInt]] = None
    # reference to the parent feature
    parentId: Optional[Union[StrictStr, StrictInt]] = None
    # for now, only string feature class is supported
    # in the future, it may be expanded with a class registry
    featureClass: Optional[str] = None


class MicroFeatureCollection(FeatureCollection):
    """A MicroJSON feature collection, which is a GeoJSON feature
    collection with additional metadata.

    Args:
        properties (Optional[Props]): The properties of the feature collection
        id (Optional[Union[StrictStr, StrictInt]]): The ID of the feature coll.
        provenance (Optional[Union[Workflow,
            WorkflowCollection,
            Artifact,
            ArtifactCollection]]): The provenance of the feature collection
    """

    properties: Optional[Union[Props, None]] = None  # type: ignore
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
