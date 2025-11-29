from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import edge as edg
from DataStructures.List import array_list as al
from DataStructures.Graph import prim_structure as pst

def prim_mst(my_graph, source):
   
    g_order = dg.order(my_graph)
    prim = pst.new_prim_structure(source, g_order)

    vertices = dg.vertices(my_graph)

    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        mp.put(prim["marked"], v, False)
        mp.put(prim["dist_to"], v, float("inf"))
        mp.put(prim["edge_from"], v, None)

    mp.put(prim["dist_to"], source, 0)
    pq.insert(prim["pq"], source, 0)

    while not pq.is_empty(prim["pq"]):
        v = pq.del_min(prim["pq"])
        mp.put(prim["marked"], v, True)

        v_obj = dg.get_vertex(my_graph, v)
        adj_map = vt.get_adjacents(v_obj)
        adj_keys = mp.key_set(adj_map)

        for i in range(al.size(adj_keys)):
            w = al.get_element(adj_keys, i)
            edge = mp.get(adj_map, w)
            weight = edg.weight(edge)

            if mp.get(prim["marked"], w) is True:
                continue

            old_dist = mp.get(prim["dist_to"], w)
            if weight < old_dist:
                mp.put(prim["dist_to"], w, weight)
                mp.put(prim["edge_from"], w, v)
                pq.insert(prim["pq"], w, weight)

    return prim

def edges_mst(my_graph, aux_structure):
   
    edges_list = al.new_list()
    keys = mp.key_set(aux_structure["edge_from"])

    for i in range(al.size(keys)):
        v = al.get_element(keys, i)
        u = mp.get(aux_structure["edge_from"], v)

        if u is not None:
            dist = mp.get(aux_structure["dist_to"], v)
            arco = {
                "edge_from": u,
                "to": v,
                "dist_to": dist
            }
            al.add_last(edges_list, arco)

    return edges_list

def weight_mst(my_graph, aux_structure):

    total = 0
    keys = mp.key_set(aux_structure["dist_to"])

    for i in range(al.size(keys)):
        v = al.get_element(keys, i)
        dist = mp.get(aux_structure["dist_to"], v)

        if dist < float("inf"):
            total += dist

    return total