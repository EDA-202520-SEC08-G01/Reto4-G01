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
from DataStructures.Stack import stack as st

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

def load_data(catalog, filename):
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
            if tag_str.isdigit():
                tag = int(tag_str)
            else:
                tag = tag_str

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

    node_count = 0

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
        
        for j in range(al.size(nodes_list)):
            node = al.get_element(nodes_list, j)
            
            # Calcular distancia temporal y espacial
            dt_hours = abs(
                (ev_time - node["creation_timestamp"]).total_seconds()
            ) / 3600.0
            
            d_km = haversine(
                node["lat"],
                node["lon"],
                ev_lat,
                ev_lon
            )
            
            # Verificar si cumple AMBAS condiciones
            if d_km < 3.0 and dt_hours < 3.0:
                nodo_encontrado = node
                break  # Tomar el PRIMER nodo que cumpla
        
        if nodo_encontrado is not None:
            # Agregar evento al nodo existente
            al.add_last(nodo_encontrado["events"], ev)
            nodo_encontrado["events_count"] += 1

            # Agregar tag si no existe
            tags_list = nodo_encontrado["tags"]
            found = False
            for j in range(al.size(tags_list)):
                if al.get_element(tags_list, j) == ev_tag:
                    found = True
                    break
            if not found:
                al.add_last(tags_list, ev_tag)

            # Actualizar promedio de distancia al agua
            c = nodo_encontrado["events_count"]
            old_avg = nodo_encontrado["prom_distancia_agua"]
            nodo_encontrado["prom_distancia_agua"] = (
                old_avg * (c - 1) + ev_dist_agua
            ) / c

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

            node_count += 1

    total_nodos = al.size(nodes_list)
    total_grullas = mp.size(tags_map)

    # ARCOS DEL GRAFO

    last_node_by_tag = mp.new_map(total_grullas + 1, 0.7)
    dist_migratoria = mp.new_map(total_nodos + 1, 0.7)
    dist_hidrica = mp.new_map(total_nodos + 1, 0.7)

    for i in range(total_eventos):
        ev = al.get_element(events, i)
        tag = ev["tag"]
        ev_id = ev["event-id"]

        node_id = mp.get(event_to_node, ev_id)
        prev_node_id = mp.get(last_node_by_tag, tag)

        if prev_node_id is None:
            mp.put(last_node_by_tag, tag, node_id)
            continue

        # CAMBIO: Crear arco INCLUSO si node_id == prev_node_id
        if True:  
            node_prev = mp.get(nodes_by_id, prev_node_id)
            node_curr = mp.get(nodes_by_id, node_id)

        # Solo crear arco si son nodos DIFERENTES
        if node_id != prev_node_id:
            d_km = haversine(
                node_prev["lat"], node_prev["lon"],
                node_curr["lat"], node_curr["lon"]
            )

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

    # Agregar arcos
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

    total_arcos_distance = dg.order(g_dist)
    total_arcos_water = dg.order(g_water)

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
        total_arcos_distance,
        total_arcos_water,
        primeros_5,
        ultimos_5
    )


# Funciones de consulta sobre el catálogo
def req_1(catalog, migr_origin, migr_dest):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1

    start = get_time()
    graph = catalog["graph_distance"]
    structure = djk.dijsktra(graph, migr_origin)

    if not djk.has_path_to(migr_dest, structure):
        end = get_time()
        tiempo_ms = delta_time(start, end)
        return (
            al.new_list(),   
            math.inf,        
            0,              
            al.new_list(),   
            al.new_list(),   
            tiempo_ms
        )
    
    path = djk.path_to(migr_dest, structure)
    total_dist = djk.dist_to(migr_dest, structure["visited"])

    path_al = al.new_list()
    for i in range(lt.size(path)):
        al.add_last(path_al, lt.get_element(path, i)["info"])

    i_primeros_5 = al.new_list()
    i_ultimos_5 = al.new_list()
    primeros_5 = al.new_list()
    ultimos_5 = al.new_list()
    total_nodos = lt.size(path)

    if total_nodos > 0:

        limite = min(5, total_nodos)
        for i in range(limite):
            al.add_last(i_primeros_5, lt.get_element(path, i)["info"])

        limite2 = min(5, total_nodos)
        inicio_ultimos = total_nodos - limite2
        for i in range(inicio_ultimos, total_nodos):
            al.add_last(i_ultimos_5, lt.get_element(path, i)["info"])
        
        for i in i_primeros_5["elements"]:
            al.add_last(primeros_5, mp.get(catalog["nodes_by_id"], i))

        for i in i_ultimos_5["elements"]:
            al.add_last(ultimos_5, mp.get(catalog["nodes_by_id"], i))

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return path_al, total_dist, lt.size(path), primeros_5, ultimos_5, tiempo_ms

