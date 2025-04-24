import matplotlib.pyplot as plt
from node import Node, Distance
from segment import Segment

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

    def AddNode(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            return True
        return False

    def AddSegment(self, name, nameOrigin, nameDestination):
        origin_node = None
        destination_node = None

        for node in self.nodes:
            if node.name == nameOrigin:
                origin_node = node
            if node.name == nameDestination:
                destination_node = node

        if origin_node and destination_node and origin_node != destination_node:
            segment = Segment(name, origin_node, destination_node)
            self.segments.append(segment)

            if destination_node not in origin_node.neighbors:
                origin_node.add_neighbor(destination_node)
            if origin_node not in destination_node.neighbors:
                destination_node.add_neighbor(origin_node)

            return True
        return False

    def GetClosest(self, x, y):
        return min(self.nodes, key=lambda node: Distance(node, Node("temp", x, y)))

    def get_neighbors(self, node):
        return node.neighbors if hasattr(node, 'neighbors') else []

    def get_distance(self, node1, node2):
        for segment in self.segments:
            if (segment.origin == node1 and segment.destination == node2) or \
               (segment.origin == node2 and segment.destination == node1):
                return segment.cost
        return float('inf')

def LoadGraphFromFile(filename):
    G = Graph()
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    try:
                        node_name = parts[0]
                        x = float(parts[1])
                        y = float(parts[2])
                        G.AddNode(Node(node_name, x, y))
                    except ValueError:
                        continue
                elif len(parts) == 3 and parts[0] != '':
                    segment_name = parts[0]
                    origin = parts[1]
                    destination = parts[2]
                    G.AddSegment(segment_name, origin, destination)
    except FileNotFoundError:
        print(f"Error: El archivo {filename} no se encuentra.")
    return G

def CreateGraph_1():
    g = Graph()
    g.AddNode(Node("A", 0, 0))
    g.AddNode(Node("B", 1, 2))
    g.AddNode(Node("C", 2, 0))
    g.AddSegment("S1", "A", "B")
    g.AddSegment("S2", "B", "C")
    g.AddSegment("S3", "C", "A")
    return g

def CreateGraph_2():
    g = Graph()
    g.AddNode(Node("X", 3, 3))
    g.AddNode(Node("Y", 5, 7))
    g.AddNode(Node("Z", 8, 4))
    g.AddSegment("S4", "X", "Y")
    g.AddSegment("S5", "Y", "Z")
    return g
