import time
from .entity import Entity

class EntitySawmil(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        self.extractable_items = ["wood"]
        self.last_extract_time = time.time()
    
    def extract(self, item):
        if item in self.extractable_items:
            self.inventory[item] = self.inventory.get(item, 0) + 1
        
    def update(self, tile):
        now = time.time()
        if now - self.last_extract_time >= 0.01:
            if tile.getResources().get("wood", 0) > 0:
                tile.getResources()["wood"] -= 1
                self.extract("wood")
            self.last_extract_time = now