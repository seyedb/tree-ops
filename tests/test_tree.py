# these tests are designed for pytest framework

import pytest
import tree as Tree
import deepdiff

@pytest.fixture
def dflt_tree():
    '''Returns a default initialized tree object.'''
    return Tree.tree()

@pytest.fixture
def dflt_treeNode():
    '''Returns a default initialized treeNode object.'''
    return Tree.tree().treeNode()

@pytest.fixture
def simple_tree():
    '''Returns a simple tree with 3 nodes: root, its left and right nodes:
        'root':  {'left': 'left', 'right': 'right'}
        'left':  {'left': 'None', 'right': 'None'}
        'right': {'left': 'None', 'right': 'None'}
    '''
    smpl_tree = Tree.tree()
    root = Tree.tree().treeNode('root')
    left = Tree.tree().treeNode('left')
    right = Tree.tree().treeNode('right')
    smpl_tree.root = root
    root.left = left
    root.right = right
    left.parent = root
    right.parent = root

    return smpl_tree

@pytest.fixture
def sample_bst_bstNode():
    '''Returns a sample binary search tree and one of its nodes as a sample node.
       The tree has the following form and the sample node is indicated with *
          8:  {'left': 3, 'right': 10}
        * 3:  {'left': 1, 'right': 6}
          10: {'left': 'None', 'right': 14}
          1:  {'left': 'None', 'right': 'None'}
          6:  {'left': 4, 'right': 7}
          14: {'left': 13, 'right': 'None'}
          4:  {'left': 'None', 'right': 'None'}
          7:  {'left': 'None', 'right': 'None'}
          13: {'left': 'None', 'right': 'None'}
    '''
    t = Tree.tree()
    n1 = Tree.tree().treeNode(1)
    n3 = Tree.tree().treeNode(3)
    n4 = Tree.tree().treeNode(4)
    n6 = Tree.tree().treeNode(6)
    n7 = Tree.tree().treeNode(7)
    n8 = Tree.tree().treeNode(8)
    n10 = Tree.tree().treeNode(10)
    n13 = Tree.tree().treeNode(13)
    n14 = Tree.tree().treeNode(14)
    t.root = n8
    n8.left = n3
    n8.right = n10
    n3.left = n1
    n3.right = n6
    n6.left = n4
    n6.right = n7
    n10.right = n14
    n14.left = n13
    n3.parent = n8
    n10.parent = n8
    n1.parent = n3
    n6.parent = n3
    n14.parent = n10
    n4.parent = n6
    n7.parent = n6
    n13.parent = n14

    return t, n3

def test_default_tree(dflt_tree):
    dflt_root = (dflt_tree.root == None)
    assert dflt_root

def test_default_treeNode(dflt_treeNode):
    dflt_data = (dflt_treeNode.data == None)
    dflt_left = (dflt_treeNode.left == None)
    dflt_right = (dflt_treeNode.right == None)
    dflt_status = (dflt_treeNode.status == Tree.node_status.UNVISITED)
    dflt_parent = (dflt_treeNode.parent == None)
    dflt_height = (dflt_treeNode.height == 0)
    dflt_balance_factor = (dflt_treeNode.balance_factor == 0)
    assert (dflt_data and dflt_left and dflt_right and dflt_status and dflt_parent and dflt_height and dflt_balance_factor)

def test_getStatus(dflt_treeNode):
    assert dflt_treeNode._getStatus() == Tree.node_status.UNVISITED

def test_setStatus(dflt_treeNode):
    dflt_treeNode._setStatus(Tree.node_status.VISITED)
    assert dflt_treeNode.status == Tree.node_status.VISITED

