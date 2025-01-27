from typing import List, Optional

from microjson.vt2pbf.config import EXTEND
from microjson.vt2pbf.exceptions import LayerExistError
from microjson.vt2pbf.service.layer import Layer

from mapbox_vector_tile.Mapbox import vector_tile_pb2


class Tile:
    def __init__(self, extend: Optional[int] = None):
        self.tile_pbf = vector_tile_pb2.tile()
        self.extend = extend or EXTEND
        self._layers: dict[str, Layer] = {}

    def serialize_to_bytestring(self) -> bytes:
        return self.tile_pbf.SerializeToString()

    def add_layer(self, name: str, features: List[dict]):
        if name in self._layers:
            raise LayerExistError(
                'Layer with this name already exist in the tile')

        layer = Layer(self.tile_pbf, name, extend=self.extend)
        for feature in features:
            layer.add_feature(feature)

        self._layers[name] = layer


def parse_from_string(pbf_string: bytes) -> Tile:
    tile = Tile()
    tile.tile_pbf.ParseFromString(pbf_string)
    return tile.tile_pbf
