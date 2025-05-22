from .tile import Tile

class TileMountain(Tile):
    def __init__(self,q,r):
        super().__init__(q, r, name = "mountain", walkable = False, build_options = ["mine"])
        self.resources = {
            "rock": 500,
            "coal": 500,
            "water": 0,
            "wood": 0
        }