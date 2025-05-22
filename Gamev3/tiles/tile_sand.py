from .tile import Tile

class TileSand(Tile):
    def __init__(self,q,r):
        super().__init__(q,r, name = "Sand", walkable = True, build_options = ["rail", "train", "factory"])
        