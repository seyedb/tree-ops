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

def test__lt__():
    n1 = Tree.tree().treeNode(1)
    n2 = Tree.tree().treeNode(2)
    n3 = Tree.tree().treeNode(3)
    assert (n1 < n2 and n3 > n2)

def test__le__():
    n1 = Tree.tree().treeNode(1)
    n2 = Tree.tree().treeNode(1)
    assert (n2 <= n1)

def test_treeNode__str__(dflt_treeNode):
    treeNode_str = dflt_treeNode.__str__()
    ref_str = "data: None,\tleft: None,\tright: None,\tstatus: node_status.UNVISITED,\tparent: None,\theight: 0,\tbalance factor: 0"
    assert treeNode_str == ref_str

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

def test_tree__str__(simple_tree):
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

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(v0, v0_ref)]
    cond_v0 = diff_list == [{}] * 3

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(v1, v1_ref)]
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

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, rep_ref)]
    cond = diff_list == [{}] * 5

    assert cond

def test_update_height(sample_bst):
    t, nodes = sample_bst
    t.update_height()

    ref = {8: 3, 3: 2, 10: 2, 6: 1, 14: 1, 1: 0, 4: 0, 7: 0, 13: 0}

    h_dict = {node.data:node.height for node in nodes}

    diff = deepdiff.DeepDiff(h_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_updateHeight(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    t._updateHeight(n3)

    ref = {3: 2, 6: 1, 1: 0, 4: 0, 7: 0}

    ind = [1, 3, 4, 6, 7]
    h_dict = {nodes[i].data:nodes[i].height for i in ind}

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

    bf_dict = {node.data:node.balance_factor for node in nodes}

    diff = deepdiff.DeepDiff(bf_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_updataBalanceFactor(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    t._updateBalanceFactor(n3)

    ref = {3: -1, 6: 0, 1: 0, 4: 0, 7: 0}

    ind = [1, 3, 4, 6, 7]
    bf_dict = {nodes[i].data:nodes[i].balance_factor for i in ind}

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

    stat_dict = {node.data:node.status for node in nodes}

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
    stat_dict = {nodes[i].data:nodes[i].status for i in ind}

    diff = deepdiff.DeepDiff(stat_dict, ref)
    # the diff must be an empty dictionary
    assert not diff

def test_add_node(sample_bst):
    t, nodes = sample_bst
    n10 = nodes[2] # the existing node to be affected

    t.add_node(9)

    n9 = n10.left # n10.left was None

    # the new node
    cond0 = (n9.data == 9)
    cond1 = (n9.left == None)
    cond2 = (n9.right == None)
    cond3 = (n9.status == Tree.node_status.UNVISITED)
    cond4 = (n9.parent == n10)
    cond5 = (n9.height == 0)
    cond6 = (n9.balance_factor == 0)

    cond7 = (n10.balance_factor == -1) # was -2

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7]

    assert all(cond)

def test_addNode(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1] # subtree root

    # the existing nodes that will be affected
    n4 = nodes[6]
    n6 = nodes[4]

    t._addNode(n3, 5)

    n5 = n4.right # n4.right was None

    # the new node
    cond0 = (n5.data == 5)
    cond1 = (n5.left == None)
    cond2 = (n5.right == None)
    cond3 = (n5.status == Tree.node_status.UNVISITED)
    cond4 = (n5.parent == n4)
    cond5 = (n5.height == 0)
    cond6 = (n5.balance_factor == 0)

    cond7 = (n4.height == 1) # was 0
    cond8 = (n4.balance_factor == -1) # was 0

    cond9 = (n3.height == 3) # was 2
    cond10 = (n3.balance_factor == -2) # was -1

    cond11 = (n6.height == 2) # was 1
    cond12 = (n6.balance_factor == 1) # was 0

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8,
            cond9, cond10, cond11, cond12]

    assert all(cond)

def test_add_node_balanced(sample_bst):
    t, nodes = sample_bst
    # the nodes that will be affected
    n8 = nodes[0]
    n10 = nodes[2]
    n14 = nodes[5]
    n13 = nodes[8]

    t.add_node(11, True)

    n11 = n10.right # was n14

    # the new node
    cond0 = (n11.data == 11)
    cond1 = (n11.left == None)
    cond2 = (n11.right == None)
    cond3 = (n11.status == Tree.node_status.UNVISITED)
    cond4 = (n11.parent == n10)
    cond5 = (n11.height == 0)
    cond6 = (n11.balance_factor == 0)

    cond7 = (n8.right == n13) # n10

    cond8 = (n10.parent == n13) # n8
    cond9 = (n10.height == 1) # 2
    cond10 = (n10.balance_factor == -1) # -2

    cond11 = (n13.left == n10) # None
    cond12 = (n13.right == n14) # None
    cond13 = (n13.parent == n8) # n14
    cond14 = (n13.height == 2) # 0
    cond15 = (n13.balance_factor == 1) # 0

    cond16 = (n14.left == None) # n13
    cond17 = (n14.parent == n13) # n10
    cond18 = (n14.height == 0) # 1
    cond19 = (n14.balance_factor == 0) # 1

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8,
            cond9, cond10, cond11, cond12, cond13, cond14, cond15, cond16,
            cond17, cond18, cond19]

    assert all(cond)

def test_addNode_balanced(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1] # subtree root

    # the nodes that will be affected
    n4 = nodes[6]
    n6 = nodes[4]
    n8 = nodes[0]

    t._addNode(n3, 5, True)

    n5 = n6.left # n6.left was n4

    # the new node
    cond0 = (n5.data == 5)
    cond1 = (n5.left == None)
    cond2 = (n5.right == None)
    cond3 = (n5.status == Tree.node_status.UNVISITED)
    cond4 = (n5.parent == n6)
    cond5 = (n5.height == 0)
    cond6 = (n5.balance_factor == 0)

    cond7 = (n8.left == n4) # n3

    cond8 = (n4.left == n3) # None
    cond9 = (n4.right == n6) # None
    cond10 = (n4.parent == n8) # n6
    cond11 = (n4.height == 2) # 0

    cond12 = (n3.right == None) # n6
    cond13 = (n3.parent == n4) # n8
    cond14 = (n3.height == 1) # 2
    cond15 = (n3.balance_factor == 1) # -1

    cond16 = (n6.left == n5) # n4
    cond17 = (n6.parent == n4) # n3

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8,
            cond9, cond10, cond11, cond12, cond13, cond14, cond15, cond16,
            cond17]

    assert all(cond)