def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    REQ 3: Identificar posibles rutas migratorias dentro del nicho biológico
    Usando Orden Topológico (DFO) sobre el grafo de todos los puntos migratorios.
    """

    start = get_time()
    graph = catalog["graph_distance"]     # grafo del nicho biológico
    nodes_map = catalog["nodes_by_id"]    # id_nodo -> info_nodo
    structure = dfo.dfo(graph)
    reversepost = structure["reversepost"]    # stack

    if st.size(reversepost) == 0:
        end = get_time()
        return {
            "total_puntos": 0,
            "total_individuos": 0,
            "primeros_5": al.new_list(),
            "ultimos_5": al.new_list(),
            "tiempo_ms": delta_time(start, end)
        }

    # Pasar reversepost (stack) a un array_list en orden topológico 
    order = al.new_list()          # la ruta migratoria
    aux_stack = st.new_stack()

    # invertimos el stack en aux_stack
    while st.size(reversepost) > 0:
        v = st.pop(reversepost)
        st.push(aux_stack, v)

    # reconstruimos reversepost y llenamos order en el orden correcto
    while st.size(aux_stack) > 0:
        v = st.pop(aux_stack)
        st.push(reversepost, v)
        al.add_last(order, v)

    total_puntos = al.size(order)

    # --- 3. Calcular total de individuos únicos que usan la ruta ---
    individuos_set = mp.new_map(5000, 0.7)   # mapa id_grulla -> True

    for i in range(total_puntos):
        nid = al.get_element(order, i)
        node = mp.get(nodes_map, nid)

        tags_list = node["tags"]            # array_list de IDs de grulla
        tags_count = al.size(tags_list)

        for j in range(tags_count):
            grulla_id = al.get_element(tags_list, j)
            mp.put(individuos_set, grulla_id, True)

    total_individuos = mp.size(individuos_set)

    # --- 4. Construir lista enriquecida de puntos migratorios ---
    pts_mig = al.new_list()

    for i in range(total_puntos):

        nid = al.get_element(order, i)
        node = mp.get(nodes_map, nid)

        lat = node.get("lat", "Unknown")
        lon = node.get("lon", "Unknown")

        tags_list = node["tags"]            # array_list
        tags_count = al.size(tags_list)

        # -------- TRES primeros y TRES últimos identificadores de grullas --------
        # primeras 3
        primeras_3 = al.new_list()
        limit_first = 3
        if tags_count < 3:
            limit_first = tags_count

        for k in range(limit_first):
            grulla_id = al.get_element(tags_list, k)
            al.add_last(primeras_3, grulla_id)

        # últimas 3
        ultimas_3 = al.new_list()
        limit_last = 3
        if tags_count < 3:
            limit_last = tags_count

        start_idx = tags_count - limit_last
        for k in range(start_idx, tags_count):
            grulla_id = al.get_element(tags_list, k)
            al.add_last(ultimas_3, grulla_id)

        # -------- Distancia a vecinos en la ruta migratoria --------
        dist_prev = "Unknown"
        dist_next = "Unknown"

        # distancia al vértice anterior en la ruta migratoria
        if i > 0:
            prev_id = al.get_element(order, i - 1)
            prev_node = mp.get(nodes_map, prev_id)
            dist_prev = haversine(node, prev_node)

        # distancia al vértice siguiente en la ruta migratoria
        if i < total_puntos - 1:
            next_id = al.get_element(order, i + 1)
            next_node = mp.get(nodes_map, next_id)
            dist_next = haversine(node, next_node)

        # -------- Descripción del punto migratorio --------
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

        al.add_last(pts_mig, desc)

    # --- 5. Sacar los CINCO primeros y CINCO últimos vértices de la RUTA ---
    limit = 5
    if total_puntos < 5:
        limit = total_puntos

    # sub_list(list, pos_i, num_elements)
    primeros_5 = al.sub_list(pts_mig, 0, limit)
    ultimos_5 = al.sub_list(pts_mig, total_puntos - limit, limit)

    end = get_time()
    tiempo_ms = delta_time(start, end)

    return {
        "total_puntos": total_puntos,
        "total_individuos": total_individuos,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5,
        "tiempo_ms": tiempo_ms
    }

def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

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
