#
import tree

def list_to_tree(dlist, rootVal=None, balanced=False):
    '''
    Constructs a binary tree (BST or AVL) from a given list of node data

    NOTE: 
        - if balanced=True the rebalancing procedure (consisting of tree rotations) may lead to a 
        tree where rootVal is not nccessarily the root. 
        - if rootVal=None (default) the first element of dlist will be assgined to rootVal

    args:
        dlist (list): list of node data
        rootVal (node val data type): value of the root node, may or may not be from dlist
        balanced (boolean): if True the result will be a balanced tree
    returns:
        (tree) a BST from the given data list
    '''
    t = tree.tree()

    if rootVal is None:
        try:
            rootVal = dlist[0]
        except IndexError:
            print("Error! dlist, the list of node data, is empty.")
            return None

    t.add_node(rootVal, balanced)

    try:
        dlist.remove(rootVal)
    except ValueError:
        pass

    for data in dlist:
        t.add_node(data, balanced)

    return t

def balance_by_recursion(inTree):
    '''
    Converts a given binary tree (may or may not be BST) to a balanced binary tree by recursion
    in the following steps:
        - creates a sorted list of nodes from the input tree using an inorder traversal path
        - constructs a balanced tree recursively from a sorted list of nodes:
            1- find the middle of the list and make it the root
            2- get the middle left half of the list and make it the left node of the step 1
            3- get the middle right half of the list and make it the right node of the step 1

    args:
        inTree (tree) input tree
    returns:
        (tree) a balanced binary tree containing the data/nodes from the given binary tree
    '''
    balancedt = tree.tree()
    path = inTree.inorder_traversal(inTree.root)
    # reset the visit status (can be avoided if visit status is removed as a node attribute)
    for node in path:
        node._setStatus(node_status.UNVISITED)

    rnode = inTree._balanceByRecursion(path, 0, len(path) - 1)
    balancedt.root = rnode

    return balancedt

def convert_to_AVL(inTree):
    '''
    Converts a given tree (may or may not be BST) to a balanced (AVL) tree

    args:
        inTree (tree) input tree
    returns:
        (tree) a balanced (AVL) tree containing the data/nodes from the given tree
    '''
    avlTree = tree.tree()
    inTree._convertToAVL(inTree.root, avlTree)

    return avlTree

