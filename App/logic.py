import time
import math
import csv
from datetime import datetime
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import dijsktra as djk
from DataStructures.List import single_linked_list as lt
from DataStructures.Graph import dfo as dfo
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dfs as dfs
from DataStructures.Stack import stack as st
from DataStructures.Graph import edge as edg
from DataStructures.Graph import prim as prim
from DataStructures.Graph import vertex as vt

def haversine(lat1, lon1, lat2, lon2):
    """
    Distancia Haversine en kilómetros entre dos puntos (lat, lon) en grados.
    """
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_closest_node(catalog, lat, lon):
    """
    Dado un catálogo y una posición (lat, lon),
    devuelve (nodo_más_cercano).

    Si no hay nodos, devuelve (None).
    """
    nodes_list = catalog["nodes"]
    best_node = None
    best_dist = math.inf

    n = al.size(nodes_list)
    for i in range(n):
        node = al.get_element(nodes_list, i)
        d = haversine(lat, lon, node["lat"], node["lon"])
        if d < best_dist:
            best_dist = d
            best_node = node

    return best_node

def get_first_last_nodes(catalog, path_list, graph):
    """
    Extrae los primeros 5 y últimos 5 nodos de un camino
    usando SOLO TADS del curso (array_list y map).
    """

    first_5 = al.new_list()
    last_5 = al.new_list()
    total_nodes = al.size(path_list)

    if total_nodes == 0:
        return first_5, last_5

    # primeros 5
    limit_first = min(5, total_nodes)

    for i in range(limit_first):

        node_id = al.get_element(path_list, i)
        node = mp.get(catalog["nodes_by_id"], node_id)

        # Distancia al siguiente nodo
        distance_to_next = "Desconocido"

        if i < total_nodes - 1:
            next_node_id = al.get_element(path_list, i + 1)

            v_obj = dg.get_vertex(graph, node_id)
            edge = vt.get_edge(v_obj, next_node_id)

            if edge is not None:
                distance_to_next = edge["weight"]

        # TAGS del nodo actual
        tags = node["tags"]
        n_tags = al.size(tags)

        # primeros y ultimos 3 tags
        first_3_tags = al.new_list()
        limit_3_first = min(3, n_tags)

        for j in range(limit_3_first):
            al.add_last(first_3_tags, al.get_element(tags, j))

        if al.size(first_3_tags) == 0:
            al.add_last(first_3_tags, "Desconocido")

        last_3_tags = al.new_list()
        limit_3_last = min(3, n_tags)
        start_last = n_tags - limit_3_last

        # Evitar negativos 
        if start_last < 0:
            start_last = 0

        for j in range(start_last, n_tags):
            al.add_last(last_3_tags, al.get_element(tags, j))

        if al.size(last_3_tags) == 0:
            al.add_last(last_3_tags, "Desconocido")


        node_info = {
            "id": node_id,
            "lat": node["lat"],
            "lon": node["lon"],
            "num_individuals": n_tags,
            "first_3_tags": first_3_tags,
            "last_3_tags": last_3_tags,
            "distance_to_next": distance_to_next
        }

        al.add_last(first_5, node_info)

    # ultimos 5-
    limit_last = min(5, total_nodes)
    start_last_section = total_nodes - limit_last

    for i in range(start_last_section, total_nodes):

        node_id = al.get_element(path_list, i)
        node = mp.get(catalog["nodes_by_id"], node_id)

        distance_to_next = "Desconocido"

        if i < total_nodes - 1:
            next_node_id = al.get_element(path_list, i + 1)

            v_obj = dg.get_vertex(graph, node_id)
            edge = vt.get_edge(v_obj, next_node_id)

            if edge is not None:
                distance_to_next = edge["weight"]

        tags = node["tags"]
        n_tags = al.size(tags)

        first_3_tags = al.new_list()
        limit_3_first = min(3, n_tags)

        for j in range(limit_3_first):
            al.add_last(first_3_tags, al.get_element(tags, j))

        if al.size(first_3_tags) == 0:
            al.add_last(first_3_tags, "Desconocido")

        last_3_tags = al.new_list()
        limit_3_last = min(3, n_tags)
        start_last_tags = n_tags - limit_3_last

        if start_last_tags < 0:
            start_last_tags = 0

        for j in range(start_last_tags, n_tags):
            al.add_last(last_3_tags, al.get_element(tags, j))

        if al.size(last_3_tags) == 0:
            al.add_last(last_3_tags, "Desconocido")

        node_info = {
            "id": node_id,
            "lat": node["lat"],
            "lon": node["lon"],
            "num_individuals": n_tags,
            "first_3_tags": first_3_tags,
            "last_3_tags": last_3_tags,
            "distance_to_next": distance_to_next
        }

        al.add_last(last_5, node_info)

    return first_5, last_5


def cmp_events_by_timestamp(e1, e2):
    return e1["timestamp"] < e2["timestamp"]

