import networkx as nx
from collections import defaultdict
import random
import math


def find_centroids(graph, group_A, paths):
    group_A_true_vertices = []

    for vertex, in_group_A in group_A.items():
        if in_group_A:
            group_A_true_vertices.append(vertex)
    centroids = {}
    for v in graph.nodes():
        if group_A[v]:
            centroids[v] = v
        else:
            shortest_paths_v = paths[v]
            min_dist = math.inf
            for u in group_A_true_vertices:
                dist = shortest_paths_v[0][u]
                if dist < min_dist:
                    min_dist = dist
                    centroid_v = u

            centroids[v] = centroid_v
    return centroids


def compute_clusters(graph, centroids, paths):
    clusters = {}
    for v in graph.nodes():
        centroid_v = centroids[v]
        if centroid_v == v:
            clusters[v] = []
        else:
            cluster_v = [u for u in graph.nodes() if paths[v][0][u] < paths[u][0][centroids[u]] and u != v]
            clusters[v] = cluster_v
    return clusters


def create_labels(graph, centroids, group_A, paths):
    labels = {}
    for v in graph.nodes():
        centroid_v = centroids[v]
        if group_A[v]:
            labels[v] = (v, v, None)
        else:
            shortest_paths_v = paths[centroid_v]
            shortest_path = shortest_paths_v[1][v]
            if len(shortest_path) > 1:
                first_edge = (shortest_path[0], shortest_path[1])
                labels[v] = (v, centroid_v, first_edge)
            else:
                labels[v] = (v, centroid_v, None)

    return labels


def generate_routing_charts(graph, clusters, group_A, paths):
    routing_charts = defaultdict(dict)
    group_A_true_vertices = []
    for vertex, in_group_A in group_A.items():
        if in_group_A:
            group_A_true_vertices.append(vertex)
    for v in graph.nodes():
        routing_chart_v = {}
        for u in group_A_true_vertices:
            if u != v:
                shortest_path_v_u = paths[v][1][u]
                routing_chart_v[u] = (shortest_path_v_u[0], shortest_path_v_u[1])
        for u in clusters[v]:
            if u != v:
                shortest_path_v_u = paths[v][1][u]
                routing_chart_v[u] = (shortest_path_v_u[0], shortest_path_v_u[1])
        routing_charts[v] = routing_chart_v
    return routing_charts


def pre_process(graph):
    n = len(graph)
    group_A = {v: random.random() < 1 / math.sqrt(n) for v in graph.nodes()}
    paths = dict(nx.all_pairs_dijkstra(graph, cutoff=None, weight='weight'))
    centroids = find_centroids(graph, group_A, paths)
    clusters = compute_clusters(graph, centroids, paths)
    routing_charts = generate_routing_charts(graph, clusters, group_A, paths)
    labels = create_labels(graph, centroids, group_A, paths)
    processed_graph = {
        'group_A': group_A,
        'clusters': clusters,
        'centroids': centroids,
        'routing_charts': routing_charts,
        'labels': labels,
        'paths': paths
    }
    return processed_graph
