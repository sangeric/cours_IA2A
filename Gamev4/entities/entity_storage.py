import time
from .entity import Entity

class EntityStorage(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 10000, linkable = True)
        
    def add_item(self, item, amount):
        current = self.inventory.get(item, 0)
        if current + amount <= self.inventory_capacity:
            self.inventory[item] = current + amount
            return True
        return False