def new_logic():

    eventos_estimados = 25000
    catalog = {
        "events": al.new_list(),                 
        "nodes": al.new_list(),                 
        "nodes_by_id": mp.new_map(eventos_estimados, 0.7),
        "event_to_node": mp.new_map(eventos_estimados, 0.7),
        "tags": mp.new_map(128, 0.7),        
        "graph_distance": dg.new_graph(eventos_estimados),
        "graph_water": dg.new_graph(eventos_estimados),
    }


    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename='1000_cranes_mongolia_small.csv'):
    start = get_time()
    events = catalog["events"]
    tags_map = catalog["tags"]

    ruta = "Data/" + filename
    with open(ruta, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            event_id = row["event-id"]
            lat = float(row["location-lat"])
            lon = float(row["location-long"])
            timestamp = datetime.strptime(row["timestamp"],
                                          "%Y-%m-%d %H:%M:%S.%f")

            comments = row["comments"]
            if comments == "":
                dist_agua_km = 0.0
            else:
                dist_agua_km = float(comments) / 1000.0

            tag_str = row["tag-local-identifier"]
            tag = int(tag_str) if tag_str.isdigit() else tag_str

            evento = {
                "event-id": event_id,
                "lat": lat,
                "lon": lon,
                "timestamp": timestamp,
                "dist_agua_km": dist_agua_km,
                "tag": tag
            }

            al.add_last(events, evento)

            if not mp.contains(tags_map, tag):
                mp.put(tags_map, tag, True)

    total_eventos = al.size(events)

    # Ordenar eventos
    if total_eventos > 1:
        events_sorted = al.merge_sort(events, cmp_events_by_timestamp)
        catalog["events"] = events_sorted
        events = events_sorted

    # Inicializar estructuras
    nodes_list = catalog["nodes"]
    nodes_by_id = catalog["nodes_by_id"]
    event_to_node = catalog["event_to_node"]
    g_dist = catalog["graph_distance"]
    g_water = catalog["graph_water"]

    # CREACIÓN DE NODOS

    for i in range(total_eventos):
        ev = al.get_element(events, i)
        ev_id = ev["event-id"]
        ev_lat = ev["lat"]
        ev_lon = ev["lon"]
        ev_time = ev["timestamp"]
        ev_dist_agua = ev["dist_agua_km"]
        ev_tag = ev["tag"]

        # Buscar si el evento pertenece a algún nodo existente
        nodo_encontrado = None
        j = 0
        total_nodes = al.size(nodes_list)

        while j < total_nodes and nodo_encontrado is None:
            node = al.get_element(nodes_list, j)

            dt_hours = abs((ev_time - node["creation_timestamp"]).total_seconds()) / 3600.0

            d_km = haversine(node["lat"], node["lon"], ev_lat, ev_lon)

            if d_km < 3.0 and dt_hours < 3.0:
                nodo_encontrado = node

            j += 1

        # Si se encontró nodo, agregar evento al nodo
        if nodo_encontrado is not None:

            al.add_last(nodo_encontrado["events"], ev)
            nodo_encontrado["events_count"] += 1

            # Agregar tag si no existe
            tags_list = nodo_encontrado["tags"]
            found = False
            k = 0
            total_tags = al.size(tags_list)

            while k < total_tags and not found:
                if al.get_element(tags_list, k) == ev_tag:
                    found = True
                k += 1

            if not found:
                al.add_last(tags_list, ev_tag)

            # Actualizar promedio distancia al agua
            c = nodo_encontrado["events_count"]
            old_avg = nodo_encontrado["prom_distancia_agua"]
            nodo_encontrado["prom_distancia_agua"] = (old_avg * (c - 1) + ev_dist_agua) / c

            mp.put(event_to_node, ev_id, nodo_encontrado["id"])

        else:
            # Crear nuevo nodo
            node_id = ev_id
            node = {
                "id": node_id,
                "lat": ev_lat,
                "lon": ev_lon,
                "creation_timestamp": ev_time,
                "tags": al.new_list(),
                "events": al.new_list(),
                "events_count": 1,
                "prom_distancia_agua": ev_dist_agua
            }

            al.add_last(node["events"], ev)
            al.add_last(node["tags"], ev_tag)

            al.add_last(nodes_list, node)
            mp.put(nodes_by_id, node_id, node)
            dg.insert_vertex(g_dist, node_id, node)
            dg.insert_vertex(g_water, node_id, node)
            mp.put(event_to_node, ev_id, node_id)

    total_nodos = al.size(nodes_list)
    total_grullas = mp.size(tags_map)

    # CREACIÓN DE ARCOS 

    last_node_by_tag = mp.new_map(total_grullas + 1, 0.7)
    dist_migratoria = mp.new_map(total_nodos + 1, 0.7)
    dist_hidrica = mp.new_map(total_nodos + 1, 0.7)

    for i in range(total_eventos):
        ev = al.get_element(events, i)
        tag = ev["tag"]
        ev_id = ev["event-id"]

        node_id = mp.get(event_to_node, ev_id)
        prev_node_id = mp.get(last_node_by_tag, tag)

        # CASO 1: Es el primer evento de esta grulla
        if prev_node_id is None:
            mp.put(last_node_by_tag, tag, node_id)

        else:
            node_prev = mp.get(nodes_by_id, prev_node_id)
            node_curr = mp.get(nodes_by_id, node_id)

            if node_id != prev_node_id:
                d_km = haversine(node_prev["lat"], node_prev["lon"], node_curr["lat"], node_curr["lon"])

                # Grafo de distancia
                sub = mp.get(dist_migratoria, prev_node_id)
                if sub is None:
                    sub = mp.new_map(4, 0.7)
                    mp.put(dist_migratoria, prev_node_id, sub)

                agg = mp.get(sub, node_id)
                if agg is None:
                    agg = {"sum": 0.0, "count": 0}

                agg["sum"] += d_km
                agg["count"] += 1
                mp.put(sub, node_id, agg)

                # Grafo hídrico
                agua = node_curr["prom_distancia_agua"]
                sub_h = mp.get(dist_hidrica, prev_node_id)
                if sub_h is None:
                    sub_h = mp.new_map(4, 0.7)
                    mp.put(dist_hidrica, prev_node_id, sub_h)

                agg_h = mp.get(sub_h, node_id)
                if agg_h is None:
                    agg_h = {"sum": 0.0, "count": 0}

                agg_h["sum"] += agua
                agg_h["count"] += 1
                mp.put(sub_h, node_id, agg_h)

            mp.put(last_node_by_tag, tag, node_id)

    # ARCOS DEFINITIVOS

    keys_u = mp.key_set(dist_migratoria)
    for i in range(al.size(keys_u)):
        u = al.get_element(keys_u, i)
        sub = mp.get(dist_migratoria, u)
        keys_v = mp.key_set(sub)
        for j in range(al.size(keys_v)):
            v = al.get_element(keys_v, j)
            agg = mp.get(sub, v)
            avg = agg["sum"] / agg["count"]
            dg.add_edge(g_dist, u, v, avg)

    keys_u = mp.key_set(dist_hidrica)
    for i in range(al.size(keys_u)):
        u = al.get_element(keys_u, i)
        sub = mp.get(dist_hidrica, u)
        keys_v = mp.key_set(sub)
        for j in range(al.size(keys_v)):
            v = al.get_element(keys_v, j)
            agg = mp.get(sub, v)
            avg = agg["sum"] / agg["count"]
            dg.add_edge(g_water, u, v, avg)

    # PRIMEROS Y ÚLTIMOS

    primeros_5 = al.new_list()
    ultimos_5 = al.new_list()

    if total_nodos > 0:
        limite = min(5, total_nodos)
        for i in range(limite):
            al.add_last(primeros_5, al.get_element(nodes_list, i))

        limite2 = min(5, total_nodos)
        inicio_ultimos = total_nodos - limite2
        for i in range(inicio_ultimos, total_nodos):
            al.add_last(ultimos_5, al.get_element(nodes_list, i))

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return (
        catalog,
        tiempo_ms,
        total_grullas,
        total_eventos,
        total_nodos,
        dg.order(g_dist),
        dg.order(g_water),
        primeros_5,
        ultimos_5
    )

#prueba commit
# Funciones de consulta sobre el catálogo
def req_1(catalog, lat_origin, lon_origin, lat_dest, lon_dest, crane_id):

    start = get_time()
    graph = catalog["graph_distance"]
    nodes_by_id = catalog["nodes_by_id"]

    # 1. Encontrar nodos de origen y destino más cercanos a las coordenadas
    origin_node = find_closest_node(catalog, lat_origin, lon_origin)
    dest_node = find_closest_node(catalog, lat_dest, lon_dest)

    if origin_node is None or dest_node is None:
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            "Unknown",              # origin_id
            "Unknown",              # dest_id
            "Unknown",              # first_node_with_crane
            al.new_list(),          # path_ids
            0.0,                    # total_dist
            0,                      # num_vertices
            al.new_list(),          # segment_costs
            al.new_list(),          # primeros_5_nodes
            al.new_list(),          # ultimos_5_nodes
            tiempo_ms
        )

    origin_id = origin_node["id"]
    dest_id = dest_node["id"]

    # Verificar que ambos vértices existan en el grafo
    if not dg.contains_vertex(graph, origin_id) or not dg.contains_vertex(graph, dest_id):
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            origin_id,
            dest_id,
            "Unknown",
            al.new_list(),
            0.0,
            0,
            al.new_list(),
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    # 2. DFS desde el nodo de origen
    structure = dfs.dfs(graph, origin_id)

    # 3. Verificar que haya camino al destino
    if not dfs.has_path_to(dest_id, structure):
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            origin_id,
            dest_id,
            "Unknown",
            al.new_list(),
            0.0,
            0,
            al.new_list(),
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    # 4. Reconstruir camino como stack de ids (origen → destino usando pop)
    path_stack = dfs.path_to(dest_id, structure)  # stack con llaves de vértices

    path_ids = al.new_list()
    while not st.is_empty(path_stack):
        node_id = st.pop(path_stack)
        al.add_last(path_ids, node_id)

    num_vertices = al.size(path_ids)

    # 5. Calcular distancia total y costos por segmento
    total_dist = 0.0
    segment_costs = al.new_list()

    for i in range(num_vertices):
        if i < num_vertices - 1:
            u = al.get_element(path_ids, i)
            v = al.get_element(path_ids, i + 1)
            edge = dg.get_edge(graph, u, v)
            if edge is not None:
                w = edg.weight(edge)
            else:
                w = 0.0
            total_dist += w
            al.add_last(segment_costs, w)
        else:
            # Último nodo no tiene siguiente
            al.add_last(segment_costs, 0.0)

    # 6. Buscar el primer nodo donde esté la grulla (crane_id)
    if isinstance(crane_id, str) and crane_id.isdigit():
        crane_tag = int(crane_id)
    else:
        crane_tag = crane_id

    first_node_with_crane = "Unknown"

    for i in range(num_vertices):
        node_id = al.get_element(path_ids, i)
        node = mp.get(nodes_by_id, node_id)
        if node is None:
            continue
        tags_list = node["tags"]
        found = False
        for j in range(al.size(tags_list)):
            if al.get_element(tags_list, j) == crane_tag:
                found = True
                break
        if found:
            first_node_with_crane = node_id
            break

    # 7. Primeros 5 y últimos 5 nodos (info completa)
    primeros_5_nodes = al.new_list()
    ultimos_5_nodes = al.new_list()

    if num_vertices > 0:
        limite = min(5, num_vertices)
        for i in range(limite):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(primeros_5_nodes, node)

        limite2 = min(5, num_vertices)
        inicio_ultimos = num_vertices - limite2
        for i in range(inicio_ultimos, num_vertices):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(ultimos_5_nodes, node)

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return (
        origin_id,
        dest_id,
        first_node_with_crane,
        path_ids,
        total_dist,
        num_vertices,
        segment_costs,
        primeros_5_nodes,
        ultimos_5_nodes,
        tiempo_ms
    )

    
