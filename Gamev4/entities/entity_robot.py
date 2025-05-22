import heapq
from .entity import Entity

class EntityRobot(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.inventory_capacity = 10000 
        self.inventory = {
            "wood": 0,
            "water": 0,
            "rock": 0,
            "coal": 0
        }
        
    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        

    def dijkstra(self, graph, goal):
        frontier = [(0, (self.x, self.y))]
        came_from = {(self.x, self.y): None}
        cost_so_far = {(self.x, self.y): 0}

        while frontier:
            current_cost, current = heapq.heappop(frontier)
            if current == goal:
                break
            for neighbor in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.get_weight(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbor))
                    came_from[neighbor] = current
        path = []
        if goal in came_from:
            curr = goal
            while curr:
                path.append(curr)
                curr = came_from[curr]
            path.reverse()
        return path
    
    def get_total_inventory(self):
        return sum(self.inventory.values())

    def collect_resources(self, game_map):
        max_to_collect = 10 
        collected = 0

        remaining_capacity = self.inventory_capacity - self.get_total_inventory()
        if remaining_capacity <= 0:
            return

        x, y = self.getPos()
        neighbors = game_map.get_neighbors(x, y)

        for nx, ny in neighbors:
            if collected >= max_to_collect:
                break  

            tile = game_map.get_tile(y=ny, x=nx)
            resources = tile.getResources()

            for resource, qty in resources.items():
                if qty > 0 and remaining_capacity > 0:
                    to_collect = min(qty, remaining_capacity, max_to_collect - collected)
                    if to_collect <= 0:
                        continue
                    self.inventory[resource] += to_collect
                    tile.resources[resource] -= to_collect
                    collected += to_collect
                    remaining_capacity -= to_collect

                    if collected >= max_to_collect:
                        break 

    def collect_from_tile(self, tile, max_to_collect=10):
        collected = 0
        remaining_capacity = self.inventory_capacity - self.get_total_inventory()
        if remaining_capacity <= 0:
            return 0

        resources = tile.getResources()

        for res, qty in resources.items():
            if qty > 0 and remaining_capacity > 0:
                to_collect = min(qty, remaining_capacity, max_to_collect - collected)
                if to_collect <= 0:
                    continue
                self.inventory[res] += to_collect
                tile.resources[res] -= to_collect
                collected += to_collect
                remaining_capacity -= to_collect

            if collected >= max_to_collect:
                break

        return collected



        
    