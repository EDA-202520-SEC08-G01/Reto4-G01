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
    print("\n=== Ingrese los parámetros para el Requerimiento 2 ===")
    origin_lat = float(input("Ingrese la latitud del punto de origen: "))
    origin_lon = float(input("Ingrese la longitud del punto de origen: "))
    dest_lat = float(input("Ingrese la latitud del punto de destino: "))
    dest_lon = float(input("Ingrese la longitud del punto de destino: "))
    radius_km = float(input("Ingrese el radio del área de interés en km: "))
    
    # Ejecutar requerimiento
    result = l.req_2(control, origin_lat, origin_lon, dest_lat, dest_lon, radius_km)
    
    # Verificar si hay camino
    if result["path"] is None:
        print("\n==========================================================")
        print("                      Requerimiento 2                     ")
        print("==========================================================")
        print(f"\n{result['message']}")
        print(f"Tiempo [ms]: {result['time_ms']:.3f}")
        print("==========================================================\n")
        return
    
    # Preparar tablas
    headers = ["Identificador Único", "Posición (lat, lon)", "Num. Grullas", 
               "Primeras 3 grullas", "Últimas 3 grullas", "Dist. siguiente (km)"]
    
    tabla_primeros = []
    tabla_ultimos = []
    
    # Procesar primeros 5 nodos
    for i in range(al.size(result["first_5"])):
        node_info = al.get_element(result["first_5"], i)
        tabla_primeros.append([
            node_info["id"],
            f"({node_info['lat']:.5f}, {node_info['lon']:.5f})",
            node_info["num_individuals"],
            node_info["first_3_tags"],
            node_info["last_3_tags"],
            node_info["distance_to_next"]
        ])
    
    # Procesar últimos 5 nodos
    for i in range(al.size(result["last_5"])):
        node_info = al.get_element(result["last_5"], i)
        tabla_ultimos.append([
            node_info["id"],
            f"({node_info['lat']:.5f}, {node_info['lon']:.5f})",
            node_info["num_individuals"],
            node_info["first_3_tags"],
            node_info["last_3_tags"],
            node_info["distance_to_next"]
        ])
    
    # Crear string de la ruta completa
    ruta = ""
    for i in range(al.size(result["path"])):
        ruta += str(al.get_element(result["path"], i))
        if i < al.size(result["path"]) - 1:
            ruta += " -> "
    
    # Mensaje del último nodo en el área
    if result["last_node_in_area"] is not None:
        mensaje_area = f"El último nodo dentro del área de interés (radio {radius_km} km) es: {result['last_node_in_area']}"
    else:
        mensaje_area = f"Ningún nodo del camino se encuentra dentro del área de interés (radio {radius_km} km)"
    
    # Imprimir resultados
    print("\n==========================================================")
    print("                      Requerimiento 2                     ")
    print("==========================================================")
    
    print("\n==--- Información de la consulta ---==")
    print(f"Nodo de origen encontrado: {result['origin_node']}")
    print(f"Nodo de destino encontrado: {result['dest_node']}")
    print(f"Radio del área de interés: {result['radius_km']} km")
    print(f"\n{mensaje_area}")
    
    print("\n==--- Información del camino ---==")
    print(f"Distancia total de desplazamiento: {result['total_distance']:.3f} km")
    print(f"Número de puntos en la ruta: {result['total_nodes']}")
    print(f"Tiempo de ejecución [ms]: {result['time_ms']:.3f}")
    
    print("\n==--- Ruta completa (primeros nodos) ---==")
    ruta_preview = " -> ".join([str(al.get_element(result["path"], i)) 
                                 for i in range(min(10, al.size(result["path"])))])
    if al.size(result["path"]) > 10:
        ruta_preview += " -> ..."
    print(ruta_preview)
    
    print("\n==========================================================")
    print("==--- Primeros 5 puntos migratorios de la ruta ---==")
    print(tabulate(tabla_primeros, headers=headers, tablefmt="fancy_grid", stralign="center"))
    
    print("\n==========================================================")
    print("==--- Últimos 5 puntos migratorios de la ruta ---==")
    print(tabulate(tabla_ultimos, headers=headers, tablefmt="fancy_grid", stralign="center"))
    print("==========================================================\n")
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
    print("                      Requerimiento 1                     ")
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