def req_2(catalog, lat_origin, lon_origin, lat_dest, lon_dest, radio_km):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start = get_time()

    graph = catalog["graph_distance"]
    nodes_by_id = catalog["nodes_by_id"]

    # 1. Encontrar nodos de origen y destino más cercanos a las coordenadas
    origin_node = find_closest_node(catalog, lat_origin, lon_origin)
    dest_node = find_closest_node(catalog, lat_dest, lon_dest)

    # Si por alguna razón no se encuentran nodos
    if origin_node is None or dest_node is None:
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            "Unknown",
            "Unknown",
            "Unknown",
            al.new_list(),
            0.0,
            0,
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    origin_id = origin_node["id"]
    dest_id = dest_node["id"]

    # 2. BFS desde el nodo de origen
    visited = bfs.bfs(graph, origin_id)

    # Si no hay camino al destino
    if not bfs.has_path_to(dest_id, visited):
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            origin_id,
            dest_id,
            "Unknown",
            al.new_list(),
            0.0,
            0,
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    # 3. Reconstruir el camino usando la pila retornada por bfs.path_to
    stack_path = bfs.path_to(dest_id, visited)

    path_ids = al.new_list()
    while not st.is_empty(stack_path):
        node_id = st.pop(stack_path)
        al.add_last(path_ids, node_id)

    num_nodes_path = al.size(path_ids)

    # 4. Calcular distancia total del camino (suma de pesos de arcos)
    total_dist = 0.0
    for i in range(num_nodes_path - 1):
        u = al.get_element(path_ids, i)
        v = al.get_element(path_ids, i + 1)
        edge = dg.get_edge(graph, u, v)
        if edge is not None:
            total_dist += edg.weight(edge)

    # 5. Encontrar el último nodo dentro del radio desde el origen
    last_inside_id = "Unknown"
    origin_lat = origin_node["lat"]
    origin_lon = origin_node["lon"]

    for i in range(num_nodes_path):
        node_id = al.get_element(path_ids, i)
        node = mp.get(nodes_by_id, node_id)
        if node is None:
            continue
        d_origin = haversine(origin_lat, origin_lon, node["lat"], node["lon"])
        if d_origin <= radio_km:
            last_inside_id = node_id
        else:
            # en cuanto se sale del área, dejamos de actualizar
            break

    # 6. Construir listas de primeros y últimos 5 nodos (con toda su info)
    primeros_5_nodes = al.new_list()
    ultimos_5_nodes = al.new_list()

    if num_nodes_path > 0:
        limite = min(5, num_nodes_path)
        for i in range(limite):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(primeros_5_nodes, node)

        limite2 = min(5, num_nodes_path)
        inicio_ultimos = num_nodes_path - limite2
        for i in range(inicio_ultimos, num_nodes_path):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(ultimos_5_nodes, node)

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return (
        origin_id,
        dest_id,
        last_inside_id,
        path_ids,
        total_dist,
        num_nodes_path,
        primeros_5_nodes,
        ultimos_5_nodes,
        tiempo_ms
    )


