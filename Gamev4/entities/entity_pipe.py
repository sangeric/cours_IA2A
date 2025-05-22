from .entity import Entity

class EntityPipe(Entity):
    def __init__(self, x, y, source, destination):
        super().__init__(x, y)
        self.source = source
        self.destination = destination
        
    def transfer(self, item, amount=1):
        if self.source.inventory[item] < amount:
            print(f"Pas assez de {item} à transférer (disponible : {self.source.inventory[item]}).")
            return False

        self.source.inventory[item] -= amount
        self.destination.inventory[item] += amount

        return True