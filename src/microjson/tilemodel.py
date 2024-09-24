from typing import List, Optional, Union, Dict
from pydantic import BaseModel, AnyUrl, conlist, RootModel
from pathlib import Path


class TileLayer(BaseModel):
    id: str
    fields: Union[None, Dict[str, str], Dict[str, Dict]]
    minzoom: Optional[int] = None
    maxzoom: Optional[int] = None
    description: Optional[str] = None


class TileModel(BaseModel):
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
    minzoom: Optional[int] = None
    maxzoom: Optional[int] = None
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


class TileJSON(RootModel):
    root: TileModel
