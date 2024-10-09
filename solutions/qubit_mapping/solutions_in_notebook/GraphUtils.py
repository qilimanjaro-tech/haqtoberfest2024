from os import remove
from typing import Dict, List, Tuple


def get_highest_degree_node(graph: Dict[int, List[int]]) -> int:
    # if graph is empty, return -1
    max_node = -1
    max_degree = 0
    for node, connections in graph.items():
        degree = len(connections)
        if degree > max_degree:
            max_degree = degree
            max_node = node

    return max_node


def remove_edge(graph: Dict[int, List[int]], edge: Tuple[int, int]) -> Dict[int, List[int]]:
    new_graph = graph.copy()
    new_graph[edge[0]].remove(edge[1])
    if not new_graph[edge[0]]:
        del new_graph[edge[0]]

    new_graph[edge[1]].remove(edge[0])
    if not new_graph[edge[1]]:
        del new_graph[edge[1]]

    return new_graph


def get_max_degree_neighbor(graph: Dict[int, List[int]], node: int) -> int:
    max_degree_neighbor = graph[node][0]
    for neighbor in graph[node]:
        if len(graph[neighbor]) > len(graph[max_degree_neighbor]):
            max_degree_neighbor = neighbor
    return max_degree_neighbor


def get_subgraphs(graph: Dict[int, List[int]]) -> List[int]:
    new_graph = graph.copy()
    subgraphs: List[int] = []

    starting_node = get_highest_degree_node(new_graph)
    while starting_node != -1:
        subgraph = get_next_subgraph(new_graph, starting_node)
        subgraphs.extend(subgraph)
        starting_node = get_highest_degree_node(new_graph)

    return subgraphs


def get_next_subgraph(remaining_graph: Dict[int, List[int]], node: int) -> List[int]:
    current_node = node
    subgraph = [current_node]
    neighbor_amount = len(remaining_graph[current_node])

    while neighbor_amount > 0 and current_node not in subgraph:
        max_degree_neighbor = get_max_degree_neighbor(remaining_graph, current_node)
        subgraph.append(max_degree_neighbor)
        remaining_graph = remove_edge(remaining_graph, (current_node, max_degree_neighbor))
        current_node = max_degree_neighbor
        neighbor_amount = len(remaining_graph[current_node])

    del remaining_graph[current_node]
    return subgraph


def is_pair_present(graph: Dict[int, List[int]], node1: int, node2: int) -> bool:
    return (node1 in graph.keys() and node2 in graph[node1]) and (node2 in graph.keys() and node1 in graph[node2])


def get_node_edges(graph: Dict[int, List[int]], node: int) -> int:
    if node in graph.keys():
        return len(graph[node])
    else:
        return 0


def add_to_graph(graph: Dict[int, List[int]], node1: int, node2: int) -> Dict[int, List[int]]:
    if node1 in graph.keys():
        graph[node1].append(node2)
    else:
        graph[node1] = [node2]

    if node2 in graph.keys():
        graph[node2].append(node1)
    else:
        graph[node2] = [node1]

    return graph
