from .entity import Entity

class EntityFactory(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        producible_items = ["plank", "stone", "brick"]
    
    def produce(self, item):
        if item in self.producible_items:
            self.inventory[item] = self.inventory.get(item, 0) + 1
        
        