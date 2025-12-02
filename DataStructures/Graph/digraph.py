from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import edge as edg
from DataStructures.List import array_list as al


def new_graph(order):
    map_order = max(order, 1)
    return {
        "vertices": mlp.new_map(map_order, 0.75),
        "num_edges": 0
    }

def insert_vertex(my_graph,key_u,info_u):
    new_vertex = vt.new_vertex(key_u, info_u)
    mlp.put(my_graph["vertices"], key_u, new_vertex)
    return my_graph

def contains_vertex(my_graph, key_u):
    return mlp.contains(my_graph["vertices"], key_u)

def order(my_graph):
    return mlp.size(my_graph["vertices"])

def size(my_graph):
    return my_graph["num_edges"]

def add_edge(my_graph, key_u, key_v, weight=1.0):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    
    vertex_v = mlp.get(my_graph["vertices"], key_v)
    if vertex_v is None:
        raise KeyError(f"Vertice con llave {key_v} no existe.")
    
    if vt.get_edge(vertex_u, key_v) is None:
        vt.add_adjacent(vertex_u, key_v, weight)
        my_graph["num_edges"] += 1
    
    if vt.get_edge(vertex_v, key_u) is None:
        vt.add_adjacent(vertex_v, key_u, weight)
        my_graph["num_edges"] += 1
    
    if vt.get_edge(vertex_u, key_v) is not None and vt.get_edge(vertex_v, key_u) is not None:
        my_graph["num_edges"] -= 1
    return my_graph

def vertices(my_graph):
    return mlp.key_set(my_graph["vertices"])

def degree(my_graph, key_u):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    mapa_arcos = vt.get_adjacents(vertex_u)
    return mlp.size(mapa_arcos)

def adjacents(my_graph, key_u):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    mapa_arcos = vt.get_adjacents(vertex_u)
    return mlp.key_set(mapa_arcos)

def get_vertex(my_graph, key_u):
    return mlp.get_element(my_graph["vertices"], key_u)

def edges_vertex(my_graph, vertex):
    key_u = vt.get_key(vertex)
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        return al.new_list()
    return adjacents(my_graph, key_u)

def update_vertex_info(my_graph, key_u, new_info_u):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    old_info = mlp.get_element(my_graph["vertices"], key_u)
    old_info["value"] = new_info_u
    return my_graph

def get_vertex_info(my_graph, key_u):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    return vt.get_value(vertex_u)

def get_edge(my_graph, key_u, key_v):
    vertex_u = mlp.get(my_graph["vertices"], key_u)
    if vertex_u is None:
        raise KeyError(f"Vertice con llave {key_u} no existe.")
    return vt.get_edge(vertex_u, key_v)

