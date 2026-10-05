"""Thorup-Zwick stretch-3, name-dependent compact routing: demo driver.

Run with defaults:

    python Main.py

Or pass parameters, e.g. a 64-node random graph routing from 10 to 3:

    python Main.py --vertices 64 --graph-type regular --edge-probability 0.08 \
                   --source 10 --target 3 --seed 1

Use --no-plot to skip the Matplotlib window (prints stats only).
"""
import argparse
import random

from FindPath import find_path
from GraphGenerator import generate_graph
from HelperMethods import print_graph_information, visualize_graph, visualize_graph_with_paths
from PreProcess import pre_process


def parse_args():
    parser = argparse.ArgumentParser(description="Thorup-Zwick compact routing demo.")
    parser.add_argument('--vertices', type=int, default=36, help='number of vertices (default: 36)')
    parser.add_argument('--edge-probability', type=float, default=0.05,
                        help='edge probability for regular graphs (ignored for grids; default: 0.05)')
    parser.add_argument('--max-weight', type=int, default=10, help='maximum edge weight (default: 10)')
    parser.add_argument('--distribution', choices=['uniform', 'geometric'], default='geometric',
                        help='edge-weight distribution (default: geometric)')
    parser.add_argument('--graph-type', choices=['grid', 'regular'], default='grid',
                        help='graph structure (default: grid)')
    parser.add_argument('--source', type=int, default=15, help='source vertex w (default: 15)')
    parser.add_argument('--target', type=int, default=0, help='target vertex v (default: 0)')
    parser.add_argument('--seed', type=int, default=None, help='random seed for reproducible graphs')
    parser.add_argument('--no-plot', action='store_true', help='skip the Matplotlib visualization')
    parser.add_argument('--plot-graph-only', action='store_true',
                        help='also show the plain graph before the routed one')
    return parser.parse_args()


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    # 1. Generate a graph from the chosen parameters.
    graph = generate_graph(args.vertices, args.edge_probability, args.max_weight,
                           distribution_type=args.distribution, graph_type=args.graph_type)

    # 2. Pre-process it into the compact routing database.
    processed_graph = pre_process(graph)

    # 3. Print graph and scheme statistics (group A size, cluster sizes, stretch).
    print_graph_information(graph, processed_graph)

    # 4. Route from the source to the target using only labels and routing charts.
    w, v = args.source, args.target
    if w not in graph or v not in graph:
        raise SystemExit(f"source and target must be vertices in 0..{len(graph) - 1}")
    path = find_path(processed_graph, w, v)
    print(f"Path from {w} to {v}: {path}")

    # 5. Visualize: the routed path (red) against the true shortest path (green).
    if not args.no_plot:
        if args.plot_graph_only:
            visualize_graph(graph, processed_graph)
        visualize_graph_with_paths(graph, processed_graph, path)


if __name__ == '__main__':
    main()
