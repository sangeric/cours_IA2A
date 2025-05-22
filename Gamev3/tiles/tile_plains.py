from .tile import Tile

class TilePlains(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name = "Plains", walkable = True, build_options = ["rail","train","factory","storage"])

        