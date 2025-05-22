class Entity:
    def __init__(self, x, y, inventory_capacity = 0, linkable = False):
        self.x = x
        self.y = y
        self.inventory_capacity = inventory_capacity
        self.linkable = linkable
        self.inventory = {
            "rock": 0,
            "brick": 0,
            "coal": 0,
            "plank": 0,
            "stone": 0,
            "water": 0,
            "wood": 0
        }