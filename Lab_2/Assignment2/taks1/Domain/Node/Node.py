class Node:

    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def set_heuristics(self, start_node, end_node):
        self.g = abs(self.position[0] - start_node.position[0]) + abs(self.position[1] - start_node.position[1])
        self.h = abs(self.position[0] - end_node.position[0]) + abs(self.position[1] - end_node.position[1])
        self.f = self.g + self.h
