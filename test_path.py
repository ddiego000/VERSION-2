from path import Path
from node import Node


def test_path_functions():
    a = Node("A", 0, 0)
    b = Node("B", 3, 4)
    path = Path()

    assert not path.contains(a)
    path.add_node(a, 0)
    assert path.contains(a)

    path.add_node(b, 5)
    assert path.real_cost == 5
    assert path.last_node() == b

    estimate = path.total_estimated_cost(Node("F", 10, 10))
    print("All path tests passed.")