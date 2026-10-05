# Compact Routing in Networks (Thorup-Zwick stretch-3)

An implementation of the **Thorup-Zwick name-dependent compact routing scheme**
([Thorup & Zwick, 2001](https://doi.org/10.1145/378580.378581)). Given a
connected weighted graph standing in for a network of servers, it builds a
*compact* routing database and then routes between any two nodes using only that
database, never the full graph. Every routed path is guaranteed to be at most
**3x** the length of the true shortest path.

The point of a compact scheme is size: each node stores only about `O(sqrt(n) log n)`
entries instead of a full `O(n)` routing table, which is what makes routing
scale to large networks.

## How it works

**Pre-processing** (`PreProcess.py`), run once per graph:

1. **Group A (landmarks).** Sample a set `A` of landmarks, each node included
   independently with probability `1/sqrt(n)`, so `|A|` is about `sqrt(n)` in
   expectation.
2. **All-pairs shortest paths** via `networkx.all_pairs_dijkstra`.
3. **Centroid.** Each node's nearest landmark.
4. **Clusters.** The cluster of `v` is every node `u` that is closer to `v`
   than `u` is to its own nearest landmark.
5. **Labels.** Each node's name carries its nearest landmark and the first hop
   from that landmark toward the node.
6. **Routing charts.** Each node stores the next hop toward every landmark and
   toward every node in its cluster.

**Routing** (`FindPath.py`) uses only labels and routing charts. Depending on
whether the target is a landmark, is in the source's cluster, or neither, the
path either goes direct or detours through the target's nearest landmark. That
detour is what bounds the stretch at 3.

## Files

| File | Role |
| --- | --- |
| `GraphGenerator.py` | Build random (`regular`) or `grid` weighted graphs. |
| `PreProcess.py` | Build the compact routing database. |
| `FindPath.py` | Route between two nodes using labels + routing charts. |
| `HelperMethods.py` | Statistics and Matplotlib visualization. |
| `Main.py` | Command-line demo driver. |
| `test_stretch.py` | Checks paths are valid and stretch stays <= 3. |
| `visualizer.html` | Standalone interactive visualization (no install). |

## Running

```sh
pip install -r requirements.txt

# Defaults: a 6x6 grid, route from 15 to 0, show the plot.
python Main.py

# A 64-node random graph, route from 10 to 3, reproducible:
python Main.py --vertices 64 --graph-type regular --edge-probability 0.08 \
               --source 10 --target 3 --seed 1

# Stats only, no window:
python Main.py --no-plot
```

Run `python Main.py --help` for all options (vertices, edge probability, max
weight, weight distribution, graph type, source, target, seed).

The plot shows the routed path in **red** over the true shortest path in
**green**, with landmarks in orange and the source's cluster shaded. The console
prints group A size, cluster sizes, and the max and average stretch over all
pairs.

## Tests

```sh
python -m pytest        # or: python test_stretch.py
```

Over tens of thousands of routing queries on grids and random graphs, every
path is a valid walk from source to target and no stretch exceeds 3.

## Interactive visualization

Open `visualizer.html` in any browser (no server, no install). Generate a
graph, see landmarks and a cluster highlighted, click a source and target, and
watch the compact route build hop by hop next to the shortest path, with the
live stretch shown.
