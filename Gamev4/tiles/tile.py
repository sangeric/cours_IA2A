import random

class Tile:
    def __init__(self, q, r, name="-", walkable=False, build_options=None, entity = None, building = None):
        self.q = q
        self.r = r
        self.name = name
        self.walkable = walkable
        self.build_options = build_options or []
        self.entity = entity
        self.building = building
        
        self.resources = {
            "rock": 0,
            "coal": 0,
            "water": 0,
            "wood": 0
        }
    
    def getName(self):
        return self.name
    
    def getResources(self):
        return self.resources
    
    def getEntity(self):
        return self.entity
    
    def getBuilding(self):
        return self.building
    
    def setBuilding(self, building):
        self.building = building
        

    
