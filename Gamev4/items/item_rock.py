from .item import Item

class ItemRock(Item):
    def __init__(self):
        super().__init__(name = "rock", source = "mountain")