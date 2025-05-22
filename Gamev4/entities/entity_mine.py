import time
from .entity import Entity

class EntityMine(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        self.extractable_items = ["rock"]
        self.last_extract_time = time.time()
    
    def extract(self, item):
        if item in self.extractable_items:
            self.inventory[item] = self.inventory.get(item, 0) + 1
        
    def update(self, tile):
        now = time.time()
        if now - self.last_extract_time >= 0.01:
            if tile.getResources().get("rock", 0) > 0:
                tile.getResources()["rock"] -= 1
                self.extract("rock")
            self.last_extract_time = now