# these tests are designed for pytest framework

import pytest
import tree as Tree
import deepdiff
import operator as op

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
def sample_bst():
    '''Returns a sample binary search tree and a tuple of its nodes.
       The tree has the following form:
          8:  {'left': 3, 'right': 10}
          3:  {'left': 1, 'right': 6}
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
    # set the root manually
    t.root = n8
    # set the left and right nodes manually
    n8.left = n3
    n8.right = n10
    n3.left = n1
    n3.right = n6
    n6.left = n4
    n6.right = n7
    n10.right = n14
    n14.left = n13
    # set parent nodes manually
    n3.parent = n8
    n10.parent = n8
    n1.parent = n3
    n6.parent = n3
    n14.parent = n10
    n4.parent = n6
    n7.parent = n6
    n13.parent = n14

    nodes_tuple = (n8, n3, n10, n1, n6, n14, n4, n7, n13)

    return t, nodes_tuple

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

def test__contains__(sample_bst):
    t,_ = sample_bst
    condT = 3 in t
    condF = 5 in t
    cond = (condT, condF)
    assert cond == (True, False)

def test_containsData(sample_bst):
    t, nodes = sample_bst
    n = nodes[1]
    condT = t._containsData(6, n)
    condF = t._containsData(14, n)
    cond = (condT, condF)
    assert cond == (True, False)

def test__str__(simple_tree):
    tree_str = simple_tree.__str__()
    assert tree_str == "left root right \n"

def test_strTree(sample_bst):
    t, nodes = sample_bst
    n = nodes[1]
    test_str = t._strTree(n)
    assert test_str == "1 3 4 6 7 "

def test_verbose_rep(simple_tree):
    v0_ref = [{'data': 'root', 'left': 'left', 'right': 'right'},
              {'data': 'left', 'left': 'None', 'right': 'None'},
              {'data': 'right', 'left': 'None', 'right': 'None'}]

    v1_ref = [{'data': 'root', 'left': 'left', 'right': 'right', 'parent': 'None',
               'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0},
              {'data': 'left', 'left': 'None', 'right': 'None', 'parent': 'root',
               'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0},
              {'data': 'right', 'left': 'None', 'right': 'None', 'parent': 'root',
               'status': Tree.node_status.UNVISITED, 'height': 0, 'balance_factor': 0}]

    v0_ref = sorted(v0_ref, key=op.itemgetter('data'))
    v1_ref = sorted(v1_ref, key=op.itemgetter('data'))

    v0 = simple_tree.verbose_rep(0)
    v1 = simple_tree.verbose_rep(1)

    v0 = sorted(v0, key=op.itemgetter('data'))
    v1 = sorted(v1, key=op.itemgetter('data'))

    pairs = zip(v0, v0_ref)
    diff_list = []
    for n1, n2 in pairs:
        diff = deepdiff.DeepDiff(n1, n2)
        diff_list.append(diff)

    cond_v0 = diff_list == [{}] * 3

    pairs = zip(v1, v1_ref)
    diff_list = []
    for n1, n2 in pairs:
        diff = deepdiff.DeepDiff(n1, n2)
        diff_list.append(diff)

    cond_v1 = diff_list == [{}] * 3

    assert cond_v0 and cond_v1

def test_verboseRep(sample_bst):
    rep_ref = [{'data': 3, 'left': 1, 'right': 6},
               {'data': 1, 'left': 'None', 'right': 'None'},
               {'data': 6, 'left': 4, 'right': 7},
               {'data': 4, 'left': 'None', 'right': 'None'},
               {'data': 7, 'left': 'None', 'right': 'None'}]

    rep_ref = sorted(rep_ref, key=op.itemgetter('data'))

    rep = []
    t, nodes = sample_bst
    n3 = nodes[1]
    t._verboseRep(n3, rep, 0)

    rep = sorted(rep, key=op.itemgetter('data'))

    pairs = zip(rep, rep_ref)
    diff_list = []
    for n1, n2 in pairs:
        diff = deepdiff.DeepDiff(n1, n2)
        diff_list.append(diff)

    cond = diff_list == [{}] * 5

    assert cond

def test_update_height(sample_bst):
    t, nodes = sample_bst
    t.update_height()

    ref = {8: 3, 3: 2, 10: 2, 6: 1, 14: 1, 1: 0, 4: 0, 7: 0, 13: 0}

    h_dict = {}
    for node in nodes:
        h_dict[node.data] = node.height

    diff = deepdiff.DeepDiff(h_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_updateHeight(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    t._updateHeight(n3)

    ref = {3: 2, 6: 1, 1: 0, 4: 0, 7: 0}

    ind = [1, 3, 4, 6, 7]
    h_dict = {}
    for i in ind:
        h_dict[nodes[i].data] = nodes[i].height

    diff = deepdiff.DeepDiff(height_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_calcHeight(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    old_height = n3.height
    new_height = t._calcHeight(n3)

    assert (old_height, new_height) == (0, 2)

def test_update_balance_factor(sample_bst):
    t, nodes = sample_bst[0]
    t.update_balance_factor()

    ref = {8: 0, 3: -1, 10: -2, 6: 0, 14: 1, 1: 0, 4: 0, 7: 0, 13: 0}

    bf_dict = {}
    for node in nodes:
        bf_dict[node.data] = node.balance_factor

    diff = deepdiff.DeepDiff(bf_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_updataBalanceFactor(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    t._updateBalanceFactor(n3)

    ref = {3: -1, 6: 0, 1: 0, 4: 0, 7: 0}

    ind = [1, 3, 4, 6, 7]
    bf_dict = {}
    for i in ind:
        bf_dict[nodes[i].data] = nodes[i].balance_factor

    diff = deepdiff.DeepDiff(bf_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_calcBalanceFactor(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    old_bf = n3.balance_factor
    t._calcBalanceFactor(n3)

    assert (old_bf, n3.balance_factor) == (0, -1)

def test_reset_status(sample_bst):
    t, nodes = sample_bst

    ref = {8: Tree.node_status.UNVISITED, 3: Tree.node_status.UNVISITED, 10: Tree.node_status.UNVISITED,
           6: Tree.node_status.UNVISITED, 14: Tree.node_status.UNVISITED, 1: Tree.node_status.UNVISITED,
           4: Tree.node_status.UNVISITED, 7: Tree.node_status.UNVISITED, 13: Tree.node_status.UNVISITED}

    # for testing purpose, set the status of nodes indexed with indices in ref_ind to VISITED
    ref_ind = [0, 2, 4, 6, 8]
    for i in ref_ind:
        nodes[i].status = Tree.node_status.VISITED

    t.reset_status()

    stat_dict = {}
    for node in nodes:
        stat_dict[node.data] = node.status

    diff = deepdiff.DeepDiff(stat_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_resetSatus(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]

    ref = {3: Tree.node_status.UNVISITED, 6: Tree.node_status.UNVISITED, 1: Tree.node_status.UNVISITED,
           4: Tree.node_status.UNVISITED, 7: Tree.node_status.UNVISITED}

    # for testing purpose, set the status of nodes indexed with indices in ref_ind to VISITED
    ref_ind = [0, 2, 4, 6, 8]
    for i in ref_ind:
        nodes[i].status = Tree.node_status.VISITED

    t._resetStatus(n3)

    ind = [1, 3, 4, 6, 7]
    stat_dict = {}
    for i in ind:
        stat_dict[nodes[i].data] = nodes[i].status

    diff = deepdiff.DeepDiff(stat_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_add_node(sample_bst):
    t, nodes = sample_bst
    n10 = nodes[2]

    t.add_node(9)

    n9 = n10.left

    n9_data = (n9.data == 9)
    n9_left = (n9.left == None)
    n9_right = (n9.right == None)
    n9_status = (n9.status == Tree.node_status.UNVISITED)
    n9_parent = (n9.parent == n10)
    n9_height = (n9.height == 0)
    n9_balance_factor = (n9.balance_factor == 0)

    n10_balance_factor = (n10.balance_factor == -1)

    assert (n9_data and n9_left and n9_right and n9_status and n9_parent and n9_height and
            n9_balance_factor and n10_balance_factor)

def test_addNode(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1] # subtree root

    n4 = nodes[6] # the existing node that will be affected

    t._addNode(n3, 5)

    n5 = n4.right

    n5_data = (n5.data == 5)
    n5_left = (n5.left == None)
    n5_right = (n5.right == None)
    n5_status = (n5.status == Tree.node_status.UNVISITED)
    n5_parent = (n5.parent == n4)
    n5_height = (n5.height == 0)
    n5_balance_factor = (n5.balance_factor == 0)

    n4_balance_factor = (n4.balance_factor == -1)
    n4_height = (n4.height == 1)

    assert (n5_data and n5_left and n5_right and n5_status and n5_parent and n5_height and
            n5_balance_factor and n4_height and n4_balance_factor)
