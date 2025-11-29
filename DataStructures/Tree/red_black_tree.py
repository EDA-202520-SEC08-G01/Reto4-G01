from DataStructures.Tree import rbt_node as rbn
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll

def new_map():
    my_map = {}
    my_map["root"] = None
    my_map["type"] = "RBT"
    return my_map

def default_compare(key1, key2):
    if key1 < key2:
        return -1
    elif key1 > key2:
        return 1
    else:
        return 0
    
def rotate_left(node):
    if node is None or node["right"] is None:
        return node
    
    new_root = node["right"]
    node["right"] = new_root["left"]
    new_root["left"] = node
    return new_root

def rotate_right(node):
    if node is None or node["left"] is None:
        return node
    
    new_root = node["left"]
    node["left"] = new_root["right"]
    new_root["right"] = node
    return new_root

def flip_colors(node):
    if node is None:
        return
    node["color"] = rbn.RED
    if node["left"]:
        node["left"]["color"] = rbn.BLACK
    if node["right"]:
        node["right"]["color"] = rbn.BLACK
        
def flip_node_color(node):
    if node is None:
        return
    if node["color"] == rbn.RED:
        node["color"] = rbn.BLACK
    else:
        node["color"] = rbn.RED
        
def is_red(node):
    if node is None:
        return False
    return node["color"] == rbn.RED

def size_tree(root):
    if root is None:
        return 0
    return root["size"]

def insert_node(root, key, value):
    if root is None:
        return rbn.new_rbt_node(key, value, rbn.RED)
    
    cmp = default_compare(key, root["key"])
    if cmp < 0:
        root["left"] = insert_node(root["left"], key, value)
    elif cmp > 0:
        root["right"] = insert_node(root["right"], key, value)
    else:
        root["value"] = value

    if is_red(root["right"]) and not is_red(root["left"]):
        root = rotate_left(root)
    if is_red(root["left"]) and is_red(root["left"]["left"]):
        root = rotate_right(root)
    if is_red(root["left"]) and is_red(root["right"]):
        flip_colors(root)

    root["size"] = 1 + size_tree(root["left"]) + size_tree(root["right"])
    return root

def put(my_rbt, key, value):
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    my_rbt["root"]["color"] = rbn.BLACK
    
    return my_rbt

def get(my_rbt, key):
    return get_node(my_rbt["root"], key)

def get_node(node, key):
    k = rbn.get_key(node)
    if node is None:
        return None
    elif k > key:
        return get_node(node["right"], key)
    elif k < key:
        return get_node(node["left"], key)
    elif k == key:
        return rbn.get_value(node)
    else:
        return None

def remove(my_rbt, key):
    my_rbt["root"] = remove_node(my_rbt["root"], key)
    return my_rbt

def remove_node(node, key):
    if node is None:
        return node
    k = rbn.get_key(node)

    if k > key:
        node["right"] = remove_node(node["right"], key)
    elif k < key:
        node["left"] = remove_node(node["left"], key)
    elif k == key:
        if node["right"] is None:
            temp = node["left"]
        else:
            temp = node["right"]
        if temp is None:
            return None
        temp = get_min_node(temp)
        node = get_node(node, temp)
        return node
    else:
        return node

def get_min(my_rbt):
    min = get_min_node(my_rbt["root"])
    return rbn.get_key(min)

def get_min_node(node):
    if node is None:
        return None
    elif node["left"] is None:
        return node
    else:
        return get_min_node(node["left"])

def contains(my_rbt, key):
    return get(my_rbt, key) is not None

def size(my_rbt):
    return size_tree(my_rbt["root"])

def size_tree(node):
    if node is None:
        return 0
    return 1 + size_tree(node["left"]) + size_tree(node["right"])

def is_empty(my_rbt):
    return my_rbt["root"] is None

def key_set(my_rbt):
    return key_set_tree(my_rbt["root"], key_list=al.new_list())

