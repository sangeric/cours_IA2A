from .item import Item

class ItemPlank(Item):
    def __init__(self):
        super().__init__(name = "plank", producible = True)