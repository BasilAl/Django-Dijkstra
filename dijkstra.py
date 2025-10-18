from __future__ import annotations

import heapq
from typing import Any, Dict

from graph_dijkstra import Graph
from helpers import graph_loader


def dijkstra(
    graph: Graph, start: str, end: str, optimise: str = "cost"
) -> Dict[str, Any]:
    """
    Dijkstra's algorithm to find the shortest path and costs.
    :param graph: The graph to search.
    :param start: The starting node name.
    :param end: The destination node name.
    :param optimise: The attribute to optimize ('cost' or 'time').
    :return: A dictionary with the path, total optimized cost, and alternative cost.
    """
    if optimise not in {"cost", "time"}:
        raise ValueError(
            f"Invalid optimization attribute: {optimise}. Must be 'cost' or 'time'."
        )

    for node in graph.nodes.values():
        node.distance = float("inf")
        node.previous = None
    start_node = graph.nodes[start]
    start_node.distance = 0
    # Χωρίς heapq έπαιρνε αρκετά παραπάνω χρόνο
    pq = [(0, start_node)]  # Priority queue: (distance, node)
    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > current_node.distance:
            continue
        for vertex in graph.vertices:
            if vertex.source == current_node:
                neighbor = vertex.destination
                weight = getattr(vertex, optimise)
                new_distance = current_distance + weight
                if new_distance < neighbor.distance:
                    neighbor.distance = new_distance
                    neighbor.previous = current_node
                    heapq.heappush(pq, (new_distance, neighbor))

    path = []
    # mode_of_transportation = []
    current_node = graph.nodes[end]
    total_cost = 0
    total_time = 0
    while current_node:
        if current_node.previous:
            for vertex in graph.vertices:
                if (
                    vertex.source == current_node.previous
                    and vertex.destination == current_node
                ):
                    total_cost += vertex.cost
                    total_time += vertex.time
                    path.append([current_node, f" by {vertex.mode} to"])
                    break
        else:
            path.append([current_node, ""])
        current_node = current_node.previous

    path_string = "".join(f"{node[1]} {node[0].name}" for node in path[::-1]).strip()
    result = {
        "path": path[::-1],
        "path_string": path_string,
        # "mode": mode_of_transportation[::-1],
        "cost": total_cost,
        "time": total_time,
        "optimised_for": optimise,
    }
    return result


if __name__ == "__main__":
    # Για να το τρέξετε αλλάξτε τις παρκάτω τιμές κατάλληλα.
    FILE = "routes.csv"  # "routes.csv" default
    MODE = "cost"  #  "cost" | "time"
    START = "Amsterdam"
    FINISH = "Berlin"
    graph = graph_loader(file=FILE)

    results = dijkstra(graph, START, FINISH, optimise=MODE)

    print(f"Optimising route from {START} to {FINISH} minimising {MODE}...")
    print("Optimal path:")
    print(f"{results['path_string']}")
    print(f"Total cost: {results['cost']}")
    print(f"Total time: {results['time']}")
