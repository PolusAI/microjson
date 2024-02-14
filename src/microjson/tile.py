from typing import List, Optional, Union, Dict
from pydantic import BaseModel, HttpUrl, conlist, RootModel


class TileLayer(BaseModel):
    id: str
    fields: Union[None, Dict[str, str], Dict[str, Dict]]
    minzoom: Optional[int] = None
    maxzoom: Optional[int] = None
    description: Optional[str] = None


class TileModel(BaseModel):
    tilejson: str
    tiles: List[HttpUrl]
    format: str
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    attribution: Optional[str] = None
    template: Optional[str] = None
    legend: Optional[str] = None
    scheme: Optional[str] = None
    grid: Optional[List[HttpUrl]] = None
    data: Optional[List[HttpUrl]] = None
    minzoom: Optional[int] = None
    maxzoom: Optional[int] = None
    bounds: Optional[conlist(  # type: ignore
        float,
        min_length=4,
        max_length=4)] = None
    center: Optional[conlist(  # type: ignore
        float,
        min_length=3,
        max_length=3)] = None
    fillzoom: Optional[int] = None
    vector_layers: List[TileLayer]


class TileJSON(RootModel):
    root: TileModel
