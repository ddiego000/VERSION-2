import math

class Node:
    def __init__(self, name: str, x: float, y: float):
        """Initializes a Node with a name, coordinates (x, y), and an empty list of neighbors."""
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []  # List to store neighboring nodes

    def add_neighbor(self, neighbor):
        """Adds a neighboring node if it's not already in the list."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def __repr__(self):
        return f"Node({self.name}, {self.x}, {self.y}, Neighbors: {[n.name for n in self.neighbors]})"

def AddNeighbor(n1, n2):
    """Adds node n2 to n1's list of neighbors. Returns False if already present, otherwise True."""
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1, n2):
    """Returns the Euclidean distance between two nodes."""
    return math.sqrt((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2)
