from .entity import Entity

class EntityRobot(Entity):
    def __init__(self, q, r):
        super().__init__(q, r, inventory_capacity = 100)
        