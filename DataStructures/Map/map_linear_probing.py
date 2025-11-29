from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
import random


def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(num_elements / load_factor)
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)

    table = al.new_list()
    elem = []
    for i in range(capacity):
        entry = me.new_map_entry(None, None)
        elem.append(entry)
    table["elements"] = elem
    table["size"] = capacity

    retorno = {
        "prime": prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0,
    }
    return retorno


def is_available(table, pos):
    entry = al.get_element(table, pos)
    key = me.get_key(entry)
    return (key is None) or (key == "__EMPTY__")


def default_compare(key, entry):
    key1 = me.get_key(entry)
    if key == key1:
        return 0
    elif key > key1:
        return 1
    else:
        return -1


def find_slot(my_map, key, hash_value):
    c = my_map["capacity"]
    t = my_map["table"]

    available = None
    s = hash_value

    for i in range(c):
        idx = (s + i) % c  
        if is_available(t, idx):
            if available is None:
                available = idx
            entry = al.get_element(t, idx)
            if me.get_key(entry) is None:
                return False, available
        else:
            entry = al.get_element(t, idx)
            if default_compare(key, entry) == 0:
                return True, idx

    return False, available


def rehash(my_map):
    old_elements = my_map["table"]["elements"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    new_table = al.new_list()
    new_list_elems = []
    for i in range(new_capacity):
        new_entry = me.new_map_entry(None, None)
        new_list_elems.append(new_entry)
    new_table["elements"] = new_list_elems
    new_table["size"] = new_capacity

    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    for i in range(old_capacity):
        entry = old_elements[i]
        k = me.get_key(entry)
        if (k is not None) and (k != "__EMPTY__"):
            put(my_map, k, me.get_value(entry))

    return my_map


def put(my_map, key, value):
    h = mf.hash_value(my_map, key)
    occupied, index = find_slot(my_map, key, h)
    table = my_map["table"]

    if occupied:
        entry = al.get_element(table, index)
        me.set_value(entry, value)
    else:
        new_entry = me.new_map_entry(key, value)
        table["elements"][index] = new_entry
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)

    return my_map


def get(my_map, key):
    h = mf.hash_value(my_map, key)
    occupied, index = find_slot(my_map, key, h)
    if occupied:
        entry = al.get_element(my_map["table"], index)
        return me.get_value(entry)
    return None


def contains(my_map, key):
    h = mf.hash_value(my_map, key)
    occupied, index = find_slot(my_map, key, h)
    return occupied


def remove(my_map, key):
    h = mf.hash_value(my_map, key)
    occupied, index = find_slot(my_map, key, h)
    if occupied:
        entry = al.get_element(my_map["table"], index)
        old_val = me.get_value(entry)
        me.set_key(entry, "__EMPTY__")
        me.set_value(entry, "__EMPTY__")
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        return old_val
    else:
        return None


def size(my_map):
    return my_map["size"]


def is_empty(my_map):
    return my_map["size"] == 0


def key_set(my_map):
    keys = al.new_list()
    for i in range(my_map["capacity"]):
        entry = my_map["table"]["elements"][i]
        key = me.get_key(entry)
        if key is not None and key != "__EMPTY__":
            al.add_last(keys, key)
    return keys


def value_set(my_map):
    values = al.new_list()
    for i in range(my_map["capacity"]):
        entry = my_map["table"]["elements"][i]
        key = me.get_key(entry)
        if key is not None and key != "__EMPTY__":
            al.add_last(values, me.get_value(entry))
    return values
