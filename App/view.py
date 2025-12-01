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
    


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

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
        tabla_primeros.append([i,
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
    print("                      Requerimiento 1                     ")
    print("==========================================================")

    print("==--- Información cargada ---==")
    print("Ruta Tomada (mejor ruta): ", path_al['elements'])
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
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


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
