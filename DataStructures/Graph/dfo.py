from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue
from DataStructures.Stack import stack
from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import dfo_structure


def dfo(my_graph):
  
    g_order = dg.order(my_graph)
    search = dfo_structure.new_dfo_structure(g_order)

    vertices = dg.vertices(my_graph)

    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        mp.put(search["marked"], v, False)

    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        if mp.get(search["marked"], v) is False:
            dfs_vertex(my_graph, v, search)

    return search


def dfs_vertex(my_graph, key_v, aux_structure):
    
    mp.put(aux_structure["marked"], key_v, True)

    # PREORDER
    queue.enqueue(aux_structure["pre"], key_v)

    # Procesar adyacentes
    vertex_obj = dg.get_vertex(my_graph, key_v)
    adj_map = vt.get_adjacents(vertex_obj)
    adj_keys = mp.key_set(adj_map)

    for i in range(al.size(adj_keys)):
        w = al.get_element(adj_keys, i)
        visited = mp.get(aux_structure["marked"], w)

        if visited is None:
            mp.put(aux_structure["marked"], w, False)
            visited = False

        if visited is False:
            dfs_vertex(my_graph, w, aux_structure)

    # POSTORDER
    queue.enqueue(aux_structure["post"], key_v)

    # REVERSE POSTORDER
    stack.push(aux_structure["reversepost"], key_v)

    return aux_structure