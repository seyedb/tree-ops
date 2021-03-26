# these tests are designed for pytest framework

import pytest
import tree as Tree
import treeOps as to
import deepdiff
import operator as op

@pytest.fixture
def ref_bst():
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
    # set height manually
    n8.height = 3
    n3.height = 2
    n10.height = 2
    n6.height = 1
    n14.height = 1
    # set balance factor manually
    n10.balance_factor = -2
    n3.balance_factor = -1
    n14.balance_factor = 1

    nodes_tuple = (n8, n3, n10, n1, n6, n14, n4, n7, n13)

    return t, nodes_tuple

def test_list_to_tree():
    dlist = [6, 10, 14, 3, 4, 1, 8, 13, 7]
    t = to.list_to_tree(dlist, rootVal=8, balanced=False)

    ref_rep = [
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 3,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 4, 'parent': 6,
     'status': 'unvisited', 'height': 1, 'balance_factor': 0},
    {'data': 4, 'left': 'None', 'right': 'None', 'parent': 3,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 6, 'left': 3, 'right': 7, 'parent': 8,
     'status': 'unvisited', 'height': 2, 'balance_factor': 1},
    {'data': 7, 'left': 'None', 'right': 'None', 'parent': 6,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 8, 'left': 6, 'right': 10, 'parent': 'None',
     'status': 'unvisited', 'height': 3, 'balance_factor': 0},
    {'data': 10, 'left': 'None', 'right': 14, 'parent': 8,
     'status': 'unvisited', 'height': 2, 'balance_factor': -2},
    {'data': 13, 'left': 'None', 'right': 'None', 'parent': 14,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 14, 'left': 13, 'right': 'None', 'parent': 10,
     'status': 'unvisited', 'height': 1, 'balance_factor': 1}]

    rep = t.verbose_rep(1)
    rep = sorted(rep, key=op.itemgetter('data'))

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 9

    assert cond

def test_list_to_tree_balanced():
    dlist = [6, 10, 14, 3, 4, 1, 8, 13, 7]
    t = to.list_to_tree(dlist, rootVal=8, balanced=True)

    ref_rep = [
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 3,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 'None', 'parent': 4,
     'status': 'unvisited', 'height': 1, 'balance_factor': 1},
    {'data': 4, 'left': 3, 'right': 6, 'parent': 8,
     'status': 'unvisited', 'height': 2, 'balance_factor': 0},
    {'data': 6, 'left': 'None', 'right': 7, 'parent': 4,
     'status': 'unvisited', 'height': 1, 'balance_factor': -1},
    {'data': 7, 'left': 'None', 'right': 'None', 'parent': 6,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 8, 'left': 4, 'right': 13, 'parent': 'None',
     'status': 'unvisited', 'height': 3, 'balance_factor': 1},
    {'data': 10, 'left': 'None', 'right': 'None', 'parent': 13,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0},
    {'data': 13, 'left': 10, 'right': 14, 'parent': 8,
     'status': 'unvisited', 'height': 1, 'balance_factor': 0},
    {'data': 14, 'left': 'None', 'right': 'None', 'parent': 13,
     'status': 'unvisited', 'height': 0, 'balance_factor': 0}]

    rep = t.verbose_rep(1)
    rep = sorted(rep, key=op.itemgetter('data'))

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 9

    assert cond

def test_dict_to_tree(ref_bst):
    ref_t,_ = ref_bst

    ref_rep = ref_t.verbose_rep(1)
    ref_rep = sorted(ref_rep, key=op.itemgetter('data'))

    tdict = {
        1:  {'left': 'None', 'right': 'None'},
        3:  {'left': 1, 'right': 6},
        4:  {'left': 'None', 'right': 'None'},
        6:  {'left': 4, 'right': 7},
        7:  {'left': 'None', 'right': 'None'},
        8:  {'left': 3, 'right': 10},
        10: {'left': 'None', 'right': 14},
        13: {'left': 'None', 'right': 'None'},
        14: {'left': 13, 'right': 'None'}}

    t = to.dict_to_tree(tdict, root_ind=5)

    rep = t.verbose_rep(1)
    rep = sorted(rep, key=op.itemgetter('data'))

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 9

    assert cond
