from path import Path

def reachable_nodes(network, start_node):
    visited = set()
    to_visit = [start_node]

    while to_visit:
        current = to_visit.pop()
        if current not in visited:
            visited.add(current)
            neighbors = network.get_neighbors(current)
            to_visit.extend([n for n in neighbors if n not in visited])

    return visited

def FindShortestPath(network, origin, destination):
    current_paths = []

    initial_path = Path()
    initial_path.add_node(origin, 0)
    current_paths.append(initial_path)

    while current_paths:
        current_paths.sort(key=lambda p: p.total_estimated_cost(destination))
        path = current_paths.pop(0)
        last = path.last_node()

        if last == destination:
            return path

        for neighbor in network.get_neighbors(last):
            if path.contains(neighbor):
                continue
            new_path = path.copy()
            cost = network.get_distance(last, neighbor)
            new_path.add_node(neighbor, cost)
            current_paths.append(new_path)

    return None