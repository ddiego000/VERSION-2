from network import FindShortestPath
from network import create_test_network

def test_shortest_path():
    N = create_test_network()
    origin = N.get_node("A")
    destination = N.get_node("F")
    path = FindShortestPath(N, origin, destination)

    if path:
        print("Shortest path from A to F:", [n.name for n in path.nodes])
        print("Cost:", path.real_cost)
    else:
        print("No path found")