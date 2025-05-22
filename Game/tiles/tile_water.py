from .tile import Tile

class TileWater(Tile):
    def __init__(self,q,r):
        super().__init__(q,r, name = "Water", build_options = ["bridge"], resources = ["water"])