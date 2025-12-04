from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import vertex as vt
from DataStructures.Graph import edge as edg
from DataStructures.List import array_list as al
from DataStructures.Graph import prim_structure as pst

def prim_mst(my_graph, source):
    
    source = str(source)

    g_order = dg.order(my_graph)
    prim = pst.new_prim_structure(source, g_order)

    vertices = dg.vertices(my_graph)

    # Inicialización
    for i in range(al.size(vertices)):
        v = str(al.get_element(vertices, i))
        mp.put(prim["marked"], v, False)
        mp.put(prim["dist_to"], v, float("inf"))
        mp.put(prim["edge_from"], v, None)

    mp.put(prim["dist_to"], source, 0)
    pq.insert(prim["pq"], source, 0)

    # PRIM
    while not pq.is_empty(prim["pq"]):
        v = str(pq.del_min(prim["pq"]))
        mp.put(prim["marked"], v, True)

        # obtener vértice real del grafo
        v_obj = dg.get_vertex(my_graph, v)

        # si v no existe en el grafo → NO procesamos adyacentes (sin continue)
        if v_obj is not None:

            adj_map = vt.get_adjacents(v_obj)
            adj_keys = mp.key_set(adj_map)

            for i in range(al.size(adj_keys)):
                w = str(al.get_element(adj_keys, i))
                edge = mp.get(adj_map, w)
                weight = edg.weight(edge)

                marked_w = mp.get(prim["marked"], w)

                # relajación SOLO si aún no está marcado
                if marked_w is False:
                    old_dist = mp.get(prim["dist_to"], w)

                    if weight < old_dist:
                        mp.put(prim["dist_to"], w, weight)
                        mp.put(prim["edge_from"], w, v)
                        pq.insert(prim["pq"], w, weight)

    return prim
