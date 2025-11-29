from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import digraph as dg
from DataStructures.Stack import stack as st
from DataStructures.Graph import vertex as vt
from DataStructures.List import array_list as al

from DataStructures.Map import map_linear_probing as mlp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vtx


def dfs(my_graph, source):
    """
    Inicia un DFS sobre my_graph desde el vértice source.
    Retorna la estructura search que contiene:
        visited, pre, post, reversepost, parent
    """

    search = {
        "visited": mlp.new_map(100, 0.75),
        "pre": al.new_list(),
        "post": al.new_list(),
        "reversepost": st.new_stack(),
        "parent": mlp.new_map(100, 0.75)
    }

    # Inicializar visitados y padres
    verts = dg.vertices(my_graph)
    for i in range(al.size(verts)):
        v = al.get_element(verts, i)
        mlp.put(search["visited"], v, False)
        mlp.put(search["parent"], v, None)

    dfs_vertex(my_graph, source, search)

    return search


def dfs_vertex(my_graph, vertex, search):
    """
    DFS recursivo. Actualiza:
        visited, pre, post, reversepost y parent.
    """
    mlp.put(search["visited"], vertex, True)
    al.add_last(search["pre"], vertex)
    vertex_obj = dg.get_vertex(my_graph, vertex)
    adj_map = vtx.get_adjacents(vertex_obj)
    adj_keys = mlp.key_set(adj_map)

    for i in range(al.size(adj_keys)):
        w = al.get_element(adj_keys, i)
        if not mlp.get(search["visited"], w):
            # Registrar el padre de w
            mlp.put(search["parent"], w, vertex)
            dfs_vertex(my_graph, w, search)

    al.add_last(search["post"], vertex)
    st.push(search["reversepost"], vertex)

    return search

def has_path_to(vertex, search):
    visited_map = search["visited"]

    if not mlp.contains(visited_map, vertex):
        return False
    return mlp.get(visited_map, vertex) is True


def path_to(vertex, search):

    if not mlp.contains(search["visited"], vertex):
        return None

    if mlp.get(search["visited"], vertex) is not True:
        return None

    parent_map = search["parent"]
    path = st.new_stack()
    current = vertex
    
    while current is not None:
        st.push(path, current)
        current = mlp.get(parent_map, current)

    return path
