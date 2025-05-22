import heapq
from .entity import Entity

class EntityRobot(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.inventory_capacity = 100 
        
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
        
    