from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import digraph as dg
from DataStructures.List import stack as st
import math

def dijsktra(my_graph, source):
    
    structure = ds.new_dijsktra_structure(source, dg.order(my_graph))

    visited = structure["visited"]
    heap = structure["pq"]

    vertices = dg.vertices(my_graph)

    for v in vertices["elements"]:
        mlp.put(visited, v, {
            "marked": False,
            "edge_from": None,
            "dist_to": float("inf")
        })

    src_info = mlp.get(visited, source)
    if src_info is None:
        raise KeyError(f"El vertice con llave {source} no existe en el grafo.")
    src_info["dist_to"] = 0

    pq.insert(heap, 0, source)

    while pq.size(heap) > 0:

        v = pq.remove(heap)
        v_info = mlp.get(visited, v)

        # La PQ puede contener duplicados
        if v_info["marked"]:
            continue

        v_info["marked"] = True

        # Obtener vecinos
        neighbors = dg.adjacents(my_graph, v)

        for w in neighbors["elements"]:

            edge = dg.get_edge(my_graph, v, w)
            weight = edge["weight"]

            w_info = mlp.get(visited, w)

            if w_info["marked"]:
                continue

            new_cost = v_info["dist_to"] + weight

            if new_cost < w_info["dist_to"]:
                w_info["dist_to"] = new_cost
                w_info["edge_from"] = v
                
                pq.insert(heap, new_cost, w)

    return structure

def dist_to(key_v, visited_map):
    
    if not mlp.contains(visited_map, key_v):
        return math.inf

    v_info = mlp.get(visited_map, key_v)
    return v_info["dist_to"]

def has_path_to(key_v, aux_structure):
    
    visited = aux_structure["visited"]
    if not mlp.contains(visited, key_v):
        return False
    info = mlp.get(visited, key_v)
    
    return info["marked"] == True

def path_to(key_v, aux_structure):
    visited = aux_structure["visited"]
    source = aux_structure["source"]
    info = mlp.get(visited, key_v)

    if info is None or info["marked"] is False or info["dist_to"] == float("inf"):
        return None

    stack = st.new_stack()
    v = key_v

    while v is not None:

        st.push(stack, v)

        if v == source:
            break

        v_info = mlp.get(visited, v)
        v = v_info["edge_from"]

    return stack