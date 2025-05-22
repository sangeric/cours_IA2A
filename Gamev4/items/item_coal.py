from .item import Item

class ItemCoal(Item):
    def __init__(self):
        super().__init__(name = "coal", source = "mountain")