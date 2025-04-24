from path import Path
import heapq

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
    queue = []
    initial_path = Path()
    initial_path.add_node(origin, 0)
    heapq.heappush(queue, (initial_path.total_estimated_cost(destination), initial_path))

    while queue:
        _, path = heapq.heappop(queue)
        last = path.last_node()

        if last == destination:
            return path

        for neighbor in network.get_neighbors(last):
            if path.contains(neighbor):
                continue
            new_path = path.copy()
            cost = network.get_distance(last, neighbor)
            new_path.add_node(neighbor, cost)
            heapq.heappush(queue, (new_path.total_estimated_cost(destination), new_path))

    return None