def key_set_tree(node, key_list):
    if node is not None:
        key_set_tree(node["left"], key_list)
        al.add_last(key_list, rbn.get_key(node))
        key_set_tree(node["right"], key_list)
    return key_list

def get_max_node(node):
    if node is None:
        return None
    if node["right"] is None:
        return node
    else:
        return get_max_node(node["right"])

def get_max(my_bst):
    nodo = get_max_node(my_bst["root"])
    return rbn.get_key(nodo)

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
        current_key = rbn.get_key(root)
        if key_initial < current_key:
            left_keys = keys_range(root["left"], key_initial, key_final, key)
            node = left_keys["first"]
            while node is not None:
                sll.add_last(retorno, node["info"])
                node = node["next"]
        if key_initial <= current_key <= key_final:
            sll.add_last(retorno, current_key)
        if current_key < key_final:
            right_keys = keys_range(root["right"], key_initial, key_final, key)
            node = right_keys["first"]
            while node is not None:
                sll.add_last(retorno, node["info"])
                node = node["next"]
    return retorno

def keys(my_bst, key_initial, key_final):
    return keys_range(my_bst["root"], key_initial, key_final, key_initial)
                      
def floor(my_rbt, key):
    return floor_key(my_rbt["root"], key)

def floor_key(node, key):
    if node is None:
        return None
    k = rbn.get_key(node)
    if k == key:
        return k
    elif k > key:
        return floor_key(node["left"], key)
    else:
        check = floor_key(node["right"], key)
        if check is not None:
            return check
        return k
        
def ceiling(my_rbt, key):
    return ceiling_key(my_rbt["root"], key)

def ceiling_key(node, key):
    if node is None:
        return None
    k = rbn.get_key(node)
    if k == key:
        return k
    elif k < key:
        return ceiling_key(node["right"], key)
    else:
        check = ceiling_key(node["left"], key)
        if check is not None:
            return check
        return k
    
def value_set_tree(node, value_list):
    if node is not None:
        value_set_tree(node["left"], value_list)
        al.add_last(value_list, rbn.get_value(node))
        value_set_tree(node["right"], value_list)
    return value_list

def value_set(my_rbt):
    return value_set_tree(my_rbt["root"], value_list=al.new_list())

def rank_keys(root, key):
    if root is None:
        return 0
    cmp = default_compare(key, rbn.get_key(root))
    if cmp < 0:
        return rank_keys(root["left"], key)
    elif cmp > 0:
        return 1 + size_tree(root["left"]) + rank_keys(root["right"], key)
    else:
        return size_tree(root["left"])
    
def rank(my_rbt, key):
    return rank_keys(my_rbt["root"], key)

def select_key(root, rank):
    if root is None:
        return None
    l_size = size_tree(root["left"])
    if rank < l_size:
        return select_key(root["left"], rank)
    elif rank > l_size:
        return select_key(root["right"], rank - l_size - 1)
    else:
        return rbn.get_key(root)
    
def select(my_rbt, rank):
    return select_key(my_rbt["root"], rank)

# aparentemente falto left key y right key, pero es usar para left key min node y right key max node (creo) y pues ponerlas aca xd
# lo dejo asi pq me voy a dormir muchachoides
def values_range(root, key_initial, key_final, value_list):
    if root is not None:
        current_key = rbn.get_key(root)
        if key_initial < current_key:
            values_range(root["left"], key_initial, key_final, value_list)
        if key_initial <= current_key <= key_final:
            al.add_last(value_list, rbn.get_value(root))
        if current_key < key_final:
            values_range(root["right"], key_initial, key_final, value_list)
    return value_list

def values(my_rbt, key_initial, key_final):
    return values_range(my_rbt["root"], key_initial, key_final, value_list=al.new_list())

def left_key(my_rbt):
    min_key = get_min_node(my_rbt["root"])
    return rbn.get_key(min_key)

def right_key(my_rbt):
    max_key = get_max_node(my_rbt["root"])
    return rbn.get_key(max_key)