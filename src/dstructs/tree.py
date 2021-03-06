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
        def __init__(self, data=None, status=node_status.UNVISITED, balance_factor=0):
            '''
            Initializes a tree node
            A tree node has a value, a left child, a right child, a visit status, parent node, 
            height of the tree rooted at the node, and balance factor (difference between the
            height of the left and the right subtrees)
            '''
            self.data = data
            self.left = None
            self.right = None
            self.status = status
            self.parent = None
            self.height = 0
            self.balance_factor = balance_factor

        def _getStatus(self):
            '''
            A function to get the visit status of a tree node
            
            returns:
                (node_status) visit status of the given node
            '''
            return self.status
    
        def _setStatus(self, status):
            '''
            A function to set the visit status of a tree node
    
            args:
                status (node_status): the new visit status to be assigned to the node
            returns:
                (treeNode) the input tree node with its visit status updated
            '''
            self.status = status

    def __str__(self):
        '''
        A function to print a tree starting from its root
        '''
        if self.root is not None:
            self._printTree(self.root)
        print("\n")

    def _printTree(self, node):
        '''
        A helper function for printing a tree starting from a given node all the way down

        args:
            node (treeNode): the tree node at which the printing starts 
        '''
        if node is not None:
            self._printTree(node.left)
            print("{} ".format(node.data),end="")
            self._printTree(node.right)

    def _getHeight(self, node):
        '''
        A helper function to get the height of the tree rooted at a given node

        returns:
            (int) tree height
        '''
        if node is not None:
            return node.height
        else:
            return -1

    def _updateHeight(self, node):
        '''
        A helper function to update the height of a given tree node

        returns:
            (treeNode) the imput tree node with updated height
        '''
        lheight = self._getHeight(node.left)
        rheight = self._getHeight(node.right)
        node.height = max(lheight, rheight) + 1

    def _updateBalanceFactor(self, node):
        '''
        A helper function to update the balance factor of a given tree node

        returns:
            (treeNode) the imput tree node with updated balance factor
        '''
        lheight = self._getHeight(node.left)
        rheight = self._getHeight(node.right)
        node.balance_factor = lheight - rheight

    def reset_status(self):
        '''
        A function to reset the visit status of all the nodes in a tree to UNVISITED
        '''
        self._resetStatus(self.root)

    def _resetStatus(self, node):
        '''
        A helper function to reset the visit status of each node below the given node to UNVISITED 
        after a traversal routine (in-, pre-, postorder, DFS, BFS) call, it is done recursively 
        following an in-order fashion

        args:
            node (treeNode): the tree node at which the procedure starts
        '''
        if node is not None:
            self._resetStatus(node.left)
            node._setStatus(node_status.UNVISITED)
            self._resetStatus(node.right)

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
            self.root = self._addNode(self.root, data)

    def _addNode(self, node, data):
        '''
        A helper function that finds the right location for the new node according to the BST-property.

        args:
            data (node val data type): the value to be assigned to the new node
            node (treeNode): the node at which the recursive approach to insert a new node starts
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
        if data < node.data:
            if node.left is not None:
                lnode = self._addNode(node.left, data)
            else:
                lnode = self.treeNode(data)

            node.left = lnode
            lnode.parent = node
        else:
            if node.right is not None:
                rnode = self._addNode(node.right, data)
            else:
                rnode = self.treeNode(data)

            node.right = rnode
            rnode.parent = node
        
        self._updateHeight(node)
        self._updateBalanceFactor(node)

        return node

    def insert_node(self, data):
        '''
        Inserts a node in a tree in level order (uses _insertNode with the root as the starting node) 
        (see documentation of _insertNode for more details)

        args:
            data (node val data type): the value to be assigned to the new tree node
        returns:
            (tree) tree updated with a new node
        '''
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self._insertNode(self.root, data)

    def _insertNode(self, node, data):
        '''
        A helper function that inserts a node in a binary tree (not necessarily BST) in level order 
        (breadth-first):
            traversing down the tree from the given starting point, if a node N is found whose left 
            node is empty, a new node with the given data is created as N.left, else if a node N is 
            found whose right node is empty, the new node is created as N.right. 

        args:
            data (node val data type): the value to be assigned to the new node
            node (treeNode): the node at which the traversal to insert a new node starts
        returns:
            (tree) tree updated with a new node 
        '''
        Q = deque()
        Q.append(node)

        while Q:
            node = Q.popleft()

            if node.left is None:
                lnode = self.treeNode(data)
                node.left = lnode
                lnode.parent = node
                break
            else:
                Q.append(node.left)

            if node.right is None:
                rnode = self.treeNode(data)
                node.right = rnode
                rnode.parent = node
                break
            else:
                Q.append(node.right)

        self._updateHeight(node)
        self._updateBalanceFactor(node)

        return node

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

    def DFS(self, start, path=None):
        '''
        Depth-First Search (DFS)

        args:
            start (node val data type): the key value of the node where the search starts
            path (list of treeNode): the DFS path (empty path to be filled with nodes)
        returns:
            (list of treeNode) the full DFS path
        '''
        if path is None:
            path = []

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
                path = self.DFS(child.data, path)

        return path
        
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
            (int) -1 if the tree (subtree) is not balanced, otherwise returns the height of the 
                  tree (subtree)
        '''
        if node is None:
            return 0

        lheight = self._isBalanced(node.left)
        if lheight == -1: return -1

        rheight = self._isBalanced(node.right)
        if rheight == -1: return -1

        if abs(lheight - rheight) > 1: return -1

        return max(lheight, rheight) + 1

    def balance_by_recursion(self):
        '''
        Converts a given binary tree (may or may not be BST) to a balanced binary tree by recursion 
        in the following steps:
            - creates a sorted list of nodes from the input tree using an inorder traversal path
            - constructs a balanced tree recursively from a sorted list of nodes:
                1- find the middle of the list and make it the root 
                2- get the middle left half of the list and make it the left node of the step 1
                3- get the middle right half of the list and make it the right node of the step 1

        returns:
            (tree) a balanced binary tree contating the data from a given binary tree
        '''
        balancedt = tree()
        path = self.inorder_traversal(self.root)
        # reset the visit status (can be avoided if visit status is removed as a node attribute) 
        for node in path:
            node._setStatus(node_status.UNVISITED)

        rnode = self._balanceByRecursion(path, 0, len(path) - 1)
        balancedt.root = rnode

        return balancedt

    def _balanceByRecursion(self, nodes, start, end):
        '''
        A helper function to convert a binary tree to a balanced binary tree by recursion. Performs
        the recursive step.

        args:
            nodes (treeNode): the portion of the node list over which a recursion step is taken
            start (int): the index of the left-most element of the list over which the currect step 
            of recursion is performed
            end (int): the index of the right-most element of the list over which the current step 
            of recursion is performed
        returns:
            (treeNode) the root node of the constructed balanced tree after recursion is completed
        '''
        if start > end:
            return None

        mid = (start + end) // 2

        node = nodes[mid]
        node.left = self._balanceByRecursion(nodes, start, mid - 1)
        node.right = self._balanceByRecursion(nodes, mid + 1, end)

        return node

    def _rotateRight(self, node):
        '''
        A helper function to perform right rotation of subtree rooted at node

        args:
            node (treeNode): the parent node of the subtree to rotate
        returns:
            (treeNode) root of the new tree
        '''
        assert(node.left is not None)

        pivot = node.left
        node.left = pivot.right
        if pivot.right is not None:
            pivot.right.parent = node
        pivot.right = node

        pivot.parent = node.parent
        node.parent = pivot

        # if the rotation is happening at a node in the middle of a tree
        if pivot.parent is not None:
            if pivot.parent.right == node:
                pivot.parent.right = pivot
            elif pivot.parent.left == node:
                pivot.parent.left = pivot

        if self.root == node:
            self.root = pivot

        self._updateHeight(node)
        self._updateBalanceFactor(node)
        self._updateHeight(pivot)
        self._updateBalanceFactor(pivot)

        return pivot

    def _rotateLeft(self, node):
        '''
        A helper function to perform left rotation of subtree rooted at node

        args:
            node (treeNode): the parent node of the subtree to rotate
        returns:
            (treeNode) root of the new tree
        '''
        assert(node.right is not None)

        pivot = node.right
        node.right = pivot.left
        if pivot.left is not None:
            pivot.left.parent = node
        pivot.left = node

        pivot.parent = node.parent
        node.parent = pivot

        # if the rotation is happening at a node in the middle of a tree
        if pivot.parent is not None:
            if pivot.parent.right == node:
                pivot.parent.right = pivot
            elif pivot.parent.left == node:
                pivot.parent.left = pivot

        if self.root == node:
            self.root = pivot

        self._updateHeight(node)
        self._updateBalanceFactor(node)
        self._updateHeight(pivot)
        self._updateBalanceFactor(pivot)

        return pivot

def list_to_BST(dlist, rootdata):
    '''
    Constructs a BST from a given list of node data

    args:
        dlist (list): list of node data
        rootdata (node val data type): data of the root node, may or may not be from dlist
    returns:
        (tree) a BST from the given data list
    '''
    t = tree()
    t.add_node(rootdata)

    try:
        dlist.remove(rootdata)
    except ValueError:
        pass

    for data in dlist:
        t.add_node(data)

    return t
