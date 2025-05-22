from .graph_base import BaseGraph

class SetGraph(BaseGraph):
    def __init__(self):
        self.vertices = set()
        self.edges = dict()

    def add_vertex(self, v):
        self.vertices.add(v)

    def get_vertices(self):
        return self.vertices

    def has_vertex(self, v):
        return v in self.vertices

    def add_edge(self, u, v, weight=1):
        if u in self.vertices and v in self.vertices:
            self.edges[(u, v)] = weight

    def get_edges(self):
        return self.edges

    def has_edge(self, u, v):
        return (u, v) in self.edges

    def get_weight(self, u, v):
        return self.edges.get((u, v), None)

    def neighbors(self, v):
        return [b for (a, b) in self.edges if a == v]