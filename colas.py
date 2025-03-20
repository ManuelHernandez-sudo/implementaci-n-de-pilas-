class Node:
    def __init__(self, data, priority=0):
        self.data = data
        self.priority = priority
        self.next = None

class Queue:
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self.count = 0

    def enqueue(self, element):
        new_node = Node(element)
        if self.is_empty():
            self.front_node = self.rear_node = new_node
        else:
            self.rear_node.next = new_node
            self.rear_node = new_node
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        removed_data = self.front_node.data
        self.front_node = self.front_node.next
        if self.front_node is None:
            self.rear_node = None
        self.count -= 1
        return removed_data

    def front(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.front_node.data

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

class PriorityQueue:
    def __init__(self):
        self.front_node = None
        self.count = 0

    def enqueue(self, element, priority):
        new_node = Node(element, priority)
        if self.is_empty() or priority > self.front_node.priority:
            new_node.next = self.front_node
            self.front_node = new_node
        else:
            current = self.front_node
            while current.next and current.next.priority >= priority:
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Priority Queue is empty")
        removed_data = self.front_node.data
        self.front_node = self.front_node.next
        self.count -= 1
        return removed_data

    def is_empty(self):
        return self.count == 0

    def size(self):
        return self.count

# Aplicación 1: Gestión de tareas con prioridad
task_queue = PriorityQueue()
task_queue.enqueue("Tarea Normal 1", 1)
task_queue.enqueue("Tarea Crítica", 3)
task_queue.enqueue("Tarea Normal 2", 1)

print("Procesando tareas en orden de prioridad:")
while not task_queue.is_empty():
    print(task_queue.dequeue())

# Aplicación 2: Atención al cliente con clientes VIP
customer_queue = PriorityQueue()
customer_queue.enqueue("Cliente Regular 1", 1)
customer_queue.enqueue("Cliente VIP", 2)
customer_queue.enqueue("Cliente Regular 2", 1)

print("\nAtendiendo clientes en orden de prioridad:")
while not customer_queue.is_empty():
    print(customer_queue.dequeue())