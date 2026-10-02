INF = float("inf")


def buildPath(previous, origin, destination):
    path = [destination]
    while path[-1] != origin:
        path.append(previous[path[-1]])
    return path[::-1]


def dijkstra(graph, origin, destination):
    if any(weight < 0 for _, _, weight in graph.edges(data="weight")):
        raise ValueError("Dijkstra no admite pesos negativos.")

    distances = {node: INF for node in graph.nodes}
    distances[origin] = 0
    previous = {}
    pending = set(graph.nodes)

    while pending:
        current = min(pending, key=lambda node: distances[node])
        if distances[current] == INF:
            break
        pending.remove(current)

        for neighbor, data in graph[current].items():
            newDistance = distances[current] + data["weight"]
            if newDistance < distances[neighbor]:
                distances[neighbor] = newDistance
                previous[neighbor] = current

    if distances[destination] == INF:
        return None, INF
    return buildPath(previous, origin, destination), distances[destination]


def relaxEdges(graph, distances, previous):
    changed = False
    for u in graph.nodes:
        for v, data in graph[u].items():
            if distances[u] + data["weight"] < distances[v]:
                distances[v] = distances[u] + data["weight"]
                previous[v] = u
                changed = True
    return changed


def bellmanFord(graph, origin, destination):
    distances = {node: INF for node in graph.nodes}
    distances[origin] = 0
    previous = {}

    for _ in range(len(graph.nodes) - 1):
        relaxEdges(graph, distances, previous)

    if relaxEdges(graph, distances, previous):
        raise ValueError("El grafo tiene un ciclo de peso negativo.")

    if distances[destination] == INF:
        return None, INF
    return buildPath(previous, origin, destination), distances[destination]
