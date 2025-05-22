from .entity import Entity

class EntityFactory(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        #producible_items = ["plank", "stone", "brick"]
        self.dependencies = ["sawmill", "mine"] 
    
    def produce(self, item):
        if item in self.producible_items:
            self.inventory[item] = self.inventory.get(item, 0) + 1
    
    def can_build_factory(game_map, pos):
        x, y = pos
        neighbors = game_map.get_neighbors(x, y)
        required_types = {"EntityMine", "EntitySawmil"}
        found_types = set()

        for nx, ny in neighbors:
            tile = game_map.get_tile(ny, nx)
            building = tile.getBuilding()
            if building:
                found_types.add(building.__class__.__name__)
        
        return required_types.issubset(found_types)

        