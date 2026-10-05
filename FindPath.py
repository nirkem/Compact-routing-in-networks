def find_path(processed_graph, w, v):
    group_A = processed_graph['group_A']
    clusters = processed_graph['clusters']
    centroids = processed_graph['centroids']
    routing_charts = processed_graph['routing_charts']
    labels = processed_graph['labels']

    if group_A[v]:
        # If v belongs to group_A, use w's routing chart to find the path to v
        next_edge = routing_charts[w].get(v)
        path = [w, next_edge[1]]
        while path[-1] != v:
            next_edge = routing_charts[path[-1]].get(v)
            path.append(next_edge[1])
        return path


    elif v in clusters[w]:
        # If v belongs to the cluster of w, use w's routing chart to find the path to v
        next_edge = routing_charts[w].get(v)
        path = [w, next_edge[1]]
        while path[-1] != v:
            next_edge = routing_charts[path[-1]].get(v)
            path.append(next_edge[1])
        return path


    elif centroids[w] != v:
        # If w is not the centroid of v, find the centroid of v using label[v] and move towards it
        centroid_v = labels[v][1]
        if w == centroid_v:
            path = [w]
        else:
            next_edge = routing_charts[w].get(centroid_v)
            path = [w, next_edge[1]]
        if path[-1] == v:
            return path
        while path[-1] != centroid_v:
            next_edge = routing_charts[path[-1]].get(centroid_v)
            path.append(next_edge[1])
        # Once we reach the centroid, use labels[v][2] to find the first edge on the shortest path to v
        first_edge = labels[v][2]
        path.append(first_edge[1])
        # Continue along the shortest path until we reach v
        while path[-1] != v:
            next_edge = routing_charts[path[-1]].get(v)
            path.append(next_edge[1])
        return path


    else:
        # If w is the centroid of v, move towards v using label[v]
        next_edge = labels[v][2]
        if next_edge:
            path = [w, next_edge[1]]
            while path[-1] != v:
                next_edge = routing_charts[path[-1]].get(v)
                if next_edge:
                    path.append(next_edge[1])
            return path
