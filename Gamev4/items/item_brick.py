from .item import Item

class ItemBrick(Item):
    def __init__(self):
        super().__init__(name = "brick", producible = True)