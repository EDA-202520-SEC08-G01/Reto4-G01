from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sl

def new_queue():
    new_queue = al.new_list()
    return new_queue

#def new_queue2():
#    new_queue = sl.new_list()
 #   return new_queue

def enqueue(my_queue, element):
    enqueue = al.add_last(my_queue, element)
    return enqueue
    
#def enqueuelinked(my_queue, element):
 #   if my_queue["size"] == 0:
  #      raise Exception("EmptyStructureError: queue is empty")
   # else:
    #    enqueue = sl.add_last(my_queue, element)
     #   return element

def dequeue(my_queue):
    if my_queue["size"] == 0:
        raise Exception("EmptyStructureError: queue is empty")
    else:
        dequeue = al.remove_first(my_queue)
        return dequeue

#def dequeuelinked(my_queue):
 #   if my_queue["size"] == 0:
  #      raise Exception("EmptyStructureError: queue is empty")
   # else:
    #    dequeue = sl.remove_first(my_queue)
     #   return dequeue
    
def is_empty(my_queue):
    return al.is_empty(my_queue)

#def is_emptylinked(my_queue):
 #   return sl.is_empty(my_queue)

def peek(my_queue):
    if my_queue["size"] == 0:
        raise Exception("EmptyStructureError: queue is empty")
    else:
        peek = al.first_element(my_queue)
        return peek
    
#def peeklinked(my_queue):
 #   if my_queue["size"] == 0:
  #      raise Exception("EmptyStructureError: queue is empty")
   # else:
    #    peek = sl.first_element(my_queue)
     #   return peek
    
def size(my_queue):
    size = al.size(my_queue)
    return size

#def sizelinked(my_queue):
 #   size = sl.size(my_queue)
  #  return size

