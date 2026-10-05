import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from FindPath import find_path


def print_graph_information(graph, processed_graph):
    group_A = processed_graph['group_A']
    clusters = processed_graph['clusters']
    paths = processed_graph['paths']

    group_A_size = sum(1 for vertex in group_A if group_A[vertex])
    print("Group A size:", group_A_size)

    avg_cluster_size = sum(len(cluster) for cluster in clusters.values()) / len(clusters)
    print("Average cluster size:", avg_cluster_size)

    max_cluster_size = max(len(cluster) for cluster in clusters.values())
    print("Max cluster size:", max_cluster_size)

    # Stretch over every ordered pair: routed-path weight / shortest-path weight.
    stretches = []
    for w in graph.nodes():
        for v in graph.nodes():
            if w == v:
                continue
            path = find_path(processed_graph, w, v)
            path_weight = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            shortest_path = paths[w][1][v]
            shortest_path_weight = sum(graph[a][b]['weight'] for a, b in zip(shortest_path[:-1], shortest_path[1:]))
            stretches.append(path_weight / shortest_path_weight)

    if stretches:
        print("Max stretch:", max(stretches))
        print("Average stretch:", sum(stretches) / len(stretches))
    else:
        print("No paths found to calculate stretch")


def _layout(graph):
    """Grid coordinates for grid graphs, a spring layout otherwise."""
    n = len(graph)
    side = int(round(n ** 0.5))
    is_grid = side * side == n and graph.number_of_edges() == 2 * side * (side - 1)
    if is_grid:
        return {node: (node % side, side - 1 - node // side) for node in graph.nodes()}
    return nx.spring_layout(graph, seed=42, weight='weight')


def _path_edges(path):
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def _path_weight(graph, path):
    return sum(graph[a][b]['weight'] for a, b in zip(path[:-1], path[1:]))


def visualize_graph(graph, processed_graph):
    """Draw the plain graph with group A (landmarks) highlighted."""
    group_A = processed_graph['group_A']
    pos = _layout(graph)
    landmarks = [node for node in group_A if group_A[node]]

    plt.figure(figsize=(12, 9))
    nx.draw(graph, pos, with_labels=True, node_size=700, font_size=11, font_weight="bold",
            width=2, edge_color="#b0b0b0", node_color="#cfe3ff")
    nx.draw_networkx_nodes(graph, pos, nodelist=landmarks, node_color="#ffb300", node_size=700)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'), font_size=9)
    plt.title("Graph with group A (landmarks in orange)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def visualize_graph_with_paths(graph, processed_graph, path):
    """Draw the routed path (red) against the true shortest path (green).

    Landmarks (group A) are orange, and the source vertex's cluster is shaded.
    """
    group_A = processed_graph['group_A']
    clusters = processed_graph['clusters']
    paths = processed_graph['paths']

    pos = _layout(graph)
    w, v = path[0], path[-1]
    landmarks = [node for node in group_A if group_A[node]]
    cluster_w = clusters.get(w, [])

    routed_weight = _path_weight(graph, path)
    shortest_path = paths[w][1][v]
    shortest_weight = _path_weight(graph, shortest_path)
    stretch = routed_weight / shortest_weight if shortest_weight else 1.0

    plt.figure(figsize=(12, 9))

    # Base graph.
    nx.draw(graph, pos, with_labels=True, node_size=650, font_size=11, font_weight="bold",
            width=1.5, edge_color="#c8c8c8", node_color="#cfe3ff")

    # Shade the source vertex's cluster.
    if cluster_w:
        nx.draw_networkx_nodes(graph, pos, nodelist=cluster_w, node_color="#dcd0ff", node_size=650)
    # Landmarks.
    nx.draw_networkx_nodes(graph, pos, nodelist=landmarks, node_color="#ffb300", node_size=650)
    # Source and target stand out.
    nx.draw_networkx_nodes(graph, pos, nodelist=[w], node_color="#e53935", node_size=820)
    nx.draw_networkx_nodes(graph, pos, nodelist=[v], node_color="#2e7d32", node_size=820)

    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'), font_size=9)

    # Shortest path (green) drawn slightly wider underneath the routed path (red).
    nx.draw_networkx_edges(graph, pos, edgelist=_path_edges(shortest_path),
                           edge_color='#2e7d32', width=6, alpha=0.55)
    nx.draw_networkx_edges(graph, pos, edgelist=_path_edges(path),
                           edge_color='#e53935', width=3)

    legend = [
        plt.Line2D([0], [0], color='#e53935', lw=3, label=f'Routed path  (weight {routed_weight})'),
        plt.Line2D([0], [0], color='#2e7d32', lw=5, alpha=0.55, label=f'Shortest path  (weight {shortest_weight})'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ffb300', markersize=11, label='Group A (landmarks)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#dcd0ff', markersize=11, label=f'Cluster of {w}'),
    ]
    plt.legend(handles=legend, loc='upper right', fontsize=10, framealpha=0.9)
    plt.title(f"Routing {w} -> {v}   stretch = {stretch:.2f}  (guaranteed <= 3)")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