def req_3(catalog):
    """
    REQ 3: Identificar posibles rutas migratorias dentro del nicho biológico
    Usando Orden Topológico (DFO) sobre el grafo de todos los puntos migratorios.
    """

    start = get_time()

    graph = catalog["graph_distance"]     # Grafo del nicho biológico
    nodes_map = catalog["nodes_by_id"]    # id_nodo -> info_nodo

    # dfo 
    structure = dfo.dfo(graph)
    reversepost = structure["reversepost"]   # stack con reverse postorder

    # Si no hay nada, no hay ruta migratoria viable
    if st.size(reversepost) == 0:
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            0,                 # total_puntos
            0,                 # total_individuos
            al.new_list(),     # primeros_5
            al.new_list(),     # ultimos_5
            tiempo_ms
        )

    # 2. Pasar reversepost (stack) a un array_list 'order' en orden topológico 
    order = al.new_list()
    while st.size(reversepost) > 0:
        v = st.pop(reversepost)       # al hacer pop de reversepost se obtiene el topological order
        al.add_last(order, v)

    total_puntos = al.size(order)

    #3. Total de individuos únicos que usan la ruta migratoria 
    individuos_set = mp.new_map(5000, 0.7)   # mapa de grullas usando map

    for i in range(total_puntos):
        nid = al.get_element(order, i)
        node = mp.get(nodes_map, nid)
        if node is None:
            continue

        tags_list = node["tags"]              # array_list de IDs de grullas
        tags_count = al.size(tags_list)

        for j in range(tags_count):
            grulla_id = al.get_element(tags_list, j)
            mp.put(individuos_set, grulla_id, True)

    total_individuos = mp.size(individuos_set)

    # Construir lista enriquecida de puntos migratorios de la ruta
    enriched = al.new_list()

    for i in range(total_puntos):

        nid = al.get_element(order, i)
        node = mp.get(nodes_map, nid)
        if node is None:
            continue

        # lat / lon (Unknown si no existen)
        if "lat" in node and "lon" in node:
            lat = node["lat"]
            lon = node["lon"]
        else:
            lat = "Unknown"
            lon = "Unknown"

        tags_list = node["tags"]           # array_list
        tags_count = al.size(tags_list)

        # Tres primeros y tres últimos IDs de grullas
        # primeras 3
        primeras_3 = al.new_list()
        limit_first = 3 if tags_count >= 3 else tags_count

        for k in range(limit_first):
            grulla_id = al.get_element(tags_list, k)
            al.add_last(primeras_3, grulla_id)

        # últimas 3
        ultimas_3 = al.new_list()
        limit_last = 3 if tags_count >= 3 else tags_count

        start_idx = tags_count - limit_last
        for k in range(start_idx, tags_count):
            grulla_id = al.get_element(tags_list, k)
            al.add_last(ultimas_3, grulla_id)

        # Distancias a vértices vecinos en la ruta
        dist_prev = "Unknown"
        dist_next = "Unknown"

        # distancia al vértice anterior en la ruta migratoria
        if i > 0 and lat != "Unknown" and lon != "Unknown":
            prev_id = al.get_element(order, i - 1)
            prev_node = mp.get(nodes_map, prev_id)
            if prev_node is not None and "lat" in prev_node and "lon" in prev_node:
                dist_prev = haversine(lat, lon,prev_node["lat"], prev_node["lon"])

        # distancia al vértice siguiente en la ruta migratoria
        if i < total_puntos - 1 and lat != "Unknown" and lon != "Unknown":
            next_id = al.get_element(order, i + 1)
            next_node = mp.get(nodes_map, next_id)
            if next_node is not None and "lat" in next_node and "lon" in next_node:
                dist_next = haversine(lat, lon, next_node["lat"], next_node["lon"])

        desc = {
            "id": nid,
            "lat": lat,
            "lon": lon,
            "num_individuos": tags_count,
            "primeras_3_grullas": primeras_3,
            "ultimas_3_grullas": ultimas_3,
            "distancia_anterior": dist_prev,
            "distancia_siguiente": dist_next
        }

        al.add_last(enriched, desc)

    # --- 5. Sacar los CINCO primeros y CINCO últimos vértices de la ruta migratoria ---
    limit = 5 if total_puntos >= 5 else total_puntos

    # sub_list(list, pos_i, num_elements)
    primeros_5 = al.sub_list(enriched, 0, limit)
    ultimos_5 = al.sub_list(enriched, total_puntos - limit, limit)
    end = get_time()
    tiempo_ms = delta_time(start, end)

    # --- 6. Retorno en el formato que probablemente usará tu view ---
    return (
        total_puntos,
        total_individuos,
        primeros_5,
        ultimos_5,
        tiempo_ms
    )

