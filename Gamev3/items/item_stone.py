from .item import Item

class ItemStone(Item):
    def __init__(self):
        super().__init__(name = "stone", producible = True)