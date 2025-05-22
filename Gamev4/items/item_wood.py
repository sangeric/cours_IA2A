from .item import Item

class ItemWood(Item):
    def __init__(self):
        super().__init__(name = "wood", source = "forest")