def test__contains__(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    condT = 3 in t
    condF = 5 in t
    cond = (condT, condF)
    assert cond == (True, False)

def test_containsData(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n = sample_bst_bstNode[1]
    condT = t._containsData(6, n)
    condF = t._containsData(14, n)
    cond = (condT, condF)
    assert cond == (True, False)

def test__str__(simple_tree):
    tree_str = simple_tree.__str__()
    assert tree_str == "left root right \n"

def test_strTree(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n = sample_bst_bstNode[1]
    test_str = t._strTree(n)
    assert test_str == "1 3 4 6 7 "

def test_verbose_rep(simple_tree):
    rep_v0_ref = {'root': {'left': 'left', 'right': 'right'},
                  'left': {'left': 'None', 'right': 'None'},
                  'right': {'left': 'None', 'right': 'None'}}

    rep_v1_ref = {'root': {'left': 'left', 'right': 'right', 'parent': 'None', 'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0},
                  'left': {'left': 'None', 'right': 'None', 'parent': 'root', 'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0},
                  'right': {'left': 'None', 'right': 'None', 'parent': 'root', 'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0}}

    rep_v0 = simple_tree.verbose_rep(0)
    rep_v1 = simple_tree.verbose_rep(1)

    diff_v0 = deepdiff.DeepDiff(rep_v0, rep_v0_ref)
    diff_v1 = deepdiff.DeepDiff(rep_v1, rep_v1_ref)

    cond = (diff_v0, diff_v1)
    assert cond == ({}, {})

def test_verboseRep(sample_bst_bstNode):
    rep_ref = {3: {'left': 1, 'right': 6},
               1: {'left': 'None', 'right': 'None'},
               6: {'left': 4, 'right': 7},
               4: {'left': 'None', 'right': 'None'},
               7: {'left': 'None', 'right': 'None'}}

    rep = {}
    t = sample_bst_bstNode[0]
    n3 = sample_bst_bstNode[1]
    t._verboseRep(n3, rep, 0)

    diff = deepdiff.DeepDiff(rep, rep_ref)
    assert diff == {}

def test_update_height(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    t.update_height()

    ref = {8: 3, 3: 2, 10: 2, 6: 1, 14: 1, 1: 0, 4: 0, 7: 0, 13: 0}

    current = t.root
    height_dict = {}
    stk = []
    while True:
        while current:
            stk.append(current)
            current = current.left

        if stk:
            current = stk.pop()
            height_dict[current.data] = current.height
            current = current.right
        else:
            break

    diff = deepdiff.DeepDiff(height_dict, ref)
    assert diff == {}

def test_updateHeight(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n3 = sample_bst_bstNode[1]
    t._updateHeight(n3)

    ref = {3: 2, 6: 1, 1: 0, 4: 0, 7: 0}

    current = n3
    height_dict = {}
    stk = []
    while True:
        while current:
            stk.append(current)
            current = current.left

        if stk:
            current = stk.pop()
            height_dict[current.data] = current.height
            current = current.right
        else:
            break

    print(height_dict)
    diff = deepdiff.DeepDiff(height_dict, ref)
    assert diff == {}

def test_calcHeight(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n3 = sample_bst_bstNode[1]
    old_height = n3.height
    new_height = t._calcHeight(n3)

    assert (old_height, new_height) == (0, 2)

def test_update_balance_factor(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    t.update_balance_factor()

    ref = {8: 0, 3: -1, 10: -2, 6: 0, 14: 1, 1: 0, 4: 0, 7: 0, 13: 0}

    current = t.root
    bf_dict = {}
    stk = []
    while True:
        while current:
            stk.append(current)
            current = current.left

        if stk:
            current = stk.pop()
            bf_dict[current.data] = current.balance_factor
            current = current.right
        else:
            break

    diff = deepdiff.DeepDiff(bf_dict, ref)
    assert diff == {}

def test_updataBalanceFactor(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n3 = sample_bst_bstNode[1]
    t._updateBalanceFactor(n3)

    ref = {3: -1, 6: 0, 1: 0, 4: 0, 7: 0}

    current = n3
    bf_dict = {}
    stk = []
    while True:
        while current:
            stk.append(current)
            current = current.left

        if stk:
            current = stk.pop()
            bf_dict[current.data] = current.balance_factor
            current = current.right
        else:
            break

    diff = deepdiff.DeepDiff(bf_dict, ref)
    assert diff == {}

def test_calcBalanceFactor(sample_bst_bstNode):
    t = sample_bst_bstNode[0]
    n3 = sample_bst_bstNode[1]
    old_bf = n3.balance_factor
    t._calcBalanceFactor(n3)

    assert (old_bf, n3.balance_factor) == (0, -1)