def req_4(catalog, lat_origin, lon_origin):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    
    start = get_time()
    
    # 1. Encontrar nodo de origen más cercano a las coordenadas
    origin_node = find_closest_node(catalog, lat_origin, lon_origin)
    
    if origin_node is None:
        end = get_time()
        return (
            "Unknown",
            0,
            0,
            0.0,
            al.new_list(),
            al.new_list(),
            delta_time(start, end)
        )
    
    # IMPORTANTE: Convertir a string para evitar problemas de tipos
    origin_id = str(origin_node["id"])
    graph = catalog["graph_water"]  # Usar grafo hídrico
    nodes_by_id = catalog["nodes_by_id"]
    
    # 2. Verificar que el vértice existe en el grafo
    if not dg.contains_vertex(graph, origin_id):
        end = get_time()
        return (
            origin_id,
            0,
            0,
            0.0,
            al.new_list(),
            al.new_list(),
            delta_time(start, end)
        )
    
    # 3. Ejecutar Prim desde el origen
    prim_structure = prim.prim_mst(graph, origin_id)
    
    # 4. Obtener los vértices que pertenecen al MST
    # Un vértice está en el MST si su distancia es < infinito
    mst_vertices = al.new_list()
    keys_dist = mp.key_set(prim_structure["dist_to"])
    
    for i in range(al.size(keys_dist)):
        vertex_id = al.get_element(keys_dist, i)
        # Convertir a string por consistencia
        vertex_id = str(vertex_id)
        dist = mp.get(prim_structure["dist_to"], vertex_id)
        
        # Solo incluir vértices alcanzables (distancia < infinito)
        if dist is not None and dist < float("inf"):
            al.add_last(mst_vertices, vertex_id)
    
    total_puntos = al.size(mst_vertices)
    
    # Si no hay puntos en el MST
    if total_puntos == 0:
        end = get_time()
        return (
            origin_id,
            0,
            0,
            0.0,
            al.new_list(),
            al.new_list(),
            delta_time(start, end)
        )
    
    # 5. Calcular peso total del MST (distancia total a fuentes hídricas)
    total_dist_hidrica = prim.weight_mst(graph, prim_structure)
    
    # 6. Contar individuos únicos (grullas) que usan el corredor
    individuos_map = mp.new_map(total_puntos * 4, 0.7)
    
    for i in range(total_puntos):
        vertex_id = al.get_element(mst_vertices, i)
        node = mp.get(nodes_by_id, vertex_id)
        
        if node is None:
            continue
        
        tags = node["tags"]
        num_tags = al.size(tags)
        
        for j in range(num_tags):
            tag = al.get_element(tags, j)
            # Convertir tag a string para evitar problemas de comparación
            tag_str = str(tag)
            if not mp.contains(individuos_map, tag_str):
                mp.put(individuos_map, tag_str, True)
    
    total_individuos = mp.size(individuos_map)
    
    # 7. Obtener primeros 5 y últimos 5 nodos con información detallada
    primeros_5 = al.new_list()
    ultimos_5 = al.new_list()
    
    if total_puntos > 0:
        # Primeros 5
        limit_first = min(5, total_puntos)
        for i in range(limit_first):
            vertex_id = al.get_element(mst_vertices, i)
            node = mp.get(nodes_by_id, vertex_id)
            
            if node is None:
                continue
            
            # Obtener tags
            tags = node["tags"]
            num_tags = al.size(tags)
            
            # Primeros 3 tags
            first_3_tags = al.new_list()
            for j in range(min(3, num_tags)):
                al.add_last(first_3_tags, al.get_element(tags, j))
            
            if al.size(first_3_tags) == 0:
                al.add_last(first_3_tags, "Desconocido")
            
            # Últimos 3 tags
            last_3_tags = al.new_list()
            if num_tags <= 3:
                # Si hay 3 o menos, copiar los primeros
                for j in range(num_tags):
                    al.add_last(last_3_tags, al.get_element(tags, j))
            else:
                # Tomar los últimos 3
                start_idx = num_tags - 3
                for j in range(start_idx, num_tags):
                    al.add_last(last_3_tags, al.get_element(tags, j))
            
            if al.size(last_3_tags) == 0:
                al.add_last(last_3_tags, "Desconocido")
            
            node_info = {
                "id": vertex_id,
                "lat": node.get("lat", "Unknown"),
                "lon": node.get("lon", "Unknown"),
                "num_individuals": num_tags,
                "first_3_tags": first_3_tags,
                "last_3_tags": last_3_tags
            }
            
            al.add_last(primeros_5, node_info)
        
        # Últimos 5
        limit_last = min(5, total_puntos)
        start_last = total_puntos - limit_last
        
        for i in range(start_last, total_puntos):
            vertex_id = al.get_element(mst_vertices, i)
            node = mp.get(nodes_by_id, vertex_id)
            
            if node is None:
                continue
            
            # Obtener tags
            tags = node["tags"]
            num_tags = al.size(tags)
            
            # Primeros 3 tags
            first_3_tags = al.new_list()
            for j in range(min(3, num_tags)):
                al.add_last(first_3_tags, al.get_element(tags, j))
            
            if al.size(first_3_tags) == 0:
                al.add_last(first_3_tags, "Desconocido")
            
            # Últimos 3 tags
            last_3_tags = al.new_list()
            if num_tags <= 3:
                for j in range(num_tags):
                    al.add_last(last_3_tags, al.get_element(tags, j))
            else:
                start_idx = num_tags - 3
                for j in range(start_idx, num_tags):
                    al.add_last(last_3_tags, al.get_element(tags, j))
            
            if al.size(last_3_tags) == 0:
                al.add_last(last_3_tags, "Desconocido")
            
            node_info = {
                "id": vertex_id,
                "lat": node.get("lat", "Unknown"),
                "lon": node.get("lon", "Unknown"),
                "num_individuals": num_tags,
                "first_3_tags": first_3_tags,
                "last_3_tags": last_3_tags
            }
            
            al.add_last(ultimos_5, node_info)
    
    end = get_time()
    tiempo_ms = delta_time(start, end)
    
    return (
        origin_id,
        total_puntos,
        total_individuos,
        total_dist_hidrica,
        primeros_5,
        ultimos_5,
        tiempo_ms
    )

