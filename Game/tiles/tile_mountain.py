from .tile import Tile

class TileMountain(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name = "Mountain", build_options = ["mine"], resources = ["rock","coal"])