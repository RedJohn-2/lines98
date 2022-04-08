import collections


class Graph:

    def __init__(self, vertices):
        self._vertices = vertices

        self._adj_lists = collections.defaultdict(list)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: int):
        self._vertices = vertices

    @property
    def adj_lists(self):
        return self._adj_lists

    def add_edge(self, u: tuple, v: tuple):
        self.adj_lists[u].append(v)
        self.adj_lists[v].append(u)

    def remove_edge(self, u: tuple, v: tuple):
        self.adj_lists[u].remove(v)
        self.adj_lists[v].remove(u)
