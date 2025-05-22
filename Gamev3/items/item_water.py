from .item import Item

class ItemWater(Item):
    def __init__(self):
        super().__init__(name = "water", source = "water")