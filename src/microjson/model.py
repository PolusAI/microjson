"""MicroJSON and GeoJSON models, defined manually using pydantic."""
from typing import Any, Optional, Union, Dict, TypeVar
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
