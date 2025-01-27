from .tilemodel import TileModel


class TileHandler:
    """
    Class to handle the generation of tiles from MicroJSON data
    """
    tile_json: TileModel
    pbf: bool
    id_counter: int
    id_set: set

    def __init__(self, tileobj: TileModel, pbf: bool = False):
        """
        Initialize the TileHandler with a TileJSON configuration and optional
        PBF flag

        Args:
        tileobj (TileModel): TileJSON configuration
        pbf (bool): Flag to indicate whether to encode the tiles in PBF

        """
        # read the tilejson file to string
        self.tile_json = tileobj
        self.pbf = pbf
        self.id_counter = 0
        self.id_set = set()
