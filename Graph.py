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

            # Solo agregar destino a vecinos de origen (dirección)
            if destination_node not in origin_node.neighbors:
                origin_node.add_neighbor(destination_node)

            # No agregar origen a vecinos de destino (no bidireccional)
            # if origin_node not in destination_node.neighbors:
            #     destination_node.add_neighbor(origin_node)

            return True
        return False

    def GetClosest(self, x, y):
        return min(self.nodes, key=lambda node: Distance(node, Node("temp", x, y)))

    def get_neighbors(self, node):
        # Ahora vecinos solo son los accesibles en dirección de segmentos
        return node.neighbors if hasattr(node, 'neighbors') else []

    def get_distance(self, node1, node2):
        # Solo si hay un segmento de node1 a node2 (dirección)
        for segment in self.segments:
            if segment.origin == node1 and segment.destination == node2:
                return segment.cost
        return float('inf')


def CreateGraph_1():
    g = Graph()

    # Nodos
    g.AddNode(Node("A", 1, 20))
    g.AddNode(Node("B", 8, 17))
    g.AddNode(Node("C", 15, 20))
    g.AddNode(Node("D", 18, 15))
    g.AddNode(Node("E", 2, 4))
    g.AddNode(Node("F", 6, 5))
    g.AddNode(Node("G", 12, 12))
    g.AddNode(Node("H", 10, 3))
    g.AddNode(Node("I", 19, 1))
    g.AddNode(Node("J", 13, 5))
    g.AddNode(Node("K", 3, 15))
    g.AddNode(Node("L", 4, 10))

    # Segmentos originales
    g.AddSegment("AB", "A", "B")
    g.AddSegment("AE", "A", "E")
    g.AddSegment("AK", "A", "K")
    g.AddSegment("BA", "B", "A")
    g.AddSegment("BC", "B", "C")
    g.AddSegment("BF", "B", "F")

    # Segmentos adicionales
    g.AddSegment("BK", "B", "K")
    g.AddSegment("BG", "B", "G")
    g.AddSegment("CD", "C", "D")
    g.AddSegment("CG", "C", "G")
    g.AddSegment("DG", "D", "G")
    g.AddSegment("DH", "D", "H")
    g.AddSegment("DI", "D", "I")
    g.AddSegment("EF", "E", "F")
    g.AddSegment("FL", "F", "L")
    g.AddSegment("GB", "G", "B")
    g.AddSegment("GF", "G", "F")
    g.AddSegment("GH", "G", "H")
    g.AddSegment("ID", "I", "D")
    g.AddSegment("IJ", "I", "J")
    g.AddSegment("JI", "J", "I")
    g.AddSegment("KA", "K", "A")
    g.AddSegment("KL", "K", "L")
    g.AddSegment("LK", "L", "K")
    g.AddSegment("LF", "L", "F")

    return g


def CreateGraph_2():
    g = Graph()
    # Nodos (con coordenadas organizadas en forma de diamante expandido)
    g.AddNode(Node("A", 10, 18))
    g.AddNode(Node("B", 5, 15))
    g.AddNode(Node("C", 15, 15))
    g.AddNode(Node("D", 2, 10))
    g.AddNode(Node("E", 8, 10))
    g.AddNode(Node("F", 12, 10))
    g.AddNode(Node("G", 18, 10))
    g.AddNode(Node("H", 5, 5))
    g.AddNode(Node("I", 10, 5))
    g.AddNode(Node("J", 15, 5))
    g.AddNode(Node("K", 8, 1))
    g.AddNode(Node("L", 12, 1))

    # Conexiones superiores
    g.AddSegment("AB", "A", "B")
    g.AddSegment("AC", "A", "C")

    # Conexiones intermedias
    g.AddSegment("BD", "B", "D")
    g.AddSegment("BE", "B", "E")
    g.AddSegment("CE", "C", "E")
    g.AddSegment("CF", "C", "F")
    g.AddSegment("CG", "C", "G")

    # Cruce central
    g.AddSegment("EF", "E", "F")

    # Conexiones inferiores
    g.AddSegment("DH", "D", "H")
    g.AddSegment("EH", "E", "H")
    g.AddSegment("EI", "E", "I")
    g.AddSegment("FI", "F", "I")
    g.AddSegment("FJ", "F", "J")
    g.AddSegment("GJ", "G", "J")

    # Base del grafo
    g.AddSegment("HK", "H", "K")
    g.AddSegment("IK", "I", "K")
    g.AddSegment("IL", "I", "L")
    g.AddSegment("JL", "J", "L")

    return g


def LoadGraphFromFile(filename):
    g = Graph()
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                name, p1, p2 = parts
                try:
                    # Intentamos interpretar p1 y p2 como coordenadas numéricas para nodo
                    x = float(p1)
                    y = float(p2)
                    node = Node(name, x, y)
                    g.AddNode(node)
                except ValueError:
                    # No son números, así que asumimos segmento
                    g.AddSegment(name, p1, p2)
    return g
