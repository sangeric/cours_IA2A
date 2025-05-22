import random

class Tile:
    def __init__(self,q,r):
        self.q = q
        self.r = r
        self.name = ""
        self.walkable = False
        self.build_options = []
        self.resources = {
            "rock": 0,
            "coal": 0,
            "water": 0,
            "wood": 0
        }
    def position(self):
        return(self.q,self.r)
    
