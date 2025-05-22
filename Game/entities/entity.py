class Entity:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.inventory = {
            "rock": 0,
            "brick": 0,
            "coal": 0,
            "plank": 0,
            "stone": 0,
            "water": 0,
            "wood": 0
        }
        inventory_capacity = 0
        linkable = False