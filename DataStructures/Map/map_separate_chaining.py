from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
import random


def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(num_elements / load_factor)
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)

    # cada bucket de la tabla será una lista encadenada vacía
    chains = []
    for i in range(capacity):
        chains.append(sll.new_list())

    retorno = {
        "prime": prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": chains,
        "current_factor": 0.0,
        "limit_factor": load_factor,
        "size": 0
    }
    return retorno


def default_compare(key, entry):
    ek = me.get_key(entry)
    if key == ek:
        return 0
    elif key > ek:
        return 1
    else:
        return -1


def put(my_map, key, value):
    h = mf.hash_value(my_map, key)
    chain = my_map["table"][h]

    # buscar si ya existe en la cadena
    for i in range(sll.size(chain)):
        entry = sll.get_element(chain, i)
        if default_compare(key, entry) == 0:
            me.set_value(entry, value)
            return my_map

    # no existe → añadir nodo nuevo
    new_entry = me.new_map_entry(key, value)
    sll.add_last(chain, new_entry)
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
    return my_map


def contains(my_map, key):
    h = mf.hash_value(my_map, key)
    chain = my_map["table"][h]
    for i in range(sll.size(chain)):
        entry = sll.get_element(chain, i)
        if default_compare(key, entry) == 0:
            return True
    return False


def get(my_map, key):
    h = mf.hash_value(my_map, key)
    chain = my_map["table"][h]
    for i in range(sll.size(chain)):
        entry = sll.get_element(chain, i)
        if default_compare(key, entry) == 0:
            return me.get_value(entry)
    return None


def remove(my_map, key):
    h = mf.hash_value(my_map, key)
    chain = my_map["table"][h]
    for i in range(sll.size(chain)):
        entry = sll.get_element(chain, i)
        if default_compare(key, entry) == 0:
            old_val = me.get_value(entry)
            sll.delete_element(chain, i)
            my_map["size"] -= 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]
            return old_val
    return None


def size(my_map):
    return my_map["size"]


def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = al.new_list()
    buckets = my_map["table"]["elements"]
    for i in range(my_map["capacity"]):
        bucket = buckets[i]
        node = bucket["first"]
        while node is not None:
            entry = node["info"]
            al.add_last(keys, me.get_key(entry))
            node = node["next"]
    return keys


def value_set(my_map):
    values = al.new_list()
    buckets = my_map["table"]["elements"]
    for i in range(my_map["capacity"]):
        bucket = buckets[i]
        node = bucket["first"]
        while node is not None:
            entry = node["info"]
            al.add_last(values, me.get_value(entry))
            node = node["next"]
    return values


def rehash(my_map):
    old_chains = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = mf.next_prime(old_capacity * 2)
    new_chains = []
    for i in range(new_capacity):
        new_chains.append(sll.new_list())

    my_map["capacity"] = new_capacity
    my_map["table"] = new_chains
    my_map["size"] = 0
    my_map["current_factor"] = 0.0

    for i in range(old_capacity):
        chain = old_chains[i]
        for j in range(sll.size(chain)):
            entry = sll.get_element(chain, j)
            put(my_map, me.get_key(entry), me.get_value(entry))

    return my_map
