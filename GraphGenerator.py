import networkx as nx
import numpy as np
import random


def generate_graph(vertices_num, edge_probability, max_weight, distribution_type='uniform', graph_type='regular'):
    """Generate a connected, weighted graph.

    graph_type='regular' builds a random graph where each possible edge exists
    with probability edge_probability, then adds the few edges needed to make it
    connected. graph_type='grid' builds a square grid (edge_probability is
    ignored, matching the assignment spec).
    """
    if graph_type == 'grid':
        return _generate_grid(vertices_num, max_weight, distribution_type)
    if graph_type == 'regular':
        return _generate_regular(vertices_num, edge_probability, max_weight, distribution_type)
    raise ValueError("Invalid graph_type. Supported types are 'regular' and 'grid'.")


def _generate_regular(vertices_num, edge_probability, max_weight, distribution_type):
    G = nx.Graph()
    G.add_nodes_from(range(vertices_num))

    # Add each possible edge with probability edge_probability.
    for u in range(vertices_num):
        for v in range(u + 1, vertices_num):
            if random.random() < edge_probability:
                G.add_edge(u, v, weight=generate_weight(max_weight, distribution_type))

    # Connect the graph by linking one node from each component to the next.
    if not nx.is_connected(G):
        components = list(nx.connected_components(G))
        for i in range(1, len(components)):
            node_prev = next(iter(components[i - 1]))
            node_curr = next(iter(components[i]))
            G.add_edge(node_prev, node_curr, weight=generate_weight(max_weight, distribution_type))

    return G


def _generate_grid(vertices_num, max_weight, distribution_type):
    # Largest square grid that fits in vertices_num nodes (e.g. 36 -> 6x6).
    side_length = int(np.sqrt(vertices_num))
    G = nx.grid_2d_graph(side_length, side_length)

    for u, v in G.edges():
        G[u][v]['weight'] = generate_weight(max_weight, distribution_type)

    # Rename (i, j) grid coordinates to single integers so the rest of the
    # pipeline can treat every graph the same way.
    mapping = {(i, j): i * side_length + j for i, j in G.nodes()}
    return nx.relabel_nodes(G, mapping)


def generate_weight(max_weight, distribution_type):
    if distribution_type == 'uniform':
        return random.randint(1, max_weight)
    elif distribution_type == 'geometric':
        # Geometric distribution: weight = 2^i with probability 1/2^(i+1),
        # capped at max_weight.
        i = 0
        while random.random() < 0.5:
            i += 1
        return min(2 ** i, max_weight)
    else:
        raise ValueError("Invalid distribution_type. Supported types are 'uniform' and 'geometric'.")
