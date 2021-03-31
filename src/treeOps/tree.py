from enum import Enum
from collections import deque

class tree(object):
    """The main (binary search) tree class."""
    def __init__(self, root=None):
        """Initializes a tree with its root node."""
        self.root = root
        if root: self.root.parent = None

    class treeNode(object):
        """The main tree node class (defined as an inner class of the tree class)."""
        def __init__(self, data=None, balance_factor=0):
            """Initializes a tree node.
            Attributes:
                data (any type): the node value.
                left (treeNode): the left child.
                right (treeNode): the right child.
                parent (treeNode): the parent node.
                height (int): the height of the tree rooted at the node.
                balance_factor (int): difference between the height of the left and the right subtrees.
            """
            self.data = data
            self.left = None
            self.right = None
            # the following are used in tree balancing algorithms
            self.parent = None
            self.height = 0
            self.balance_factor = balance_factor

        # comparison operators
        def __lt__(self, other):
            return self.data < other.data

        def __le__(self, other):
            return self.data < other.data or self.data == other.data

        # the following are optional
#        def __ne__(self, other):
#            return self.data != other.data
#
#        def __gt__(self, other):
#            return self.data > other.data
#
#        def __ge__(self, other):
#            return self.data > other.data or self.data == other.data

        def __str__(self):
            """Returns a string representation of a treeNode."""
            res = 'data: {},\t'.format(self.data)
            res += 'left: {},\t'.format('None' if self.left is None else self.left.data)
            res += 'right: {},\t'.format('None' if self.right is None else self.right.data)
            res += 'parent: {},\t'.format('None' if self.parent is None else self.parent.data)
            res += 'height: {},\t'.format(self.height)
            res += 'balance factor: {}'.format(self.balance_factor)
            return res

    def __contains__(self, data):
        """Checks if a tree contains a given data.

        Args:
            data (node val data type): the data to be found in the tree.
        Returns:
            (boolean) True if the tree contains the data, False otherwise.
        """
        if self.root is not None:
            return self._containsData(data, self.root)
        else:
            return False

    def _containsData(self, data, node):
        """(helper function) Checks if a (sub)tree rooted at a given node contains a given data.

        Args:
            data (node val data type): the data to be found in the tree.
            node (treeNode): the (root) node at which the recursive search begins.
        Returns:
            (boolean) True if the (sub)tree rooted at node contains the data, False otherwise.
        """
        if node.data == data:
            return True
        elif (data < node.data and node.left is not None):
            return self._containsData(data, node.left)
        elif (data > node.data and node.right is not None):
            return self._containsData(data, node.right)
            
        return False

    def __str__(self):
        """Represents a tree with a string starting from its root."""
        res = '\n'
        if self.root is not None:
            return self._strTree(self.root) + res
        return res

    def _strTree(self, node):
        """(helper function) Returns string representation of a (sub)tree rooted at a given node.
        NOTE:
            - The output must be in ascending order in case of BST.

        Args:
            node (treeNode): the tree node at which the printing starts.
        Returns:
            (str) a space-delimited string representing the data stored in the tree.
        """
        res = ''
        if node is not None:
            res += self._strTree(node.left)
            res += '{} '.format(node.data)
            res += self._strTree(node.right)
        return res

    def verbose_rep(self, verb_level=0):
        """Returns a verbose representation of the tree as a list of dictionaries. The dict keys are 
           the instance attributes of the nodes and dict values are the values of the attributes. The
           ordering of nodes in the list follows an in-order pattern.

        Args:
            verb_level (0 or 1): the verbosity level.
        Returns:
            (list of dict) a list of dictionaries representing the tree.
        """
        representation = []
        if self.root is not None:
            self._verboseRep(self.root, representation, verb_level)

        return representation

    def _verboseRep(self, node, rep, verb_level=0):
        """(helper function) Returns a list of dict representation of the (sub)tree rooted at the given node.

        Args:
            node (treeNode): the node where the procedure (inorder visit of the tree nodes) starts.
            rep (list): the list of dict representation to be constructed.
            verb_level (0 or 1): the verbosity level.
        Returns:
            (list of dict) a list of dictionaries containing the values of the instance attributes of
            all the nodes in the (sub)tree.
        """
        assert(verb_level in {0, 1}), 'Invalid verbosity level!'

        if node is not None:
            self._verboseRep(node.left, rep, verb_level)
            attrs = {}
            attrs['data'] = node.data
            if verb_level == 0:
                attrs['left'] = 'None' if node.left is None else node.left.data
                attrs['right'] = 'None' if node.right is None else node.right.data
            elif verb_level == 1:
                attrs['left'] = 'None' if node.left is None else node.left.data
                attrs['right'] = 'None' if node.right is None else node.right.data
                attrs['parent'] = 'None' if node.parent is None else node.parent.data
                attrs['height'] = node.height
                attrs['balance_factor'] = node.balance_factor
            rep.append(attrs)

            self._verboseRep(node.right, rep, verb_level)

    def update_height(self):
        """Updates the height of every node of a given tree."""
        self._updateHeight(self.root)

    def _updateHeight(self, node):
        """(helper function) Recursively updates the height of each node starting from the given node 
        all the way down.
        
        Args:
            node (treeNode): the tree node at which the procedure starts.
        Returns:
            (tree) the input tree where every node of its subtree rooted at the input node have updated heights.
        """
        if node is not None:
            self._updateHeight(node.left)
            node.height = self._calcHeight(node)
            self._updateHeight(node.right)

    def _calcHeight(self, node):
        """(helper function) Calculates the height of the tree rooted at a given node.

        Returns:
            (int) the height of the tree at the input node.
        """
        if node is None:
            return -1
        else:
            lheight = self._calcHeight(node.left)
            rheight = self._calcHeight(node.right)
            return max(lheight, rheight) + 1

    def update_balance_factor(self):
        """Updates the balance factor of every node of a given tree."""
        self._updateBalanceFactor(self.root)

    def _updateBalanceFactor(self, node):
        """(helper function) Recursively updates the balance factor of each node starting from the given node 
        all the way down.
        
        Args:
            node (treeNode): the tree node at which the procedure starts.
        Returns:
            (tree) the input tree where every node of its subtrees rooted at the input node have updated balance_factor.
        """
        if node is not None:
            self._updateBalanceFactor(node.left)
            self._calcBalanceFactor(node)
            self._updateBalanceFactor(node.right)

    def _calcBalanceFactor(self, node):
        """(helper function) Calculates the balance factor of the tree rooted a given tree node.

        Returns:
            (treeNode) the input tree node with updated balance factor.
        """
        lheight = self._calcHeight(node.left)
        rheight = self._calcHeight(node.right)
        node.balance_factor = lheight - rheight

    def add_node(self, data, balanced=False):
        """Adds a node to a tree.

        Args:
            data (node val data type): the value to be assigned to the new tree node.
            balanced (boolean): if True rebalance the current root after adding the new node.
        Returns:
            (tree) tree updated with the new node inserted at one of its leaves.
        """
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self.root = self._addNode(self.root, data, balanced)

    def _addNode(self, node, data, balanced=False):
        """(helper function) Finds the right location for the new node according to the BST-property.

        Args:
            data (node val data type): the value to be assigned to the new node.
            node (treeNode): the node at which the recursive approach to insert a new node starts.
            balanced (boolean): if True rebalance the current root after adding the new node.
        Returns:
            (tree) tree updated with the new node inserted at one of its leaves.
        """
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
        
        self._updateHeight(node)
        self._calcBalanceFactor(node)

        if balanced:
            return self._rebalanceSubtree(node)
        else:
            return node

    def insert_node(self, data, balanced=False):
        """Inserts a node in a tree in level order (uses _insertNode with the root as the starting node) 
        (see documentation of _insertNode for more details).

        Args:
            data (node val data type): the value to be assigned to the new tree node.
            balanced (boolean): if True rebalance the current root after adding the new node.
        Returns:
            (tree) tree updated with a new node.
        """
        if self.root is None:
            self.root = self.treeNode(data)
        else:
            self._insertNode(self.root, data, balanced)

    def _insertNode(self, node, data, balanced=False):
        """(helper function) Inserts a node in a binary tree (not necessarily BST) in level order 
        (breadth-first):
            traversing down the tree from the given starting point, if a node N is found whose left 
            node is empty, a new node with the given data is created as N.left, else if a node N is 
            found whose right node is empty, the new node is created as N.right. 

        Args:
            data (node val data type): the value to be assigned to the new node.
            node (treeNode): the node at which the traversal to insert a new node starts.
            balanced (boolean): if True rebalance the current root after adding the new node.
        Returns:
            (tree) tree updated with a new node.
        """
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

        self.update_height()
        self.update_balance_factor()

        if balanced:
            return self._rebalanceSubtree(node)
        else:
            return node

    def inorder_traversal(self, node, path=None):
        """Inorder Traversal.

        Args:
            node (treeNode): the tree node at with the inorder traversal starts.
            path (list of treeNode): the traversal path.
        Returns:
            (list of treeNode) the full traversal path.
        """
        if path is None:
            path = []

        if node is not None:
            path = self.inorder_traversal(node.left, path)
            path.append(node)
            path = self.inorder_traversal(node.right, path)

        return path

    def preorder_traversal(self, node, path=None):
        """Preorder Traversal.

        Args:
            node (treeNode): the tree node at with the preorder traversal starts.
            path (list of treeNode): the traversal path.
        Returns:
            (list of treeNode) the full traversal path.
        """
        if path is None:
            path = []

        if node is not None:
            path.append(node)
            path = self.preorder_traversal(node.left, path)
            path = self.preorder_traversal(node.right, path)

        return path

    def postorder_traversal(self, node, path=None):
        """Postorder Traversal.

        Args:
            node (treeNode): the tree node at with the postorder traversal starts.
            path (list of treeNode): the traversal path.
        Returns:
            (list of treeNode) the full traversal path.
        """
        if path is None:
            path = []

        if node is not None:
            path = self.postorder_traversal(node.left, path)
            path = self.postorder_traversal(node.right, path)
            path.append(node)

        return path

    def find_node(self, data):
        """Finds a node in a tree.
        
        Args:
            data (node val data type): the data to be found in the tree.
        Returns:
            (treeNode) the tree node that contains the given data.   
        """
        if self.root is not None:
            return self._findNode(self.root, data)
        else:
            return None

    def _findNode(self, node, data):
        """(helper function) Finds a given data in a tree.
        
        Args:
            node (treeNode): the node at which the recursive search begins.
            data (node val data type): the data to be found in the tree.
        Returns:
            (treeNode) the tree node that contains the given data.
        """
        if node.data == data:
            return node
        elif (data < node.data and node.left is not None):
            return self._findNode(node.left, data)
        elif (data > node.data and node.right is not None):
            return self._findNode(node.right, data)

    def DFS(self, start, path=None):
        """Depth-First Search (DFS).

        Args:
            start (treeNode): the node where the traversal starts.
            path (list of treeNode): the DFS path (empty path to be filled with nodes).
        Returns:
            (list of treeNode) the full DFS path.
        """
        if path is None:
            path = []

        s = self.find_node(start.data)
        if s is None:
            return

        if len(path) == 0: path.append(s)

        children = []
        if s.left is not None: children.append(s.left)
        if s.right is not None: children.append(s.right)

        for child in children:
            path.append(child)
            path = self.DFS(child, path)

        return path
        
    def BFS(self, start):
        """Breadth-First Search (BFS).

        Args:
            start (treeNode): the node where the traversal starts.
        Returns:
            (list of treeNode) the full BFS path.
        """
        s = self.find_node(start.data)
        if s is None:
            return
        path = []

        Q = deque()
        Q.append(s)
        while Q:
            k = Q.popleft()

            children = []
            if k.left is not None: children.append(k.left)
            if k.right is not None: children.append(k.right)
            for child in children:
                    Q.append(child)

            path.append(k)

        return path

    def is_balanced(self):
        """Checks whether or not a tree (BST or not) is balanced.

        Returns:
            (bool) True when the tree is balanced, False otherwise.
        """
        return self._isBalanced(self.root) > -1

    def _isBalanced(self, node):
        """(helper function) Checks if a BST is balanced.
        
        Args:
            node (treeNode): the tree node where the recursive procedure starts.
        Returns:
            (int) -1 if the tree (subtree) is not balanced, otherwise returns the height of the 
                  tree (subtree).
        """
        if node is None:
            return 0

        lheight = self._isBalanced(node.left)
        if lheight == -1: return -1

        rheight = self._isBalanced(node.right)
        if rheight == -1: return -1

        if abs(lheight - rheight) > 1: return -1

        return max(lheight, rheight) + 1

    def _balanceByRecursion(self, nodes, start, end):
        """(helper function) Converts a binary tree to a balanced binary tree by recursion. Performs
        the recursive step.
        NOTE:
            - nodes must be a list of consecutive nodes in an inorder sense.
            - nodes that come before or after the list will NOT be updated, i.e. their height, 
            balance_factor, parent, left and right nodes will remain unchanged.

        Args:
            nodes (list of treeNode): a subset of the node list over which a recursion step is taken.
            start (int): the index of the left-most element of the list over which the currect step 
            of recursion is performed.
            end (int): the index of the right-most element of the list over which the current step 
            of recursion is performed.
        Returns:
            (treeNode) the root node of the constructed balanced tree after recursion is completed.
        """
        if start > end:
            return None

        mid = start + (end - start)//2

        node = nodes[mid]
        node.left = self._balanceByRecursion(nodes, start, mid - 1)
        node.right = self._balanceByRecursion(nodes, mid + 1, end)

        if node.left: node.left.parent = node
        if node.right: node.right.parent = node

        self._updateHeight(node)
        self._calcBalanceFactor(node)

        return node

    def _convertToAVL(self, node, res):
        """(helper function) Converts a tree rooted at node into an AVL tree.
            - perform an inorder traversal of the tree;
            - insert the visited node into another (AVL) tree preserving balance.

        Args:
            node (treeNode): the root node of the (sub)tree to be traversed/converted.
            res (tree): the resulted AVL tree (can be non-empty but must be balanced).
        Returns:
            (tree) res (a balanced tree) with nodes imported from the input tree.
        """
        if node is not None:
            self._convertToAVL(node.left, res)
            res.add_node(node.data, balanced=True)
            self._convertToAVL(node.right, res)

        return res

    def _rebalanceSubtree(self, node):
        """(helper function) Rebalances a subtree rooted at a given node using rotation operations.

        Args:
            node (treeNode): root of the subtree to be rebalanced.
        Returns:
            (treeNode) the root of the rebalanced subtree.
        """
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
        """(helper function) Performs right rotation of subtree rooted at node.

        Args:
            node (treeNode): the parent node of the subtree to rotate.
        Returns:
            (treeNode) root of the new tree.
        """
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
        self._calcBalanceFactor(node)
        self._updateHeight(pivot)
        self._calcBalanceFactor(pivot)

        return pivot

    def _rotateLeft(self, node):
        """(helper function) Performs left rotation of subtree rooted at node.

        Args:
            node (treeNode): the parent node of the subtree to rotate.
        Returns:
            (treeNode) root of the new tree.
        """
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
        self._calcBalanceFactor(node)
        self._updateHeight(pivot)
        self._calcBalanceFactor(pivot)

        return pivot

