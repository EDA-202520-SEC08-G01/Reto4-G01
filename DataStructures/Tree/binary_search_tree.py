from DataStructures.Tree import bst_node as bsn
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll


def new_map():
    
    retorno = {
        "root": None
    }
    
    return retorno

def insert_node(root, key, value):
    if root is None:
        return bsn.new_node(key, value)
    if key < bsn.get_key(root):
        root["left"] = insert_node(root["left"], key, value)
    elif key > bsn.get_key(root):
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value  
    
    return root

def put(my_bst, key, value):
    my_bst["root"] = insert_node(my_bst["root"], key, value)
    return my_bst

def get(my_bst, key):
    current = my_bst["root"]
    while current is not None:
        current_key = bsn.get_key(current)
        if key == current_key:
            return bsn.get_value(current)
        elif key < current_key:
            current = current["left"]
        else:
            current = current["right"]
    return None

def size_tree(root):
    if root is None:
        return 0
    return 1 + size_tree(root["left"]) + size_tree(root["right"])

def size(my_bst):
    return size_tree(my_bst["root"])

def contains(my_bst, key):
    return get(my_bst, key) is not None

def is_empty(my_bst):
    return size(my_bst) == 0

def key_set_tree(root, keys):
    retorno = sll.new_list()
    if root is not None:
        key_set_tree(root["left"], keys)
        sll.add_last(retorno, bsn.get_key(root))
        key_set_tree(root["right"], keys)
    return retorno

def key_set(my_bst):
    keys = sll.new_list()
    key_set_tree(my_bst["root"], keys)
    return keys

def value_set_tree(root, values):
    retorno = sll.new_list()
    if root is not None:
        value_set_tree(root["left"], values)
        sll.add_last(retorno, bsn.get_value(root))
        value_set_tree(root["right"], values)
    return retorno

def value_set(my_bst):
    values = sll.new_list()
    value_set_tree(my_bst["root"], values)
    return values

def get_min_node(root):
    current = root
    while current["left"] is not None:
        current = current["left"]
    return current

def get_min(my_bst):
    if my_bst["root"] is None:
        return None
    min_node = get_min_node(my_bst["root"])
    return (bsn.get_key(min_node), bsn.get_value(min_node))

def get_max_node(root):
    current = root
    while current["right"] is not None:
        current = current["right"]
    return current

def get_max(my_bst):
    if my_bst["root"] is None:
        return None
    max_node = get_max_node(my_bst["root"])
    return (bsn.get_key(max_node), bsn.get_value(max_node))

def delete_min_tree(root):
    if root is None:
        return None
    if root["left"] is None:
        return root["right"]
    root["left"] = delete_min_tree(root["left"])
    return root

def delete_min(my_bst):
    if my_bst["root"] is not None:
        my_bst["root"] = delete_min_tree(my_bst["root"])
    return my_bst

def delete_max_tree(root):
    if root is None:
        return None
    if root["right"] is None:
        return root["left"]
    root["right"] = delete_max_tree(root["right"])
    return root

def delete_max(my_bst):
    if my_bst["root"] is not None:
        my_bst["root"] = delete_max_tree(my_bst["root"])
    return my_bst

def height_tree(root):
    if root is None:
        return -1
    left_height = height_tree(root["left"])
    right_height = height_tree(root["right"])
    return 1 + max(left_height, right_height)

def height(my_bst):
    return height_tree(my_bst["root"])

def keys_range(root, key_initial, key_final, key):
    retorno = sll.new_list()
    if root is not None:
        current_key = bsn.get_key(root)
        if key_initial < current_key:
            left_keys = keys_range(root["left"], key_initial, key_final, key)
            for k in sll.iterate(left_keys):
                sll.add_last(retorno, k)
        if key_initial <= current_key <= key_final:
            sll.add_last(retorno, current_key)
        if current_key < key_final:
            right_keys = keys_range(root["right"], key_initial, key_final, key)
            for k in sll.iterate(right_keys):
                sll.add_last(retorno, k)
    return retorno

def keys(my_bst, key_initial, key_final):
    return keys_range(my_bst["root"], key_initial, key_final, key_initial)
                      
def values_range(root, key_initial, key_final, list_value):
    retorno = sll.new_list()
    if root is not None:
        current_key = bsn.get_key(root)
        if key_initial < current_key:
            left_values = values_range(root["left"], key_initial, key_final, list_value)
            for v in sll.iterate(left_values):
                sll.add_last(retorno, v)
        if key_initial <= current_key <= key_final:
            sll.add_last(retorno, bsn.get_value(root))
        if current_key < key_final:
            right_values = values_range(root["right"], key_initial, key_final, list_value)
            for v in sll.iterate(right_values):
                sll.add_last(retorno, v)
    return retorno

def values(my_bst, key_initial, key_final):
    return values_range(my_bst["root"], key_initial, key_final, sll.new_list())

