"""Correctness checks for the compact routing scheme.

Runs with plain Python (`python test_stretch.py`) or under pytest
(`python -m pytest`). For every ordered pair of vertices it checks that the
routed path is a valid walk from source to target and that its stretch never
exceeds the Thorup-Zwick guarantee of 3.
"""
import random

import networkx as nx

from FindPath import find_path
from GraphGenerator import generate_graph
from PreProcess import pre_process

STRETCH_BOUND = 3.0
EPS = 1e-9

CASES = [
    # (graph_type, vertices, edge_probability, distribution, seed)
    ('grid', 36, 0.05, 'geometric', 0),
    ('grid', 49, 0.05, 'uniform', 1),
    ('regular', 40, 0.10, 'uniform', 2),
    ('regular', 60, 0.08, 'geometric', 3),
    ('regular', 30, 0.20, 'uniform', 4),
]


def _build(graph_type, vertices, edge_probability, distribution, seed):
    random.seed(seed)
    graph = generate_graph(vertices, edge_probability, 10,
                           distribution_type=distribution, graph_type=graph_type)
    return graph, pre_process(graph)


def _path_weight(graph, path):
    return sum(graph[a][b]['weight'] for a, b in zip(path[:-1], path[1:]))


def check_case(graph_type, vertices, edge_probability, distribution, seed):
    graph, pg = _build(graph_type, vertices, edge_probability, distribution, seed)
    worst = 0.0
    for w in graph.nodes():
        for v in graph.nodes():
            if w == v:
                continue
            path = find_path(pg, w, v)
            assert path, f"no path returned for {w}->{v}"
            assert path[0] == w and path[-1] == v, f"path endpoints wrong for {w}->{v}: {path}"
            for a, b in zip(path[:-1], path[1:]):
                assert graph.has_edge(a, b), f"path uses missing edge {a}-{b} for {w}->{v}"
            routed = _path_weight(graph, path)
            shortest = nx.shortest_path_length(graph, w, v, weight='weight')
            stretch = routed / shortest
            worst = max(worst, stretch)
            assert stretch <= STRETCH_BOUND + EPS, f"stretch {stretch} > 3 for {w}->{v}"
    return worst


def test_stretch_within_bound():
    for case in CASES:
        worst = check_case(*case)
        assert worst <= STRETCH_BOUND + EPS


if __name__ == '__main__':
    for case in CASES:
        worst = check_case(*case)
        label = f"{case[0]} n={case[1]}"
        print(f"{label:16} worst stretch = {worst:.3f}  OK")
    print("All cases passed: every routed path is valid and within stretch 3.")
