from enum import Enum

class node_status(Enum):
    '''
    List of all possible visit status of each node (tree traversal)
    '''
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class tree(object):
    '''
    The main (binary search) tree class
    '''
    def __init__(self, root=None):
        '''
        Initializes a tree with its root node
        '''
        self.root = root

    class treeNode(object):
        '''
        The main tree node class (defined as an inner class of the tree class)
        '''
        def __init__(self, data, left=None, right=None, visited=node_status.UNVISITED):
            '''
            Initializes a tree node
            A tree node has a value, a left child, a right child, and a visit status
            '''
            self.data = data
            self.left = left
            self.right = right
            self.visited = visited

    def __str__(self):
        '''
        A function to print a tree starting from its root
        '''
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        '''
        A helper function for printing a tree starting from a given node

        args:
            node (treeNode): the tree node at which the printing starts 
        '''
        if node is not None:
            self._printTree(node.left)
            print(node.data)
            self._printTree(node.right)

    def add_node(self, data):
        '''
        Adds a node to a tree.

        args:
            data (any type): the value to be assigned to the new tree node
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
        if self.root == None:
            self.root = self.treeNode(data)
        else:
            self._addNode(self.root, data)

    def _addNode(self, node, data):
        '''
        A helper function that finds the right location for the new node according to BST rule.

        args:
            data (any type): the value to be assigned to the new node
            node (treeNode): the node at which the recursive approach to insert a new node starts
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
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

    def _getStatus(self, node):
        '''
        A function to get the visit status of a tree node
        
        args:
            node (treeNode): a tree node
        returns:
            (node_status) visit status of the given node
        '''
        if node is not None:
            return node.visited
        else:
            print('Hit null node!')

    def _setStatus(self, node, visited):
        '''
        A function to set the visit status of a tree node

        args:
            node        (treeNode): a tree node
            visited (visit_status): the new visit status to be assigned to the node
        returns:
            (treeNode) the input tree node with its visit status updated
        '''
        if node is not None:
            node.visited = visited
        else:
            print('Hit null node!')

    def inorder_traversal(self, node):
        '''
        Inorder Traversal 

        args:
            node (treeNode): the tree node at with the inorder traversal starts
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
        '''
        if node is not None:
            self.inorder_traversal(node.left)
            self._setStatus(node, node_status.VISITED)
            self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        '''
        Preorder Traversal 

        args:
            node (treeNode): the tree node at with the preorder traversal starts
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
        '''
        if node is not None:
            self._setStatus(node, node_status.VISITED)
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        '''
        Postorder Traversal 

        args:
            node (treeNode): the tree node at with the postorder traversal starts
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
        '''
        if node is not None:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            self._setStatus(node, node_status.VISITED)

    def find_node(self, data):
        '''
        Finds a node in a tree
        
        args:
            data (any type): the data to be found in the tree
        returns:
            (treeNode) the tree node that contains the given data          
        '''
        if self.root is not None:
            return self._findNode(data, self.root)
        else:
            return None

    def _findNode(self, data, node):
        '''
        A helper function to find a given data in a tree
        
        args:
            data (any type): the data to be found in the tree
            node (treeNode): the node at which the recursive search begins
        returns:
            (treeNode) the tree node that contains the given data
        '''
        if node.data == data:
            return node
        elif (data < node.data and node.left is not None):
            return self._findNode(data, node.left)
        elif (data > node.data and node.right is not None):
            return self._findNode(data, node.right)