def req_5(catalog, lat_origin, lon_origin, lat_dest, lon_dest, tipo_grafo):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start = get_time()

    # 1. Escoger grafo según selección del usuario
    tipo = str(tipo_grafo).lower().strip()
    if tipo.startswith("d"):  # 'd', 'dist', 'distancia', '1', etc.
        graph = catalog["graph_distance"]
    elif tipo.startswith("a"):  # 'a', 'agua', 'hidrica', '2', etc.
        graph = catalog["graph_water"]
    else:
        # Por defecto, usar grafo de distancia si la entrada es rara
        graph = catalog["graph_distance"]

    nodes_by_id = catalog["nodes_by_id"]

    # 2. Encontrar nodos de origen y destino más cercanos a las coordenadas
    origin_node = find_closest_node(catalog, lat_origin, lon_origin)
    dest_node = find_closest_node(catalog, lat_dest, lon_dest)

    if origin_node is None or dest_node is None:
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            "Unknown",   # origin_id
            "Unknown",   # dest_id
            0.0,         # total_cost
            0,           # num_vertices
            0,           # num_arcos
            al.new_list(),  # path_ids
            al.new_list(),  # segment_costs
            al.new_list(),  # primeros_5_nodes
            al.new_list(),  # ultimos_5_nodes
            tiempo_ms
        )

    origin_id = origin_node["id"]
    dest_id = dest_node["id"]

    # 3. Ejecutar Dijkstra desde el nodo de origen en el grafo seleccionado
    structure = djk.dijsktra(graph, origin_id)

    # Si no hay camino al destino
    if not djk.has_path_to(dest_id, structure):
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            origin_id,
            dest_id,
            0.0,
            0,
            0,
            al.new_list(),
            al.new_list(),
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    # 4. Reconstruir el camino (pila de vértices) y pasarlo a ARRAY_LIST de ids
    stack_path = djk.path_to(dest_id, structure)
    if stack_path is None:
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            origin_id,
            dest_id,
            0.0,
            0,
            0,
            al.new_list(),
            al.new_list(),
            al.new_list(),
            al.new_list(),
            tiempo_ms
        )

    path_ids = al.new_list()
    n = lt.size(stack_path)

    for i in range(n):
        elem = lt.get_element(stack_path, i)
        # Stack suele guardar nodos tipo {"info": id}, por si acaso chequeamos
        if isinstance(elem, dict) and "info" in elem:
            node_id = elem["info"]
        else:
            node_id = elem
        al.add_last(path_ids, node_id)

    num_vertices = n
    num_arcos = max(0, num_vertices - 1)

    # 5. Costo total desde Dijkstra
    total_cost = djk.dist_to(dest_id, structure["visited"])

    # 6. Costo por segmento (al siguiente vértice) según el grafo
    segment_costs = al.new_list()
    for i in range(num_vertices):
        if i < num_vertices - 1:
            u = al.get_element(path_ids, i)
            v = al.get_element(path_ids, i + 1)
            edge = dg.get_edge(graph, u, v)
            if edge is not None:
                cost = edg.weight(edge)
            else:
                cost = 0.0
        else:
            # Último nodo no tiene siguiente
            cost = 0.0
        al.add_last(segment_costs, cost)

    # 7. Construir listas de primeros y últimos 5 nodos (dicts completos)
    primeros_5_nodes = al.new_list()
    ultimos_5_nodes = al.new_list()

    if num_vertices > 0:
        # Primeros 5
        limite = min(5, num_vertices)
        for i in range(limite):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(primeros_5_nodes, node)

        # Últimos 5
        limite2 = min(5, num_vertices)
        inicio_ultimos = num_vertices - limite2
        for i in range(inicio_ultimos, num_vertices):
            node_id = al.get_element(path_ids, i)
            node = mp.get(nodes_by_id, node_id)
            al.add_last(ultimos_5_nodes, node)

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return (
        origin_id,
        dest_id,
        total_cost,
        num_vertices,
        num_arcos,
        path_ids,
        segment_costs,
        primeros_5_nodes,
        ultimos_5_nodes,
        tiempo_ms
    )

