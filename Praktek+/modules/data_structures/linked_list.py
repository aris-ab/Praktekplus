# modules/data_structures/linked_list.py
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def is_empty(self):
        return self.head is None
    
    def append(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, key):
        current = self.head
        
        # If head node itself holds the key
        if current and current.data == key:
            self.head = current.next
            return True
        
        # Search for the key and delete
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        
        if current is None:
            return False
        
        prev.next = current.next
        return True
    
    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return current.data
            current = current.next
        return None
    
    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements