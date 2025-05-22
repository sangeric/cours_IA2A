class BaseGraph:
    def __init__(self):
        raise TypeError("Unable to instantiate BaseGraph: must override it.")

    def add_vertex(self, v):
        raise NotImplementedError()

    def add_vertices(self, iterable):
        for v in iterable:
            self.add_vertex(v)

    def remove_vertex(self, v):
        raise NotImplementedError()

    def remove_vertices(self, iterable):
        for v in iterable:
            self.remove_vertex(v)

    def get_vertices(self):
        raise NotImplementedError()

    def has_vertex(self, v):
        raise NotImplementedError()

    def add_edge(self, u, v, weight=1):
        raise NotImplementedError()

    def add_edges(self, dictionary):
        for k in dictionary:
            self.add_edge(*k, dictionary[k])

    def get_edges(self):
        raise NotImplementedError()

    def has_edge(self, u, v):
        raise NotImplementedError()

    def get_weight(self, u, v):
        raise NotImplementedError()

    def neighbors(self, v):
        raise NotImplementedError()