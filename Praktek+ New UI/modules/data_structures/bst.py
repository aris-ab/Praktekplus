# modules/data_structures/bst.py
class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
    
    def insert(self, key, value):
        self.root = self._insert_recursive(self.root, key, value)
    
    def _insert_recursive(self, node, key, value):
        if node is None:
            return TreeNode(key, value)
        
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        else:
            node.right = self._insert_recursive(node.right, key, value)
        
        return node
    
    def search(self, key):
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node.value if node else None
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)