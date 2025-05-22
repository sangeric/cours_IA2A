from .tile import Tile

class TileForest(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name = "forest", walkable = True, build_options = [])
        self.resources = {
            "rock": 0,
            "coal": 0,
            "water": 0,
            "wood": 500
        }