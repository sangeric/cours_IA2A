from .tile import Tile

class TileForest(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name = "Forest", walkable = True, build_options = [], resources = ["wood"])