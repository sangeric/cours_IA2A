from .entity import Entity

class EntityMine(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        extractable_items = ["rock", "coal"]
    
    def extract(self, item):
        if item in self.extractble_items:
            self.inventory[item] = self.inventory.get(item, 0) + 1
        
        