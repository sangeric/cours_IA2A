from .tile import Tile

class TileWater(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name="water", walkable=False, build_options=["bridge"])
        self.resources = {
            "rock": 0,
            "coal": 0,
            "water": 500,
            "wood": 0
        }