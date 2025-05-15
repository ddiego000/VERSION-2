from node import Distance
from node import Node
class Segment:
    def __init__(self, name, origin, destination) :
        """Constructor de la clase Segment"""
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)
    def __repr__(self):
        """Metodo para representar el objeto como string"""
        return f"Segment({self.name}, Origin: {self.origin.name}, Destination: {self.destination.name}, Cost: {self.cost})"
