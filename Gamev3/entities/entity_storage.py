from .entity import Entity

class EntityMine(Entity):
    def __init__(self, q, r):
        super().__init__(q, r, inventory_capacity = 10000, linkable = True)
    