import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config


def drawMatrix(n, drawCell):
    headerCols = st.columns(n + 1, vertical_alignment="center", gap="small")
    headerCols[0].caption("Desde ↓ / Hacia →")
    for j in range(n):
        headerCols[j + 1].markdown(f"**Hacia {j + 1}**")

    st.divider()

    for i in range(n):
        rowCols = st.columns(n + 1, vertical_alignment="center")
        rowCols[0].markdown(f"**Desde {i + 1}**")
        for j in range(n):
            with rowCols[j + 1]:
                drawCell(i, j)


def entryNotPonderated(n: int):
    if "activeButtons" not in st.session_state:
        st.session_state.activeButtons = set()

    def drawToggleButton(i, j):
        btnId = f"{i}_{j}"
        isActive = btnId in st.session_state.activeButtons
        st.button(
            label="1" if isActive else "0",
            key=f"btn_{btnId}",
            type="primary" if isActive else "secondary",
            on_click=toggleButton,
            args=(btnId,),
        )

    drawMatrix(n, drawToggleButton)

    return [
        [1 if f"{i}_{j}" in st.session_state.activeButtons else 0 for j in range(n)]
        for i in range(n)
    ]


def entryPonderated(n: int):
    matrix = [[0] * n for _ in range(n)]

    def drawWeightInput(i, j):
        matrix[i][j] = st.number_input(
            label="peso",
            value=0.0,
            step=1.0,
            key=f"weight_{i}_{j}",
            label_visibility="collapsed",
        )

    drawMatrix(n, drawWeightInput)
    st.caption("0 significa que no hay arista.")

    return matrix


def toggleButton(btnId):
    if btnId in st.session_state.activeButtons:
        st.session_state.activeButtons.remove(btnId)
    else:
        st.session_state.activeButtons.add(btnId)


def drawGraph(graph, ponderated, pathNodes=None):
    pathNodes = pathNodes or []
    pathEdges = list(zip(pathNodes, pathNodes[1:]))

    nodes = []
    for node in graph.nodes:
        color = "#e74c3c" if node in pathNodes else "#4a90d9"
        nodes.append(Node(id=str(node), label=str(node), color=color))

    edges = []
    for u, v, weight in graph.edges(data="weight"):
        inPath = (u, v) in pathEdges or (not graph.is_directed() and (v, u) in pathEdges)
        edges.append(
            Edge(
                source=str(u),
                target=str(v),
                label=f"{weight:g}" if ponderated else "",
                color="#e74c3c" if inPath else "#999999",
                width=5 if inPath else 1,
            )
        )

    config = Config(width=700, height=450, directed=graph.is_directed(), physics=True)
    agraph(nodes=nodes, edges=edges, config=config)
