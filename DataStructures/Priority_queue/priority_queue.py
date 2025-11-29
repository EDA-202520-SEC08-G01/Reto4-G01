from DataStructures.List import array_list as al
from DataStructures.Priority_queue import pq_entry as pqe


def default_compare_lower_value(father_node, child_node):
    if pqe.get_priority(father_node) <= pqe.get_priority(child_node):
        return True
    return False


def default_compare_higher_value(father_node, child_node):
    
    if pqe.get_priority(father_node) >= pqe.get_priority(child_node):
        return True
    return False


def new_heap(is_min_pq=True):

    heap = {
        "elements": al.new_list(),
        "size": 0,
        "cmp_function": default_compare_lower_value if is_min_pq else default_compare_higher_value
    }
    
    al.add_last(heap["elements"], None)
    
    return heap


def priority(my_heap, parent, child):

    return my_heap["cmp_function"](parent, child)


def swim(my_heap, pos):

    while pos > 1:
        parent_pos = pos // 2

        current_element = al.get_element(my_heap["elements"], pos)
        parent_element = al.get_element(my_heap["elements"], parent_pos)

        if priority(my_heap, parent_element, current_element):
            break

        al.change_info(my_heap["elements"], pos, parent_element)
        al.change_info(my_heap["elements"], parent_pos, current_element)
        
        pos = parent_pos


def insert(my_heap, priority_value, value):
    new_entry = pqe.new_pq_entry(priority_value, value)

    al.add_last(my_heap["elements"], new_entry)

    my_heap["size"] += 1

    swim(my_heap, my_heap["size"])
    
    return my_heap


def is_empty(my_heap):
    return my_heap["size"] == 0

def size(my_heap):
    return my_heap["size"]

def get_first_priority(my_heap):
    if is_empty(my_heap):
        return None
    first = al.get_element(my_heap["elements"], 1)
    return pqe.get_priority(first)

def sink(my_heap, pos):
    size = my_heap["size"]

    while 2 * pos <= size:
        left_child_pos = 2 * pos
        right_child_pos = 2 * pos + 1

        current_element = al.get_element(my_heap["elements"], pos)
        left_child_element = al.get_element(my_heap["elements"], left_child_pos)

        if right_child_pos <= size:
            right_child_element = al.get_element(my_heap["elements"], right_child_pos)

            if priority(my_heap, left_child_element, right_child_element):
                selected_child_pos = right_child_pos
                selected_child_element = right_child_element
            else:
                selected_child_pos = left_child_pos
                selected_child_element = left_child_element
        else:
            selected_child_pos = left_child_pos
            selected_child_element = left_child_element

        if priority(my_heap, current_element, selected_child_element):
            break

        al.change_info(my_heap["elements"], pos, selected_child_element)
        al.change_info(my_heap["elements"], selected_child_pos, current_element)

        pos = selected_child_pos

def remove(my_heap):
    if is_empty(my_heap):
        return None

    first_element = al.get_element(my_heap["elements"], 1)
    last_element = al.get_element(my_heap["elements"], my_heap["size"])

    al.change_info(my_heap["elements"], 1, last_element)
    al.remove_last(my_heap["elements"])

    my_heap["size"] -= 1

    sink(my_heap, 1)

    return pqe.get_value(first_element)

def contains(my_heap, value):
    for i in range(1, my_heap["size"] + 1):
        current_element = al.get_element(my_heap["elements"], i)
        if pqe.get_value(current_element) == value:
            return True
    return False

def is_present_value(my_heap, value):
    if is_empty(my_heap):
        return -1

    for i in range(1, my_heap["size"] + 1):
        current_element = al.get_element(my_heap["elements"], i)
        if pqe.get_value(current_element) == value:
            return i

    return -1

def exchange(my_heap, pos_a, pos_b):
    element_a = al.get_element(my_heap["elements"], pos_a)
    element_b = al.get_element(my_heap["elements"], pos_b)

    al.change_info(my_heap["elements"], pos_a, element_b)
    al.change_info(my_heap["elements"], pos_b, element_a)

def improve_priority(my_heap, priority_value, value):
    pos = is_present_value(my_heap, value)
    if pos == -1:
        return -1

    current_element = al.get_element(my_heap["elements"], pos)
    current_priority = pqe.get_priority(current_element)

    if priority_value >= current_priority:
        return -1

    new_element = pqe.new_pq_entry(priority_value, value)
    al.change_info(my_heap["elements"], pos, new_element)

    swim(my_heap, pos)

    return pos