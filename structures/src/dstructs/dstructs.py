from enum import Enum

class node_status(Enum):
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class tree(object):
    def __init__(self, root=None):
        self.root = root

    class treeNode(object):
        def __init__(self, data, left=None, right=None, visited=node_status.UNVISITED):
            self.data = data
            self.left = left
            self.right = right
            self.visited = visited

    def add_node(self, data):
        if self.root == None:
            self.root = self.treeNode(data)
        else:
            self._addNode(self.root, data)

    def _addNode(self, node, data):
        if data < node.data:
            if node.left is not None:
                self._addNode(node.left, data)
            else:
                node.left = self.treeNode(data)
        else:
            if node.right is not None:
                self._addNode(node.right, data)
            else:
                node.right = self.treeNode(data)

    def print_tree(self):
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        if node is not None:
            self._printTree(node.left)
            print(node.data)
            self._printTree(node.right)

    def _getStatus(self, node):
        if node is not None:
            return node.visited
        else:
            print('Hit null node!')

    def _setStatus(self, node, visited):
        if node is not None:
            node.visited = visited
        else:
            print('Hit null node!')

    def in_order_traversal(self, node):
        if node is not None:
            self.in_order_traversal(node.left)
            self._setStatus(node, node_status.VISITED)
            self.in_order_traversal(node.right)

    def pre_order_traversal(self, node):
        if node is not None:
            self._setStatus(node, node_status.VISITED)
            self.in_order_traversal(node.left)
            self.in_order_traversal(node.right)

    def post_order_traversal(self, node):
        if node is not None:
            self.in_order_traversal(node.left)
            self.in_order_traversal(node.right)
            self._setStatus(node, node_status.VISITED)


