import networkx as nx


def validateMatrix(matrix, ponderated):
    errors = []
    n = len(matrix)

    if any(len(row) != n for row in matrix):
        return ["La matriz debe ser cuadrada."]

    for i in range(n):
        for j in range(n):
            if not isinstance(matrix[i][j], (int, float)):
                errors.append(f"El valor en ({i + 1}, {j + 1}) no es numérico.")
            elif not ponderated and matrix[i][j] not in (0, 1):
                errors.append(f"El valor en ({i + 1}, {j + 1}) debe ser 0 o 1.")

    if all(value == 0 for row in matrix for value in row):
        errors.append("El grafo no tiene aristas.")

    return errors


def isDirected(matrix):
    n = len(matrix)
    return any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n))


def buildGraph(matrix):
    n = len(matrix)
    graph = nx.DiGraph() if isDirected(matrix) else nx.Graph()
    graph.add_nodes_from(range(1, n + 1))

    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                graph.add_edge(i + 1, j + 1, weight=matrix[i][j])

    return graph


def getMathRepresentation(graph, ponderated):
    nodes = ", ".join(str(node) for node in graph.nodes)

    edges = []
    for u, v, weight in graph.edges(data="weight"):
        edge = f"{u},{v},{weight:g}" if ponderated else f"{u},{v}"
        edges.append(f"({edge})" if graph.is_directed() else "\\{" + edge + "\\}")

    vertices = "V = \\{" + nodes + "\\}"
    edgeSet = "E = \\{" + ", ".join(edges) + "\\}"
    return vertices, edgeSet


def getAdjacents(graph):
    return {node: list(graph.neighbors(node)) for node in graph.nodes}


def findPath(graph, origin, destination, path=None):
    path = (path or []) + [origin]
    if origin == destination:
        return path

    for neighbor in graph.neighbors(origin):
        if neighbor not in path:
            result = findPath(graph, neighbor, destination, path)
            if result:
                return result
    return None


def findCycle(graph):
    minLength = 2 if graph.is_directed() else 3
    for start in graph.nodes:
        cycle = searchCycle(graph, start, [start], minLength)
        if cycle:
            return cycle
    return None


def searchCycle(graph, start, path, minLength):
    for neighbor in graph.neighbors(path[-1]):
        isLoop = len(path) == 1
        if neighbor == start and (isLoop or len(path) >= minLength):
            return path + [start]
        if neighbor not in path:
            cycle = searchCycle(graph, start, path + [neighbor], minLength)
            if cycle:
                return cycle
    return None