def test_insert_node(sample_bst):
    t, nodes = sample_bst
    n10 = nodes[2] # the existing node to be affected

    t.insert_node(2)

    n2 = n10.left # n10.left was None

    # the new node
    cond0 = (n2.data == 2)
    cond1 = (n2.left == None)
    cond2 = (n2.right == None)
    cond3 = (n2.status == Tree.node_status.UNVISITED)
    cond4 = (n2.parent == n10)
    cond5 = (n2.height == 0)
    cond6 = (n2.balance_factor == 0)

    cond7 = (n10.balance_factor == -1) # was -2

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7]

    assert all(cond)

def test_insertNode(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1] # subtree root

    n1 = nodes[3] # the existing node that will be affected

    t._insertNode(n3, 5)

    n5 = n1.left # n1.left was None

    # the new node
    cond0 = (n5.data == 5)
    cond1 = (n5.left == None)
    cond2 = (n5.right == None)
    cond3 = (n5.status == Tree.node_status.UNVISITED)
    cond4 = (n5.parent == n1)
    cond5 = (n5.height == 0)
    cond6 = (n5.balance_factor == 0)

    cond7 = (n1.height == 1) # was 0
    cond8 = (n1.balance_factor == 1) # was 0

    cond9 = (n3.balance_factor == 0) # was -1

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8, cond9]

    assert all(cond)

def test_insert_node_balanced(sample_bst):
    t, nodes = sample_bst
    # the node that will be affected
    n10 = nodes[2]

    t.insert_node(11, True)

    n11 = n10.left # was None

    # the new node
    cond0 = (n11.data == 11)
    cond1 = (n11.left == None)
    cond2 = (n11.right == None)
    cond3 = (n11.status == Tree.node_status.UNVISITED)
    cond4 = (n11.parent == n10)
    cond5 = (n11.height == 0)
    cond6 = (n11.balance_factor == 0)

    cond7 = (n10.balance_factor == -1) # -2

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7]

    assert all(cond)

def test_insertNode_balanced(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1] # subtree root

    # the nodes that will be affected
    n1 = nodes[3]

    t._insertNode(n3, 5, True)

    n5 = n1.left # n1.left was None

    # the new node
    cond0 = (n5.data == 5)
    cond1 = (n5.left == None)
    cond2 = (n5.right == None)
    cond3 = (n5.status == Tree.node_status.UNVISITED)
    cond4 = (n5.parent == n1)
    cond5 = (n5.height == 0)
    cond6 = (n5.balance_factor == 0)

    cond7 = (n1.height == 1) # 0
    cond8 = (n1.balance_factor == 1) # 0

    cond9 = (n3.balance_factor == 0) # -1

    cond = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8, cond9]

    assert all(cond)

def test_height_bf_add_node(sample_bst):
    t,_ = sample_bst
    n8 = t.root

    t.add_node(2)
    t.add_node(5)
    t.add_node(9)
    t.add_node(11)
    t.add_node(15)
    t.add_node(16)
    t.add_node(17)

    cond1 = (n8.height == 5)
    cond2 = (n8.balance_factor == -1)

    assert cond1 and cond2

def test_height_bf_insert_node(sample_bst):
    t,_ = sample_bst
    n8 = t.root

    t.insert_node(2)
    t.insert_node(5)
    t.insert_node(9)
    t.insert_node(11)
    t.insert_node(15)
    t.insert_node(16)
    t.insert_node(17)

    cond1 = (n8.height == 4)
    cond2 = (n8.balance_factor == 1)

    assert cond1 and cond2

def test_inorder_traversal(sample_bst):
    t,_ = sample_bst
    ref_inorder = [1, 3, 4, 6, 7, 8, 10, 13, 14]

    path = []
    t.inorder_traversal(t.root, path)

    inorder = [n.data for n in path]

    assert inorder == ref_inorder

def test_preorder_traversal(sample_bst):
    t,_ = sample_bst
    ref_preorder = [8, 3, 1, 6, 4, 7, 10, 14, 13]

    path = []
    t.preorder_traversal(t.root, path)

    preorder = [n.data for n in path]

    assert preorder == ref_preorder

def test_postorder_traversal(sample_bst):
    t,_ = sample_bst
    ref_postorder = [1, 4, 7, 6, 3, 13, 14, 10, 8]

    path = []
    t.postorder_traversal(t.root, path)

    postorder = [n.data for n in path]

    assert postorder == ref_postorder

def test_find_node(sample_bst):
    t, nodes = sample_bst
    n10 = nodes[2]

    n = t.find_node(2)
    cond1 = (n == None)

    n = t.find_node(10)
    cond2 = (n == n10)

    assert cond1 and cond2

def test_findNode(sample_bst):
    t, nodes = sample_bst
    n3 = nodes[1]
    n6 = nodes[4]

    n = t._findNode(n3, 6)
    cond1 = (n == n6)

    n = t._findNode(n3, 10)
    cond2 = (n == None)

    assert cond1 and cond2

