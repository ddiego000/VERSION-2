from node import Distance

class Path:
    def __init__(self):
        self.nodes = []
        self.real_cost = 0.0

    def add_node(self, node, cost):
        self.nodes.append(node)
        self.real_cost += cost

    def last_node(self):
        return self.nodes[-1] if self.nodes else None

    def contains(self, node):
        return node in self.nodes

    def total_estimated_cost(self, goal):
        if self.last_node() is None:
            return float('inf')
        return self.real_cost + Distance(self.last_node(), goal)

    def copy(self):
        new_path = Path()
        new_path.nodes = self.nodes[:]
        new_path.real_cost = self.real_cost
        return new_path
