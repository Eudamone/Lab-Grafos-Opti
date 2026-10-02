import streamlit as st
import widgets as wd
import graphLogic as gl
import algorithms as al

st.set_page_config(
    page_title="Lab Grafos",
    layout="wide"
)

st.title("Laboratorio Grafos")

graphType = st.radio("Tipo de grafo", ["No ponderado", "Ponderado"], horizontal=True)
ponderated = graphType == "Ponderado"
n = st.number_input("Cantidad de nodos", min_value=2, max_value=10, value=5, step=1)

matrix = wd.entryPonderated(n) if ponderated else wd.entryNotPonderated(n)

errors = gl.validateMatrix(matrix, ponderated)
if errors:
    for error in errors:
        st.error(error)
    st.stop()

graph = gl.buildGraph(matrix)
st.info("Grafo dirigido" if graph.is_directed() else "Grafo no dirigido")

tabGraph, tabConcepts, tabShortest = st.tabs(["Grafo", "Conceptos", "Ruta más corta"])

with tabGraph:
    vertices, edges = gl.getMathRepresentation(graph, ponderated)
    st.latex("G = (V, E)")
    st.latex(vertices)
    st.latex(edges)
    wd.drawGraph(graph, ponderated)

with tabConcepts:
    st.subheader("Nodos adyacentes")
    for node, neighbors in gl.getAdjacents(graph).items():
        st.write(f"Nodo {node}: {neighbors if neighbors else 'ninguno'}")

    st.subheader("Ciclo")
    cycle = gl.findCycle(graph)
    if cycle:
        st.success("Ciclo encontrado: " + " → ".join(map(str, cycle)))
    else:
        st.warning("El grafo no tiene ciclos.")

    st.subheader("Camino")
    nodeList = list(graph.nodes)
    pathOrigin = st.selectbox("Origen", nodeList, key="pathOrigin")
    pathDestination = st.selectbox("Destino", nodeList, index=1, key="pathDestination")
    path = gl.findPath(graph, pathOrigin, pathDestination)
    if path:
        st.success("Camino: " + " → ".join(map(str, path)))
    else:
        st.warning("No existe un camino entre esos nodos.")

with tabShortest:
    origin = st.selectbox("Nodo origen", nodeList, key="origin")
    destination = st.selectbox("Nodo destino", nodeList, index=1, key="destination")
    algorithm = st.selectbox("Algoritmo", ["Dijkstra", "Bellman-Ford"])

    if origin == destination:
        st.warning("El origen y el destino deben ser distintos.")
    else:
        try:
            if algorithm == "Dijkstra":
                shortestPath, cost = al.dijkstra(graph, origin, destination)
            else:
                shortestPath, cost = al.bellmanFord(graph, origin, destination)
        except ValueError as error:
            st.error(str(error))
        else:
            if shortestPath is None:
                st.warning("No existe una ruta entre esos nodos.")
            else:
                st.success("Ruta: " + " → ".join(map(str, shortestPath)))
                st.write(f"Costo total: **{cost:g}**")
                wd.drawGraph(graph, ponderated, shortestPath)
