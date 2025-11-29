from DataStructures.List import list_node as ns


def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0,
    }
    
    return newlist

def add_first(list, element):
    n = ns.new_single_node(element)
    if list["last"] == None:
        list["last"] = n
    n["next"] = list["first"]
    list["first"] = n
    list["size"] += 1
    return list
    

def add_last(list, element):
    n = ns.new_single_node(element)
    if list["first"] == None:
        list["first"] = n
    if list["last"] == None:
        list["last"] = n
    else:
        list["last"]["next"] = n
        list["last"] = n
    list["size"] += 1
    return list

def size(list):
    return list["size"]

def first_element(list):
    if is_empty(list):
        raise Exception("Error, indexacion fuera de rango: No hay elementos para leer")
    else:
        n = list["first"]
        return n["info"]
    
def last_element(list):
    if is_empty(list):
        raise Exception("Error, indexacion fuera de rango: No hay elementos para leer")
    else:
        n = list["last"]
        return n["info"]

def is_empty(list):
    return list["size"] == 0
    
def get_element(list, pos):
    n = list["first"] # indexacion 0
    for i in range(pos):
        n = n["next"]
    return n

def remove_first(list):
    if is_empty(list):
        raise Exception("Error: Indexación fuera de rango -> list['first'] != NoneType")
    n = list["first"]
    list["first"] = n["next"]
    list["size"] -= 1
    return n["info"]
        
def remove_last(list):
   if is_empty(list):
       raise Exception("Error: Indexación fuera de rango -> list['last'] != NoneType")
   n = list["first"]
   last = list["last"]
   
   if n == last:
       list["first"] = None
       list["last"] = None
       list["size"] = 0
       return last["info"]
   
   while n["next"] == last:
       n = n["next"]

   list["last"] = n
   list["last"]["next"] = None
   list["size"] -= 1
   return last["info"]

def insert_element(list, element, pos):
    if 0 <= pos <= size(list):
       node = ns.new_single_node(element)
       if is_empty(list):
         raise Exception("Error: Indexación fuera de rango -> Solo existe la posicion 0, pero el arreglo esta vacio.")
       node_anterior = list["first"]
       for i in range(pos-1):
            node_anterior = node_anterior["next"]
       node["next"] = node_anterior["next"]
       node_anterior["next"] = node
       return list
    else:
        raise Exception('IndexError: list index out of range') # esto esta en la documentacion de DISC - Data Structures btw
        
        
def is_present(list, element, cmp_function):
    node = ns.new_single_node(element)
    if is_empty(list):
         raise Exception("Error: Indexación fuera de rango -> No existe ningun elemento, el arreglo esta vacio.")
    nodo_buscar = list["first"]
    existe = False
    while nodo_buscar["next"] != None:
        if cmp_function(node["info"], nodo_buscar["info"]) == 0:
            existe = True
        nodo_buscar = nodo_buscar["next"]
        index += 1
    if existe:
        return index
    else:
        return -1
    
    
def delete_element(list, pos):
    if 0 <= pos <= size(list):
        if is_empty(list):
           raise Exception("Error: Indexación fuera de rango -> No se puede borrar elementos si no existe ninguno que borrar.")
        n_anterior = list["first"]
    
        for i in range(pos-1):
            n_anterior = n_anterior["next"]
            
        if n_anterior["next"] == None:
            list["first"] = None
            list["Last"] = None
            list["Size"] = 0
            return list
        else:
            n_borrar = n_anterior["next"]
            n_anterior["next"] = n_borrar["next"]
            list["size"] -= 1
            return list
    else:
        raise Exception('IndexError: list index out of range') # esto esta en la documentacion de DISC - Data Structures btw x2
        
def change_info(list, pos, new_info):
    if 0 <= pos <= size(list):
        if is_empty(list):
            raise Exception("Error: Indexación fuera de rango -> No se puede borrar elementos si no existe ninguno que borrar.")
        n_cambio = list["first"]
        for i in range(pos):
            n_cambio = n_cambio["next"]
        n_cambio["info"] = new_info
        return list
    else:
        raise Exception('IndexError: list index out of range') # esto esta en la documentacion de DISC - Data Structures btw x3

def exchange(list, pos1, pos2):
        if not(0 <= pos1 <= size(list) and 0 <= pos2 <= size(list)):
            raise Exception('IndexError: list index out of range') # esto esta en la documentacion de DISC - Data Structures btw x3
        if is_empty(list):
            raise Exception("Error: Indexación fuera de rango -> No se puede borrar elementos si no existe ninguno que borrar.")
        enc_p1_prev = list["first"]
        enc_p2_prev = list["first"]
        for i in range(pos1-1):
            enc_p1_prev = enc_p1_prev["next"]
        for i in range(pos2-1):
            enc_p2_prev = enc_p2_prev["next"]
        
        p1 = enc_p1_prev["next"]
        p2 = enc_p2_prev["next"]
        
        if p1["next"]==None:
            p1["next"] = p2["next"]
            p2["next"] = None
        elif p2["next"]==None:
            p2["next"] = p1["next"]
            p1["next"] = None
        
        enc_p2_prev["next"] = p1
        enc_p1_prev["next"] = p2
        return list

