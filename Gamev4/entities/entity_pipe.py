from .entity import Entity

class EntityPipe(Entity):
    
    def __init__(self, x, y, source, destination):
        super().__init__(x, y)
        self.source = source
        self.destination = destination
        
    def transfer(self, item, amount=1):
        if self.source.inventory[item] < amount:
            return False
        self.source.inventory[item] -= amount
        self.destination.inventory[item] += amount
        return True
    
    
    def getPipe(self):
        return self.pipe

    def setPipe(self, pipe):
        self.pipe = pipe

    def update(self):
        for item in self.source.inventory:
            if self.source.inventory[item] > 0:
                self.transfer(item)