def req_6(catalog):
    start = get_time()
    graph = catalog["graph_water"]
    nodes_map = catalog["nodes_by_id"]

    # --- 1. Obtener todos los vértices del grafo hídrico ---
    verts = dg.vertices(graph)   # array_list con IDs de nodos

    num_vertices = al.size(verts)

    # Mapa nodo -> subred_id (índice de subred)
    node_to_subred = mp.new_map(num_vertices, 0.7)

    # Mapa subred_id -> lista de nodos de esa subred
    subred_to_nodes = mp.new_map(num_vertices, 0.7)

    subred_id_counter = 0

    # --- 2. Recorrer todos los nodos y lanzar BFS por cada componente ---
    for i in range(num_vertices):
        nid = al.get_element(verts, i)

        # Si el nodo ya tiene subred asignada, lo saltamos
        if mp.contains(node_to_subred, nid):
            continue

        # Nueva subred
        subred_id_counter += 1

        # BFS desde nid
        visited_map = bfs.bfs(graph, nid)   # mapa node_id -> {edge_from, dist_to, marked}

        # Lista de nodos para esta subred
        nodes_list = al.new_list()
        mp.put(subred_to_nodes, subred_id_counter, nodes_list)

        # Para cada nodo alcanzado en este BFS, lo marcamos como parte de esta subred
        keys_visited = mp.key_set(visited_map)   # array_list con los nodos visitados

        kv_size = al.size(keys_visited)
        for j in range(kv_size):
            vid = al.get_element(keys_visited, j)

            # Si por algún motivo ya tenía subred, no lo pisamos
            if not mp.contains(node_to_subred, vid):
                mp.put(node_to_subred, vid, subred_id_counter)
                al.add_last(nodes_list, vid)

    # Hasta aquí ya tenemos:
    # - node_to_subred: nodo -> subred_id
    # - subred_to_nodes: subred_id -> array_list con nodos de esa subred

    total_subredes = subred_id_counter

    # --- 3. Construir la info detallada de cada subred ---
    subredes_info = al.new_list()

    for sid in range(1, total_subredes + 1):

        nodes_list = mp.get(subred_to_nodes, sid)
        if nodes_list is None:
            continue

        cant_nodos = al.size(nodes_list)

        # Si por alguna razón está vacía, la ignoramos
        if cant_nodos == 0:
            continue

        # --- 3.1 Calcular bounding box lat/lon y recolectar grullas únicas ---
        lat_min = None
        lat_max = None
        lon_min = None
        lon_max = None

        individuos_map = mp.new_map(1000, 0.7)  # set de IDs de grullas usando map

        for i in range(cant_nodos):
            nid = al.get_element(nodes_list, i)
            node = mp.get(nodes_map, nid)

            if node is None:
                continue

            lat = node.get("lat", "Unknown")
            lon = node.get("lon", "Unknown")

            if lat != "Unknown" and lon != "Unknown":
                if lat_min is None or lat < lat_min:
                    lat_min = lat
                if lat_max is None or lat > lat_max:
                    lat_max = lat
                if lon_min is None or lon < lon_min:
                    lon_min = lon
                if lon_max is None or lon > lon_max:
                    lon_max = lon

            # tags: lista de grullas que pasan por este nodo
            tags_list = node["tags"]
            tags_count = al.size(tags_list)

            for j in range(tags_count):
                grulla_id = al.get_element(tags_list, j)
                mp.put(individuos_map, grulla_id, True)

        # Si bounding box nunca se actualizó:
        if lat_min is None:
            lat_min = "Unknown"
            lat_max = "Unknown"
            lon_min = "Unknown"
            lon_max = "Unknown"

        total_individuos = mp.size(individuos_map)

        # --- 3.2 Obtener primeros 3 y últimos 3 nodos de la subred ---
        primeros_3_nodos = al.new_list()
        ultimos_3_nodos = al.new_list()

        limit_n = 3
        if cant_nodos < 3:
            limit_n = cant_nodos

        # Primeros 3 nodos
        for i in range(limit_n):
            nid = al.get_element(nodes_list, i)
            node = mp.get(nodes_map, nid)
            info_nodo = {
                "id": nid,
                "lat": node.get("lat", "Unknown"),
                "lon": node.get("lon", "Unknown")
            }
            al.add_last(primeros_3_nodos, info_nodo)

        # Últimos 3 nodos
        start_idx = cant_nodos - limit_n
        for i in range(start_idx, cant_nodos):
            nid = al.get_element(nodes_list, i)
            node = mp.get(nodes_map, nid)
            info_nodo = {
                "id": nid,
                "lat": node.get("lat", "Unknown"),
                "lon": node.get("lon", "Unknown")
            }
            al.add_last(ultimos_3_nodos, info_nodo)

        # --- 3.3 Obtener primeros 3 y últimos 3 IDs de grullas de la subred ---
        primeros_3_grullas = al.new_list()
        ultimos_3_grullas = al.new_list()

        ids_grullas_al = mp.key_set(individuos_map)
        cant_grullas = al.size(ids_grullas_al)

        limit_g = 3
        if cant_grullas < 3:
            limit_g = cant_grullas

        # primeros 3
        for i in range(limit_g):
            gid = al.get_element(ids_grullas_al, i)
            al.add_last(primeros_3_grullas, gid)

        # últimos 3
        start_g = cant_grullas - limit_g
        for i in range(start_g, cant_grullas):
            gid = al.get_element(ids_grullas_al, i)
            al.add_last(ultimos_3_grullas, gid)

        # --- 3.4 Construir descriptor de subred ---
        subred_info = {
            "subred_id": sid,
            "num_puntos": cant_nodos,
            "lat_min": lat_min,
            "lat_max": lat_max,
            "lon_min": lon_min,
            "lon_max": lon_max,
            "primeros_3_puntos": primeros_3_nodos,
            "ultimos_3_puntos": ultimos_3_nodos,
            "total_individuos": total_individuos,
            "primeros_3_grullas": primeros_3_grullas,
            "ultimos_3_grullas": ultimos_3_grullas
        }

        al.add_last(subredes_info, subred_info)


    def cmp_subred_mas_grande(a, b):
        return a["num_puntos"] > b["num_puntos"]

    subredes_ordenadas = al.merge_sort(subredes_info, cmp_subred_mas_grande)

    total_subredes = al.size(subredes_ordenadas)

    # 5 subredes más grandes
    limit_comp = 5
    if total_subredes < 5:
        limit_comp = total_subredes

    top_subredes = al.sub_list(subredes_ordenadas, 0, limit_comp)

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return {
        "num_subredes": total_subredes,
        "subredes_top": top_subredes,
        "tiempo_ms": tiempo_ms
    }


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
