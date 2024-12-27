from typing import List, Optional, Union, Dict, Literal
from enum import Enum
from pydantic import BaseModel, AnyUrl, conlist, RootModel
from pydantic import StrictStr
from pathlib import Path


class TileLayer(BaseModel):
    """ A vector layer in a TileJSON file.

    Args:
        id (str): The unique identifier for the layer.
        fields (Union[None, Dict[str, str]]): The fields in the layer.
        minzoom (Optional[int]): The minimum zoom level for the layer.
        maxzoom (Optional[int]): The maximum zoom level for the layer.
        description (Optional[str]): A description of the layer.
        fieldranges (Optional[Dict[str, List[Union[int, float, str]]]]):
            The ranges of the fields.
        fieldenums (Optional[Dict[str, List[str]]]):
            The enums of the fields.
        fielddescriptions (Optional[Dict[str, str]]):
            The descriptions of the fields.
    """
    id: str
    fields: Union[None, Dict[str, str]] = None
    minzoom: Optional[int] = 0
    maxzoom: Optional[int] = 22
    description: Optional[str] = None
    fieldranges: Optional[Dict[str, List[Union[int, float, str]]]] = None
    fieldenums: Optional[Dict[str, List[str]]] = None
    fielddescriptions: Optional[Dict[str, str]] = None


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


class TileModel(BaseModel):
    """ A TileJSON object.

    Args:
        tilejson (str): The TileJSON version.
        tiles (List[Union[Path, AnyUrl]]): The list of tile URLs.
        name (Optional[str]): The name of the tileset.
        description (Optional[str]): The description of the tileset.
        version (Optional[str]): The version of the tileset.
        attribution (Optional[str]): The attribution of the tileset.
        template (Optional[str]): The template of the tileset.
        legend (Optional[str]): The legend of the tileset.
        scheme (Optional[str]): The scheme of the tileset.
        grids (Optional[Union[Path, AnyUrl]]): The grids of the tileset.
        data (Optional[Union[Path, AnyUrl]]): The data of the tileset.
        minzoom (Optional[int]): The minimum zoom level of the tileset.
        maxzoom (Optional[int]): The maximum zoom level of the tileset.
        bounds (Optional[conlist(float, min_length=4, max_length=10)]):
            The bounds of the tileset.
        center (Optional[conlist(float, min_length=3, max_length=6)]):
            The center of the tileset.
        fillzoom (Optional[int]): The fill zoom level of the tileset.
        vector_layers (List[TileLayer]): The vector layers of the tileset.

    """

    tilejson: str
    tiles: List[Union[Path, AnyUrl]]
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    attribution: Optional[str] = None
    template: Optional[str] = None
    legend: Optional[str] = None
    scheme: Optional[str] = None
    grids: Optional[Union[Path, AnyUrl]] = None
    data: Optional[Union[Path, AnyUrl]] = None
    minzoom: Optional[int] = 0
    maxzoom: Optional[int] = 22
    bounds: Optional[conlist(  # type: ignore
        float,
        min_length=4,
        max_length=10)] = None
    center: Optional[conlist(  # type: ignore
        float,
        min_length=3,
        max_length=6)] = None
    fillzoom: Optional[int] = None
    vector_layers: List[TileLayer]
    multiscale: Optional[Multiscale] = None
    scale_factor: Optional[float] = None


class TileJSON(RootModel):
    """ The root object of a TileJSON file."""
    root: TileModel
