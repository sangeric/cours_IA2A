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
        for resource, qty in tile.getResources().items():
            if qty > 0:
                extracted = min(qty, 10)  
                tile.getResources()[resource] -= extracted
                for _ in range(extracted):
                    self.extract(resource)
