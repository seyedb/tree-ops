
class tree(object):

    def __init__(self, root=None):
        self.root = root

    class treeNode(object):
        # visit status
        UNVISITED = 0
        VISITED = 1
        VISITING = 2

        def __init__(self, data, left=None, right=None, visited=UNVISITED):
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
        print(type(node))
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
