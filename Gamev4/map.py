import random
import heapq
from tiles import Tile, TilePlains, TileForest, TileWater, TileSand, TileMountain
from graph import SetGraph

class Map:
    def __init__(self, width=20, height=15, size=20):
        self.width = width
        self.height = height 
        self.size = size
        self.grid = []

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getSize(self):
        return self.size
    
    def getGrid(self):
        return self.grid
    
    def get_tile(self, x, y):
        return self.grid[x][y]
        
    TILE_TYPES = [TilePlains, TileForest, TileWater, TileSand, TileMountain]
    COLORS = {
        "-": (50, 50, 50),
        1: (34, 139, 34),       #forest
        2: (139, 137, 137),     #mountain
        3: (0, 191, 255),       #water
        4: (237, 201, 175),     #sand
        5: (124, 252, 0)        #plains
    }
    COSTS = {
        "-": float('inf'),
        "forest": 2,
        "mountain": float('inf'),  # rend inaccessible
        "water": float('inf'),     # rend inaccessible
        "sand": 3,
        "plains": 1
    }
    
    
    def generate_map(self):
        for y in range(self.height):
            line = []
            for x in range(self.width):
                if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
                    line.append(Tile(y,x))
                else:
                    TileType = random.choice(self.TILE_TYPES)
                    line.append(TileType(y,x))
            self.grid.append(line)
            
    def get_neighbors(self, x, y):
        if x % 2 == 0:
            directions = [(+1, 0), (+1, -1), (0, -1), (0, +1), (-1, 0), (-1, -1)]
        else:
            directions = [(+1, 0), (+1, +1), (0, -1), (0, +1), (-1, 0), (-1, +1)]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
                
    def build_graph(self):
        graph = SetGraph()
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile.getName() != "-" and getattr(tile, "walkable", False):
                    graph.add_vertex((x, y))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile.getName() == "-" or not getattr(tile, "walkable", False):
                    continue
                for nx, ny in self.get_neighbors(x, y):
                    neighbor_tile = self.grid[ny][nx]
                    if neighbor_tile.getName() != "-" and getattr(neighbor_tile, "walkable", False):
                        poids = self.COSTS.get(neighbor_tile.getName(), float('inf'))
                        graph.add_edge((x, y), (nx, ny), poids)
        return graph
    
    
        


