from enum import Enum
from collections import deque

class node_status(Enum):
    '''List of all possible visit status of each node (tree traversal)'''
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class tree(object):
    '''The main (binary search) tree class'''
    def __init__(self, root=None):
        '''Initializes a tree with its root node.'''
        self.root = root

    class treeNode(object):
        '''The main tree node class (defined as an inner class of the tree class)'''
        def __init__(self, data=None, status=node_status.UNVISITED, balance_factor=0):
            '''Initializes a tree node.
            A tree node has a value, a left child, a right child, a visit status, parent node, 
            height of the tree rooted at the node, and balance factor (difference between the
            height of the left and the right subtrees).
            '''
            self.data = data
            self.left = None
            self.right = None
            self.status = status
            self.parent = None
            self.height = 0
            self.balance_factor = balance_factor

        # comparison operators
        def __lt__(self, other):
            return self.data < other.data

        def __le__(self, other):
            return self < other or self == other

        # the following are optional
#        def __ne__(self, other):
#            return self.data != other.data
#
#        def __gt__(self, other):
#            return self.data > other.data
#
#        def __ge__(self, other):
#            return self > other or self == other

        def _getStatus(self):
            '''Gets the visit status of a tree node.'''
            return self.status
    
        def _setStatus(self, status):
            '''Sets the visit status of a tree node to a given value.
    
            args:
                status (node_status): the new visit status to be assigned to the node
            '''
            self.status = status

    def __contains__(self, data):
        '''Checks if a tree contains a given data.

        args:
            data (node val data type): the data to be found in the tree
        returns:
            (boolean) True if the tree contains the data, False otherwise
        '''
        if self.root is not None:
            return self._containsData(data, self.root)
        else:
            return False

    def _containsData(self, data, node):
        '''(helper function) Checks if a (sub)tree rooted at a given node contains a given data.

        args:
            data (node val data type): the data to be found in the tree
            node (treeNode): the (root) node at which the recursive search begins
        returns:
            (boolean) True if the (sub)tree rooted at node contains the data, False otherwise
        '''
        if node.data == data:
            return True
        elif (data < node.data and node.left is not None):
            return self._containsData(data, node.left)
        elif (data > node.data and node.right is not None):
            return self._containsData(data, node.right)
            
        return False

    def __str__(self):
        '''Represents a tree with a string starting from its root'''
        res = "\n"
        if self.root is not None:
            return self._printTree(self.root) + res
        return res

    def _printTree(self, node):
        '''(helper function) Prints a tree rooted at a given node all the way down.
        NOTE: The output must be in ascending order in case of BST

        args:
            node (treeNode): the tree node at which the printing starts 
        returns:
            (str) a space-delimited string representing the data stored in the tree
        '''
        res = ""
        if node is not None:
            res += self._printTree(node.left)
            res += "{} ".format(node.data)
            res += self._printTree(node.right)
        return res

    def verbose_rep(self, verb_level=0):
        '''Returns a verbose representation of the tree in the form of a nested dictionary. The dict
        keys are the data of the nodes and dict values are the values of the instance attributes.

        args:
            verb_level (0 or 1): the verbosity level
        returns:
            (nested dict) a nested (2D) dictionary representing the tree
        '''
        representation = {}
        if self.root is not None:
            self._verboseRep(self.root, representation, verb_level)

        return representation

    def _verboseRep(self, node, rep, verb_level=0):
        '''(helper function) Returns a nested dict representation of the (sub)tree rooted at the given node.

        args:
            node (treeNode): the node where the procedure (inorder visit of the tree nodes) starts
            rep (dict): the dict representation to be constructed
            verb_level (0 or 1): the verbosity level
        returns:
            (nested dict) a nested (2D) dictionary containing the values of the instance attributes of
            all the nodes in the (sub)tree
        '''
        assert(verb_level in {0, 1}), 'Invalid verbosity level!'

        if node is not None:
            self._verboseRep(node.left, rep, verb_level)

            attrs = {}
            if verb_level == 0:
                attrs['left'] = 'None' if node.left is None else node.left.data
                attrs['right'] = 'None' if node.right is None else node.right.data
            elif verb_level == 1:
                attrs['left'] = 'None' if node.left is None else node.left.data
                attrs['right'] = 'None' if node.right is None else node.right.data
                attrs['parent'] = 'None' if node.parent is None else node.parent.data
                attrs['status'] = node.status
                attrs['height'] = node.height
                attrs['balance_factor'] = node.balance_factor
            rep[node.data] = attrs

            self._verboseRep(node.right, rep, verb_level)

    def update_height(self):
        '''Updates the height of every node of a given tree.'''
        self._updateHeight(self.root)

    def _updateHeight(self, node):
        '''(helper function) Recursively updates the height of each node starting from the given node 
        all the way down.
        
        args:
            node (treeNode): the tree node at which the procedure starts
        returns:
            (tree) the input tree where every node of its subtrees rooted at the input node have updated heights
        '''
        if node is not None:
            self._updateHeight(node.left)
            node.height = self._calcHeight(node)
            self._updateHeight(node.right)

    def _calcHeight(self, node):
        '''(helper function) Calculates the height of the tree rooted at a given node.

        returns:
            (treeNode) the input tree node with updated height
        '''
        if node is None:
            return -1
        else:
            lheight = self._getHeight(node.left)
            rheight = self._getHeight(node.right)
            return max(lheight, rheight) + 1

    def update_balance_factor(self):
        '''Updates the balance factor of every node of a given tree.'''
        self._updateBalanceFactor(self.root)

    def _updateBalanceFactor(self, node):
        '''(helper function) Recursively updates the balance factor of each node starting from the given node 
        all the way down.
        
        args:
            node (treeNode): the tree node at which the procedure starts
        returns:
            (tree) the input tree where every node of its subtrees rooted at the input node have updated balance_factor
        '''
        if node is not None:
            self._updateBalanceFactor(node.left)
            self._calcBalanceFactor(node)
            self._updateBalanceFactor(node.right)

    def _calcBalanceFactor(self, node):
        '''(helper function) Calculates the balance factor of the tree rooted a given tree node.

        returns:
            (treeNode) the input tree node with updated balance factor
        '''
        lheight = self._calcHeight(node.left)
        rheight = self._calcHeight(node.right)
        node.balance_factor = lheight - rheight

    def reset_status(self):
        '''Resets the visit status of all the nodes in a tree to UNVISITED.'''
        self._resetStatus(self.root)

    def _resetStatus(self, node):
        '''(helper function) Resets the visit status of each node below the given node to UNVISITED 
        after a traversal routine (in-, pre-, postorder, DFS, BFS) call, it is done recursively 
        following an in-order fashion.

        args:
            node (treeNode): the tree node at which the procedure starts
        '''
        if node is not None:
            self._resetStatus(node.left)
            node._setStatus(node_status.UNVISITED)
            self._resetStatus(node.right)

    def add_node(self, data, balanced=False):
        '''Adds a node to a tree.

        args:
            data (node val data type): the value to be assigned to the new tree node
            balanced (boolean): if True rebalance the current root after adding the new node
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self.root = self._addNode(self.root, data, balanced)

    def _addNode(self, node, data, balanced=False):
        '''(helper function) Finds the right location for the new node according to the BST-property.

        args:
            data (node val data type): the value to be assigned to the new node
            node (treeNode): the node at which the recursive approach to insert a new node starts
            balanced (boolean): if True rebalance the current root after adding the new node
        returns:
            (tree) tree updated with the new node inserted at one of its leaves
        '''
        if data < node.data:
            if node.left is not None:
                lnode = self._addNode(node.left, data, balanced)
            else:
                lnode = self.treeNode(data)

            node.left = lnode
            lnode.parent = node
        else:
            if node.right is not None:
                rnode = self._addNode(node.right, data, balanced)
            else:
                rnode = self.treeNode(data)

            node.right = rnode
            rnode.parent = node
        
        self._calcHeight(node)
        self._calcBalanceFactor(node)

        if balanced:
            return self._rebalanceSubtree(node)
        else:
            return node

    def insert_node(self, data, balanced=False):
        '''Inserts a node in a tree in level order (uses _insertNode with the root as the starting node) 
        (see documentation of _insertNode for more details).

        args:
            data (node val data type): the value to be assigned to the new tree node
            balanced (boolean): if True rebalance the current root after adding the new node
        returns:
            (tree) tree updated with a new node
        '''
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self._insertNode(self.root, data, balanced)

    def _insertNode(self, node, data, balanced=False):
        '''(helper function) Inserts a node in a binary tree (not necessarily BST) in level order 
        (breadth-first):
            traversing down the tree from the given starting point, if a node N is found whose left 
            node is empty, a new node with the given data is created as N.left, else if a node N is 
            found whose right node is empty, the new node is created as N.right. 

        args:
            data (node val data type): the value to be assigned to the new node
            node (treeNode): the node at which the traversal to insert a new node starts
            balanced (boolean): if True rebalance the current root after adding the new node
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

        self._calcHeight(node)
        self._calcBalanceFactor(node)

        if balanced:
            return self._rebalanceSubtree(node)
        else:
            return node

    def inorder_traversal(self, node, path=None):
        '''Inorder Traversal 

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
        '''Preorder Traversal 

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
        '''Postorder Traversal 

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
        '''Finds a node in a tree.
        
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
        '''(helper function) Finds a given data in a tree.
        
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
        '''Depth-First Search (DFS)

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
        '''Breadth-First Search (BFS)

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
        '''Checks whether or not a tree (BST or not) is balanced.

        returns:
            (bool) True when the tree is balanced, False otherwise
        '''
        return self._isBalanced(self.root) > -1

    def _isBalanced(self, node):
        '''(helper function) Checks if a BST is balanced.
        
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

    def _balanceByRecursion(self, nodes, start, end):
        '''(helper function) Converts a binary tree to a balanced binary tree by recursion. Performs
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

        mid = start + (end - start)//2

        node = nodes[mid]
        node.left = self._balanceByRecursion(nodes, start, mid - 1)
        node.right = self._balanceByRecursion(nodes, mid + 1, end)

        return node

    def _convertToAVL(self, node, res):
        '''(helper function) Converts a tree rooted at node into an AVL tree.
            - perform an inorder traversal of the tree
            - insert the visited node into another (AVL) tree preserving balance 

        args:
            node (treeNode): the root node of the (sub)tree to be traversed/converted
            res (tree): the resulted AVL tree (can be non-empty but must be balanced) 
        returns:
            (tree) res (a balanced tree) with nodes imported from the input tree
        '''
        if node is not None:
            self._convertToAVL(node.left, res)
            res.add_node(node.data, balanced=True)
            self._convertToAVL(node.right, res)

        return res

    def _rebalanceSubtree(self, node):
        '''(helper function) Rebalances a subtree rooted at a given node using rotation operations.

        args:
            node (treeNode): root of the subtree to be rebalanced
        returns:
            (treeNode) the root of the rebalanced subtree
        '''
        # left imbalance
        if node.balance_factor > 1:
            # left-right imbalance
            if node.left.balance_factor < 0:
                node.left = self._rotateLeft(node.left)
                return self._rotateRight(node)
            # left-left imbalance
            else:
                return self._rotateRight(node)
        # right imbalance
        elif node.balance_factor < -1:
            # right-left imbalance
            if node.right.balance_factor > 0:
                node.right = self._rotateRight(node.right)
                return self._rotateLeft(node)
            # right-right imbalance
            else:
                return self._rotateLeft(node)
        # balance_factor is in {-1, 0, 1}, the node is already balanced
        else:
            return node

    def _rotateRight(self, node):
        '''(helper function) Performs right rotation of subtree rooted at node.

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

        self._calcHeight(node)
        self._calcBalanceFactor(node)
        self._calcHeight(pivot)
        self._calcBalanceFactor(pivot)

        return pivot

    def _rotateLeft(self, node):
        '''(helper function) Performs left rotation of subtree rooted at node.

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

        self._calcHeight(node)
        self._calcBalanceFactor(node)
        self._calcHeight(pivot)
        self._calcBalanceFactor(pivot)

        return pivot

