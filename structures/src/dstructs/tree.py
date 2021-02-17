from enum import Enum
from collections import deque

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
        def __init__(self, data, left=None, right=None, status=node_status.UNVISITED):
            '''
            Initializes a tree node
            A tree node has a value, a left child, a right child, and a visit status
            '''
            self.data = data
            self.left = left
            self.right = right
            self.status = status

        def _getStatus(self):
            '''
            A function to get the visit status of a tree node
            
            returns:
                (node_status) visit status of the given node
            '''
            if self is not None:
                return self.status
            else:
                print('Hit null node!')
    
        def _setStatus(self, status):
            '''
            A function to set the visit status of a tree node
    
            args:
                status (node_status): the new visit status to be assigned to the node
            returns:
                (treeNode) the input tree node with its visit status updated
            '''
            if self is not None:
                self.status = status
            else:
                print('Hit null node!')

    def __str__(self):
        '''
        A function to print a tree starting from its root
        '''
        if self.root is not None:
            self._printTree(self.root)
        print("\n")

    def _printTree(self, node):
        '''
        A helper function for printing a tree starting from a given node

        args:
            node (treeNode): the tree node at which the printing starts 
        '''
        if node is not None:
            self._printTree(node.left)
            print("{} ".format(node.data),end="")
            self._printTree(node.right)

    def add_node(self, data):
        '''
        Adds a node to a tree.

        args:
            data (node val data type): the value to be assigned to the new tree node
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self._addNode(self.root, data)

    def _addNode(self, node, data):
        '''
        A helper function that finds the right location for the new node according to BST rule.

        args:
            data (node val data type): the value to be assigned to the new node
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

    def inorder_traversal(self, node, path=None):
        '''
        Inorder Traversal 

        args:
            node (treeNode): the tree node at with the inorder traversal starts
            path (list of treeNode): the traversal path 
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
            (list of treeNode) the full traversal path 
        '''
        if path is None:
            path = []

        if node is not None:
            path = self.inorder_traversal(node.left, path)
            node._setStatus(node_status.VISITED)
            path.append(node)
            path = self.inorder_traversal(node.right, path)

        return path

    def preorder_traversal(self, node, path=None):
        '''
        Preorder Traversal 

        args:
            node (treeNode): the tree node at with the preorder traversal starts
            path (list of treeNode): the traversal path
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
            (list of treeNode) the full traversal path 
        '''
        if path is None:
            path = []

        if node is not None:
            node._setStatus(node_status.VISITED)
            path.append(node)
            path = self.preorder_traversal(node.left, path)
            path = self.preorder_traversal(node.right, path)

        return path

    def postorder_traversal(self, node, path=None):
        '''
        Postorder Traversal 

        args:
            node (treeNode): the tree node at with the postorder traversal starts
            path (list of treeNode): the traversal path
        returns:
            (tree) the input tree with all its nodes visited once while traversing 
                   all nodes have visit status VISITED at this point
            (list of treeNode) the full traversal path 
        '''
        if path is None:
            path = []

        if node is not None:
            path = self.postorder_traversal(node.left, path)
            path = self.postorder_traversal(node.right, path)
            node._setStatus(node_status.VISITED)
            path.append(node)

        return path

    def find_node(self, data):
        '''
        Finds a node in a tree
        
        args:
            data (node val data type): the data to be found in the tree
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
            data (node val data type): the data to be found in the tree
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

    def DFS(self, start, path):
        '''
        Depth-First Search (DFS)

        args:
            start (node val data type): the key value of the node where the search starts
            path (list of treeNode): the DFS path (empty path to be filled with nodes)
        returns:
            (list of treeNode) the full DFS path
        '''
        s = self.find_node(start)
        if s is None:
            return

        if len(path) == 0: path.append(s)

        s._setStatus(node_status.VISITED)

        children = []
        if s.left is not None: children.append(s.left)
        if s.right is not None: children.append(s.right)

        for child in children:
            if child._getStatus() == node_status.UNVISITED:
                path.append(child)
                self.DFS(child.data, path)

    def BFS(self, start):
        '''
        Breadth-First Search (BFS)

        args:
            start (node val data type): the key value of the node where the search starts
        returns:
            (list of treeNode) the full BFS path
        '''
        s = self.find_node(start)
        if s is None:
            return
        s._setStatus(node_status.VISITED)
        path = []

        Q = deque()
        Q.append(s)
        while Q:
            k = Q.popleft()

            children = []
            if k.left is not None: children.append(k.left)
            if k.right is not None: children.append(k.right)
            for child in children:
                if child._getStatus() == node_status.UNVISITED:
                    child._setStatus(node_status.VISITED)
                    Q.append(child)

            k._setStatus(node_status.VISITED)
            path.append(k)

        return path

    def is_balanced(self):
        '''
        Checks whether or not a BST is balanced

        returns:
            (bool) True is the tree is balanced, False otherwise
        '''
        return self._isBalanced(self.root) > -1

    def _isBalanced(self, node):
        '''
        A helper function to check if a BST is balanced
        
        args:
            node (treeNode): the tree node where the recursive procedure starts
        returns:
            (int) -1 if the tree (subtree) is not balanced, otherwise returns the height of the tree (subtree)
        '''
        if node is None:
            return 0

        lheight = self._isBalanced(node.left)
        if lheight == -1: return -1

        rheight = self._isBalanced(node.right)
        if rheight == -1: return -1

        if abs(lheight - rheight) > 1: return -1

        return max(lheight, rheight) + 1

