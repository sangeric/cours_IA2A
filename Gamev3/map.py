import random
from tiles import TilePlains, TileForest, TileWater, TileSand, TileMountain


class Map:
    
    TILE_TYPES = [TilePlains, TileForest, TileWater, TileSand, TileMountain]

    
    def __init__(self, width, height):
        self.width = width
        self.height = height 
        self.grid = {}
        
        self.generate_map()
    
    def generate_map(self):
        for q in range(self.width):
            for r in range(self.height):
                TileType = random.choice(self.TILE_TYPES)
                self.grid[(q,r)] = TileType(q,r)
                
    def get_tile(self, q, r):
        return self.grid.get((q, r), None)
    
    def display(self):
        for r in range(self.height):
            line = " " * (r % 2)
            for q in range(self.width):
                tile = self.get_tile(q, r)
                if tile:
                    line += tile.name[0] + " "
                else:
                    line += ". "
            print(line)

