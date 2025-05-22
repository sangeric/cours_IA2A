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
        self.pipe = None
        
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
    
    def setBuildingRecipe(self, recipe):
        if self.building and hasattr(self.building, "set_recipe"):
            self.building.set_recipe(recipe)
        else:
            print(f"[WARNING] Impossible de définir la recette : aucun bâtiment ou méthode 'set_recipe' manquante sur {self.building}")

    def getPipe(self):
        return self.pipe

    def setPipe(self, pipe):
        self.pipe = pipe
        

    
