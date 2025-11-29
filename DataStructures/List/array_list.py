def new_list():
    
    new_list = {
        "first": None,
        "elements": [],
        "size": 0,
    }
    return new_list

def get_element(my_list, index):
    
    return my_list["elements"][index]

def is_present(my_list, element, cmp_function):
    
    size = my_list["size"]
    if size == 0:
        keyexist = False
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(info, element) == 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    
def size(my_list):
    return my_list["size"] 

def first_element(my_list):
    if my_list["size"] > 0:
        return my_list["elements"][0]
    else:
        return None

def last_element(my_list):
    if my_list["size"] > 0:
        return my_list["elements"][-1]
    else:
        return None

def remove_first(my_list):
      if my_list["size"] == 0:
        return "IndexError: list index out of range"
      eliminado = my_list["elements"][0]
      del my_list["elements"][0]
      my_list["size"] -= 1
      return eliminado

def remove_last(my_list):
    if my_list["size"] == 0:
        return "IndexError: list index out of range"
    else:
        eliminado = my_list["elements"][-1]
        del my_list["elements"][-1]
        my_list["size"] -= 1
        return eliminado

def insert_element(my_list, pos, element):
    if pos < 0 or pos >= my_list["size"]:
        return "IndexError: list index out of range"
    else:
        my_list["elements"].insert(pos, element)
        my_list["size"] += 1 
        return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list["size"]:
        return "IndexError: list index out of range"
    my_list["elements"][pos] = new_info
    return my_list
        
def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list["size"]) or (pos_2 < 0 or pos_2 >= my_list["size"]):
        return "IndexError: list index out of range"
    
    my_list["elements"][pos_1], my_list["elements"][pos_2] = (
        my_list["elements"][pos_2], 
        my_list["elements"][pos_1]
    )
    
    return my_list
        
def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list["size"]:
        return "IndexError: list index out of range"
    
    end_pos = pos_i + num_elements
    if end_pos > my_list["size"]:
        end_pos = my_list["size"]
    
    sub_elements = my_list["elements"][pos_i:end_pos]
    
    return {
        "size": len(sub_elements),
        "elements": sub_elements
    }
    
    
def is_empty(my_list):
    return my_list["size"] == 0

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        return "IndexError: list index out of range"
    del my_list["elements"][pos]
    my_list["size"] -= 1
    return my_list

def default_sort_criteria(element_1, element_2):
    is_sorted = False
    if element_1 < element_2:
        is_sorted=True
    return is_sorted

def selection_sort(my_list,sort_crit):
    s = size(my_list)
    for i in range(s - 1):
        mejor = i
        for j in range(i + 1, s):
            if sort_crit(get_element(my_list, j),get_element(my_list, mejor)):
                mejor = j
        if mejor != i:
            exchange(my_list, i, mejor)
        
    return my_list 

def insertion_sort(my_list, sort_crit):
    n = size(my_list)
    for i in range(1, n):
        key = get_element(my_list, i)
        j = i - 1
        while j >= 0 and not sort_crit(get_element(my_list, j), key):
            exchange(my_list, j + 1, get_element(my_list, j))
            j -= 1
        exchange(my_list, j + 1, key)

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
    i = j = 0

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
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = get_element(list, i)
            j = i
            while j >= gap and not sort_crit(get_element(list, j - gap), temp):
                exchange(list, j, get_element(list, j - gap))
                j -= gap
            exchange(list, j, temp)
        gap //= 2

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

