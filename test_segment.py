from node import Node
from segment import Segment
n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 8)

s1 = Segment("Segment1", n1, n2)
s2 = Segment("Segment2", n2, n3)

print(s1)
print(s2)