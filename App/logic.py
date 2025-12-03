import time
import math
import csv
from datetime import datetime
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as dg
from DataStructures.Graph import dijsktra as djk
from DataStructures.List import single_linked_list as lt

def haversine_km(lat1, lon1, lat2, lon2):
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
            
            d_km = haversine_km(
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
            d_km = haversine_km(
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
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


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
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