def sub_list(list, pos, num_elements):
    if not(0 <= pos <= size(list)):
            raise Exception('IndexError: list index out of range') # esto esta en la documentacion de DISC - Data Structures btw x3
    if is_empty(list):
            raise Exception("Error: Indexación fuera de rango -> No se puede borrar elementos si no existe ninguno que borrar.")
    sub_list = new_list()
    ini_lista = list["first"]
    for i in range(pos):
        ini_lista = ini_lista["next"]
    
    sub_list["first"] = ini_lista
    sub_list["last"] = list["last"]
    sub_list["size"] = num_elements
    return sub_list
    
def default_sort_criteria(element_1, element_2):
   is_sorted = False
   if element_1 < element_2:
      is_sorted = True
   return is_sorted

def selection_sort(my_list,sort_crit):
    s = size(my_list)
    for i in range(s - 1):
        mejor = i
        for j in range(i + 1, s):
            if sort_crit(get_element(my_list, j),get_element(my_list, mejor)):
                mejor = j
        if mejor != i:
            change_info(my_list, i, mejor)
    
    return my_list

def insertion_sort(my_list, sort_crit):
    n = size(my_list)
    for i in range(1, n):
        key = get_element(my_list, i)
        j = i - 1
        while j >= 0 and not sort_crit(get_element(my_list, j), key):
            change_info(my_list, j + 1, get_element(my_list, j))
            j -= 1
        change_info(my_list, j + 1, key)

    return my_list

def merge_sort(list, sort_crit):
    if list["size"] <= 1:
        return list

    mid = list["size"] // 2
    left = sub_list(list, 0, mid)
    right = sub_list(list, mid, list["size"] - mid)

    left_sorted = merge_sort(left, sort_crit)
    right_sorted = merge_sort(right, sort_crit)

    return merge(left_sorted, right_sorted, sort_crit)


def merge(left, right, sort_crit):
    merged = new_list()
    i,j = 0,0

    while i < left["size"] and j < right["size"]:
        if sort_crit(get_element(left, i), get_element(right, j)):
            add_last(merged, get_element(left, i))
            i += 1
        else:
            add_last(merged, get_element(right, j))
            j += 1

    while i < left["size"]:
        add_last(merged, get_element(left, i))
        i += 1

    while j < right["size"]:
        add_last(merged, get_element(right, j))
        j += 1

    return merged

    
def shell_sort(list, sort_crit):
    n = size(list)
    mid = n // 2

    while mid > 0:
        for i in range(mid, n):
            curr = get_element(list, i)
            j = i
            while j >= mid and not sort_crit(get_element(list, j - mid), curr):
                change_info(list, j, get_element(list, j - mid))
                j -= mid
            change_info(list, j, curr)
        mid //= 2

    return list

def concatenar(list1, list2):
    # Concatena dos listas y retorna la nueva lista.
    retorno = new_list()
    for element in list1:
        add_last(retorno, element) # copia todos los elementos de list1
    for element in list2:
        add_last(retorno, element) # dsps copia todos los elementos de list2

    return retorno

def quick_sort(list, sort_crit):
    
    n = size(list)
    if n <= 1:
        return list
    
    pivote = get_element(list, 0) # -> El primer elemento es el pivote del quick sort

    # 3 particiones: menores, mayores, iguales al pivote
    antes_pivote = new_list()
    dsps_pivote = new_list()
    iguales = new_list()

    # En este ciclo se llenan las 3 particiones en dependencia de su relación con el pivote
    for i in range(n):
        curr = get_element(list, i)
        if curr == pivote:
            add_last(iguales, curr)
        elif sort_crit(curr, pivote):
            add_last(antes_pivote, curr)
        else:
            add_last(dsps_pivote, curr)


    # Se ordenan recursivamente las particiones de antes y después. Como iguales = pivote, iguales ya está ordenada (todos son el mismo elemento/número)
    antes_pivote_sort = quick_sort(antes_pivote, sort_crit)
    dsps_pivote_sort = quick_sort(dsps_pivote, sort_crit)

    # Se concatenan las 3 particiones y se retorna la lista ordenada: antes -> iguales -> después
    return concatenar(concatenar(antes_pivote_sort, iguales), dsps_pivote_sort)