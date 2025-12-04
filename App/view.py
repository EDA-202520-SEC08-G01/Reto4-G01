import sys
from DataStructures.List import array_list as al
from tabulate import tabulate
from App import logic as l

def new_logic():
    """
        Se crea una instancia del controlador
    """

    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    return l.new_logic()

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Carga los datos
    """

    nombre_archivo = str(input("Ingrese el nombre del archivo de datos (Ejemplo: '1000_cranes_mongolia_small.csv'): \n"))
    catalog,tiempo_ms,total_grullas,total_eventos,total_nodos,total_arcos_distance,total_arcos_water,primeros_5,ultimos_5 = l.load_data(control,nombre_archivo)

    headers = ["Identificador Único","Posición","Fecha de creación","Grullas (tags)","Conteo","Prom. dist. agua (km)"]

    tabla_primeros = []
    tabla_ultimos = []

    for i in primeros_5["elements"]:
        tabla_primeros.append([i['id'],
                              (i['lat'], i['lon']),
                              i['creation_timestamp'],
                              i['tags']["elements"],
                              i["events_count"],
                              i['prom_distancia_agua']])
    
    for i in ultimos_5["elements"]:
        tabla_ultimos.append([i['id'],
                              (i['lat'], i['lon']),
                              i['creation_timestamp'],
                              i['tags']["elements"],
                              i["events_count"],
                              i['prom_distancia_agua']])

    print("==========================================================")
    print("                      Carga de datos                      ")
    print("==========================================================")

    print("==--- Información cargada ---==")
    print("Número de grullas reconocidas: ", total_grullas)
    print("Número de eventos cargados: ", total_eventos)
    print("Número de nodos cargados en el grafo: ", total_nodos)
    print("Número de arcos de distancia cargados (total arcos): ", total_arcos_distance)
    print("Número de arcos de agua cargados (total arcos): ", total_arcos_water)
    print("Tiempo [ms]: ", tiempo_ms)

    print("========================================================== \n")
    print("==--- Primeros 5 elementos del catálogo ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print("==--- Últimos 5 elementos del catálogo ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")

    return catalog
    




def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    
    migr_origin = str(input("Ingrese el identificador único del origen de la migracion: "))
    migr_dest = str(input("Ingrese el identificador único del destino de la migracion: "))

    path_al, distancia_nodos, tamano, primeros_5, ultimos_5, tiempo_ms = l.req_1(control, migr_origin, migr_dest)

    headers = ["Identificador Único","Posición","Fecha de creación","Grullas (tags)","Conteo","Prom. dist. agua (km)"]

    tabla_primeros = []
    tabla_ultimos = []

    for i in primeros_5["elements"]:
        tabla_primeros.append([i["id"],
                              (i['lat'], i['lon']),
                              i['creation_timestamp'],
                              i['tags']["elements"],
                              i["events_count"],
                              i['prom_distancia_agua']])
    
    for i in ultimos_5["elements"]:
        tabla_ultimos.append([i['id'],
                              (i['lat'], i['lon']),
                              i['creation_timestamp'],
                              i['tags']["elements"],
                              i["events_count"],
                              i['prom_distancia_agua']])
    
    ruta = ""
    for i in range(al.size(path_al)):
        ruta += al.get_element(path_al, i)
        if i < al.size(path_al) - 1:
            ruta += " -> "

    print("==========================================================")
    print("                      Requerimiento 1                     ")
    print("==========================================================")

    print("==--- Información cargada ---==")
    print("Ruta Tomada (mejor ruta): ", ruta)
    print("Distancia entre nodos: ", distancia_nodos)
    print("Numero de puntos en la ruta: ", tamano)
    print("Tiempo [ms]: ", tiempo_ms)

    print("========================================================== \n")
    print("==--- Primeros 5 elementos del catálogo ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print("==--- Últimos 5 elementos del catálogo ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print()


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    # Pedir datos al usuario
    lat_origin = float(input("Ingrese la LATITUD del punto de origen: "))
    lon_origin = float(input("Ingrese la LONGITUD del punto de origen: "))
    lat_dest = float(input("Ingrese la LATITUD del punto de destino: "))
    lon_dest = float(input("Ingrese la LONGITUD del punto de destino: "))
    radio_km = float(input("Ingrese el radio del área de interés (en km): "))

    (
        origin_id,
        dest_id,
        last_inside_id,
        path_ids,
        total_dist,
        num_nodes_path,
        _primeros_5_nodes,   # no los usamos aquí
        _ultimos_5_nodes,    # idem
        tiempo_ms
    ) = l.req_2(control, lat_origin, lon_origin, lat_dest, lon_dest, radio_km)

    # Si no hay camino
    if num_nodes_path == 0:
        print("==========================================================")
        print("                      Requerimiento 2                     ")
        print("==========================================================")
        print(f"No se reconoce un camino viable entre {origin_id} y {dest_id}.")
        print("Tiempo [ms]: ", tiempo_ms)
        print("========================================================== \n")
        return

    # Reconstruir lista de nodos (diccionarios) en el camino
    nodes_list = control["nodes"]
    path_nodes = []

    for i in range(al.size(path_ids)):
        node_id = al.get_element(path_ids, i)
        encontrado = None
        for node in nodes_list["elements"]:
            if node["id"] == node_id:
                encontrado = node
                break
        if encontrado is not None:
            path_nodes.append(encontrado)

    # Construir string de la ruta (IDs)
    ruta = ""
    for i, node in enumerate(path_nodes):
        ruta += node["id"]
        if i < len(path_nodes) - 1:
            ruta += " -> "

    # ==== IMPRESIÓN DE LA INFORMACIÓN GENERAL (lo que pide el enunciado) ====
    print("==========================================================")
    print("                      Requerimiento 2                     ")
    print("==========================================================")
    print("Punto migratorio de ORIGEN más cercano: ", origin_id)
    print("Punto migratorio de DESTINO más cercano: ", dest_id)
    print(f"Último nodo dentro del radio de {radio_km} km: ", last_inside_id)
    #print("Ruta tomada: ", ruta)
    print("Distancia total del camino (km): ", total_dist)
    print("Número de puntos en la ruta: ", num_nodes_path)
    print("Tiempo [ms]: ", tiempo_ms)

    # ==== TABLAS DE 5 PRIMEROS Y 5 ÚLTIMOS NODOS ====

    headers = [
        "ID nodo",
        "Posición (lat, lon)",
        "Fecha de creación",
        "# grullas",
        "Tags (3_P)",
        "Tags (3_U)",
        "Prom. dist. agua [km]",
        "Dist. sig. nodo [km]"
    ]

    tabla_primeros = []
    tabla_ultimos = []

    def info_tags(node):
        tags_list = node["tags"]["elements"]
        num_grullas = len(tags_list)
        if num_grullas == 0:
            primeros3 = []
            ultimos3 = []
        elif num_grullas <= 3:
            primeros3 = tags_list
            ultimos3 = tags_list
        else:
            primeros3 = tags_list[:3]
            ultimos3 = tags_list[-3:]
        return num_grullas, primeros3, ultimos3

    def formatear_posicion(node):
        return f"{node['lat']:.5f}, {node['lon']:.5f}"

    def formatear_tags(tags):
        if not tags:
            return "—"
        return ", ".join(str(t) for t in tags)

    # Primeros 5 puntos migratorios
    limite = min(5, len(path_nodes))
    for i in range(limite):
        node = path_nodes[i]
        num_grullas, primeros3, ultimos3 = info_tags(node)

        # Distancia al siguiente nodo en la ruta
        if i < len(path_nodes) - 1:
            next_node = path_nodes[i + 1]
            dist_next = l.haversine(
                node["lat"], node["lon"],
                next_node["lat"], next_node["lon"]
            )
            dist_next_str = f"{dist_next:.3f}"
        else:
            dist_next_str = "—"

        tabla_primeros.append([
            node["id"],
            formatear_posicion(node),
            node["creation_timestamp"],
            num_grullas,
            formatear_tags(primeros3),
            formatear_tags(ultimos3),
            f"{node['prom_distancia_agua']:.4f}",
            dist_next_str
        ])

    # Últimos 5 puntos migratorios

    total_nodos_camino = len(path_nodes)
    # Tomar los últimos 5 (o menos, si hay menos de 5)
    last_nodes = path_nodes[-5:] if total_nodos_camino >= 5 else path_nodes

    for idx, node in enumerate(last_nodes):
        # índice real del nodo dentro de path_nodes
        original_index = total_nodos_camino - len(last_nodes) + idx

        num_grullas, primeros3, ultimos3 = info_tags(node)

        # Distancia al siguiente nodo en la ruta (hay siguiente
        # solo si NO es el último nodo global del camino)
        if original_index < total_nodos_camino - 1:
            next_node = path_nodes[original_index + 1]
            dist_next = l.haversine(
                node["lat"], node["lon"],
                next_node["lat"], next_node["lon"]
            )
            dist_next_str = f"{dist_next:.3f}"
        else:
            dist_next_str = "—"

        tabla_ultimos.append([
            node["id"],
            formatear_posicion(node),
            node["creation_timestamp"],
            num_grullas,
            formatear_tags(primeros3),
            formatear_tags(ultimos3),
            f"{node['prom_distancia_agua']:.4f}",
            dist_next_str
        ])

    print("========================================================== \n")
    print("==--- Primeros 5 puntos migratorios en la ruta ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print("==--- Últimos 5 puntos migratorios en la ruta ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print()
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3

    total_puntos, total_invididuos, primeros_5, ultimos_5, tiempo_ms = l.req_3(control)

    headers = ["Identificador Único","Posición","Numero de individuos","Primeras tres grullas","Ultimas tres grullas","Distancia al punto anterior (km)","Distancia al siguiente punto (km)"]

    tabla_primeros = []
    tabla_ultimos = []

    for i in primeros_5["elements"]:
        tabla_primeros.append([i['id'],
                              (i['lat'], i['lon']),
                              i['num_individuos'],
                              i['primeras_3_grullas']["elements"],
                              i['ultimas_3_grullas']["elements"],
                              i['distancia_anterior'],
                              i['distancia_siguiente']])
    
    for i in ultimos_5["elements"]:
        tabla_ultimos.append([i['id'],
                              (i['lat'], i['lon']),
                              i['num_individuos'],
                              i['primeras_3_grullas']["elements"],
                              i['ultimas_3_grullas']["elements"],
                              i['distancia_anterior'],
                              i['distancia_siguiente']])

    print("==========================================================")
    print("                      Requerimiento 3                     ")
    print("==========================================================")

    print("==--- Información cargada ---==")
    print("Total de puntos migratorios: ", total_puntos)
    print("Total de invididuos: ", total_invididuos)
    print("Tiempo [ms]: ", tiempo_ms)

    print("========================================================== \n")
    print("==--- Primeros 5 elementos del catálogo ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print("==--- Últimos 5 elementos del catálogo ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print()


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    lat_origin = float(input("Ingrese la LATITUD del punto de origen: "))
    lon_origin = float(input("Ingrese la LONGITUD del punto de origen: "))
    lat_dest = float(input("Ingrese la LATITUD del punto de destino: "))
    lon_dest = float(input("Ingrese la LONGITUD del punto de destino: "))

    print("\nSeleccione el tipo de grafo a utilizar:")
    print("  1 - Grafo por distancia de desplazamiento")
    print("  2 - Grafo por distancias a fuentes hídricas")
    tipo_grafo = input("Ingrese 1 o 2 (o escriba 'distancia' / 'agua'): ")

    (
        origin_id,
        dest_id,
        total_cost,
        num_vertices,
        num_arcos,
        path_ids,
        segment_costs,
        _primeros_5_nodes,   # no los usamos aquí
        _ultimos_5_nodes,    # idem
        tiempo_ms
    ) = l.req_5(control, lat_origin, lon_origin, lat_dest, lon_dest, tipo_grafo)

    # Si no hay camino
    if num_vertices == 0 or al.size(path_ids) == 0:
        print("==========================================================")
        print("                      Requerimiento 5                     ")
        print("==========================================================")
        print(f"No se reconoce un camino viable entre {origin_id} y {dest_id}.")
        print("Tiempo [ms]: ", tiempo_ms)
        print("========================================================== \n")
        return

    # Reconstruir lista de nodos en el camino (diccionarios)
    nodes_list = control["nodes"]
    path_nodes = []

    for i in range(al.size(path_ids)):
        node_id = al.get_element(path_ids, i)
        encontrado = None
        for node in nodes_list["elements"]:
            if node["id"] == node_id:
                encontrado = node
                break
        if encontrado is not None:
            path_nodes.append(encontrado)

    # Construir string de la ruta a partir de los IDs
    ruta = ""
    for i in range(al.size(path_ids)):
        nid = al.get_element(path_ids, i)
        ruta += nid
        if i < al.size(path_ids) - 1:
            ruta += " -> "

    # Descripción del tipo de costo
    tipo = str(tipo_grafo).lower().strip()
    if tipo.startswith("2") or tipo.startswith("a"):
        desc_costo = "Costo total (distancia a fuentes hídricas)"
    else:
        desc_costo = "Costo total (distancia de desplazamiento)"

    # ==== IMPRESIÓN DE LA INFORMACIÓN GENERAL ====
    print("==========================================================")
    print("                      Requerimiento 5                     ")
    print("==========================================================")
    print("Punto migratorio de ORIGEN más cercano: ", origin_id)
    print("Punto migratorio de DESTINO más cercano: ", dest_id)
    #print("Ruta óptima identificada: ", ruta)
    print(desc_costo + ": ", total_cost)
    print("Número de puntos (vértices) en la ruta: ", num_vertices)
    print("Número de segmentos (arcos) en la ruta: ", num_arcos)
    print("Tiempo [ms]: ", tiempo_ms)

    # ==== TABLAS DE 5 PRIMEROS Y 5 ÚLTIMOS NODOS ====

    headers = [
        "ID nodo",
        "Posición (lat, lon)",
        "Fecha de creación",
        "# grullas",
        "Tags (3 primeros)",
        "Tags (3 últimos)",
        "Prom. dist. agua [km]",
        "Costo sig. segmento"
    ]

    tabla_primeros = []
    tabla_ultimos = []

    def info_tags(node):
        tags_list = node["tags"]["elements"]
        num_grullas = len(tags_list)
        if num_grullas == 0:
            primeros3 = []
            ultimos3 = []
        elif num_grullas <= 3:
            primeros3 = tags_list
            ultimos3 = tags_list
        else:
            primeros3 = tags_list[:3]
            ultimos3 = tags_list[-3:]
        return num_grullas, primeros3, ultimos3

    def formatear_posicion(node):
        return f"{node['lat']:.5f}, {node['lon']:.5f}"

    def formatear_tags(tags):
        if not tags:
            return "—"
        return ", ".join(str(t) for t in tags)

    # ===== Primeros 5 puntos migratorios =====
    total_nodos_camino = len(path_nodes)
    limite = min(5, total_nodos_camino)

    for i in range(limite):
        node = path_nodes[i]
        num_grullas, primeros3, ultimos3 = info_tags(node)

        # costo al siguiente segmento (según el grafo elegido)
        costo_seg = al.get_element(segment_costs, i)
        costo_seg_str = f"{costo_seg:.3f}" if i < num_vertices - 1 else "—"

        tabla_primeros.append([
            node["id"],
            formatear_posicion(node),
            node["creation_timestamp"],
            num_grullas,
            formatear_tags(primeros3),
            formatear_tags(ultimos3),
            f"{node['prom_distancia_agua']:.4f}",
            costo_seg_str
        ])

    # ===== Últimos 5 puntos migratorios =====
    last_nodes = path_nodes[-5:] if total_nodos_camino >= 5 else path_nodes

    for idx, node in enumerate(last_nodes):
        # índice real dentro de path_nodes / segment_costs
        original_index = total_nodos_camino - len(last_nodes) + idx

        num_grullas, primeros3, ultimos3 = info_tags(node)

        if original_index < num_vertices - 1:
            costo_seg = al.get_element(segment_costs, original_index)
            costo_seg_str = f"{costo_seg:.3f}"
        else:
            costo_seg_str = "—"

        tabla_ultimos.append([
            node["id"],
            formatear_posicion(node),
            node["creation_timestamp"],
            num_grullas,
            formatear_tags(primeros3),
            formatear_tags(ultimos3),
            f"{node['prom_distancia_agua']:.4f}",
            costo_seg_str
        ])

    print("========================================================== \n")
    print("==--- Primeros 5 puntos migratorios en la ruta ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print("==--- Últimos 5 puntos migratorios en la ruta ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("========================================================== \n")
    print()
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
