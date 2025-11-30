from DataStructures.List import single_linked_list as sll

def new_stack():
    return sll.new_list()

def push(stack, element):
    return sll.add_first(stack, element)  

def pop(stack):
    return sll.remove_first(stack)

def is_empty(stack):
    return sll.is_empty(stack)

def top(stack):
    return sll.first_element(stack)

def size(stack):
    return sll.size(stack)