# these tests are designed for pytest framework
import pytest
import tree as Tree
import treeOps as to
import deepdiff
import operator as op
import string
import collections

@pytest.fixture
def ref_bst():
    """Returns a sample binary search tree and a tuple of its nodes.
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
    """
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

@pytest.fixture
def ref_cbqp():
    """Returns a reference binary quadratic minimization problem."""
    Q = [[ 2, -3,  1],
         [ 2,  0, -1],
         [ 1,  4,  5]]
    A = [[-5,  0, -1],
         [ 1,  2, -1],
         [-3,  4,  1]]
    b = [-2, 3, 4]
    cbqp = to.CBQP(3, Q, A, b)
    return cbqp

def test_list_to_tree():
    dlist = [6, 10, 14, 3, 4, 1, 8, 13, 7]
    t = to.list_to_tree(dlist, rootVal=8, balanced=False)

    ref_rep = [
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 3,
     'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 4, 'parent': 6,
     'height': 1, 'balance_factor': 0},
    {'data': 4, 'left': 'None', 'right': 'None', 'parent': 3,
     'height': 0, 'balance_factor': 0},
    {'data': 6, 'left': 3, 'right': 7, 'parent': 8,
     'height': 2, 'balance_factor': 1},
    {'data': 7, 'left': 'None', 'right': 'None', 'parent': 6,
     'height': 0, 'balance_factor': 0},
    {'data': 8, 'left': 6, 'right': 10, 'parent': 'None',
     'height': 3, 'balance_factor': 0},
    {'data': 10, 'left': 'None', 'right': 14, 'parent': 8,
     'height': 2, 'balance_factor': -2},
    {'data': 13, 'left': 'None', 'right': 'None', 'parent': 14,
     'height': 0, 'balance_factor': 0},
    {'data': 14, 'left': 13, 'right': 'None', 'parent': 10,
     'height': 1, 'balance_factor': 1}]

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
     'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 'None', 'parent': 4,
     'height': 1, 'balance_factor': 1},
    {'data': 4, 'left': 3, 'right': 6, 'parent': 8,
     'height': 2, 'balance_factor': 0},
    {'data': 6, 'left': 'None', 'right': 7, 'parent': 4,
     'height': 1, 'balance_factor': -1},
    {'data': 7, 'left': 'None', 'right': 'None', 'parent': 6,
     'height': 0, 'balance_factor': 0},
    {'data': 8, 'left': 4, 'right': 13, 'parent': 'None',
     'height': 3, 'balance_factor': 1},
    {'data': 10, 'left': 'None', 'right': 'None', 'parent': 13,
     'height': 0, 'balance_factor': 0},
    {'data': 13, 'left': 10, 'right': 14, 'parent': 8,
     'height': 1, 'balance_factor': 0},
    {'data': 14, 'left': 'None', 'right': 'None', 'parent': 13,
     'height': 0, 'balance_factor': 0}]

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

def test_balance_by_recursion(ref_bst):
    t,_ = ref_bst

    balancedt = to.balance_by_recursion(t)

    ref_rep = [
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 3,
     'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 4, 'parent': 7,
     'height': 2, 'balance_factor': -1},
    {'data': 4, 'left': 'None', 'right': 6, 'parent': 3,
     'height': 1, 'balance_factor': -1},
    {'data': 6, 'left': 'None', 'right': 'None', 'parent': 4,
     'height': 0, 'balance_factor': 0},
    {'data': 7, 'left': 3, 'right': 10, 'parent': 'None',
     'height': 3, 'balance_factor': 0},
    {'data': 8, 'left': 'None', 'right': 'None', 'parent': 10,
     'height': 0, 'balance_factor': 0},
    {'data': 10, 'left': 8, 'right': 13, 'parent': 7,
     'height': 2, 'balance_factor': -1},
    {'data': 13, 'left': 'None', 'right': 14, 'parent': 10,
     'height': 1, 'balance_factor': -1},
    {'data': 14, 'left': 'None', 'right': 'None', 'parent': 13,
     'height': 0, 'balance_factor': 0}]

    rep = balancedt.verbose_rep(1)
    rep = sorted(rep, key=op.itemgetter('data'))

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 9

    assert cond

def test_convert_to_AVL(ref_bst):
    t,_ = ref_bst

    balancedt = to.convert_to_AVL(t)

    ref_rep = [
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 3,
     'height': 0, 'balance_factor': 0},
    {'data': 3, 'left': 1, 'right': 4, 'parent': 6,
     'height': 1, 'balance_factor': 0},
    {'data': 4, 'left': 'None', 'right': 'None', 'parent': 3,
     'height': 0, 'balance_factor': 0},
    {'data': 6, 'left': 3, 'right': 8, 'parent': 'None',
     'height': 3, 'balance_factor': -1},
    {'data': 7, 'left': 'None', 'right': 'None', 'parent': 8,
     'height': 0, 'balance_factor': 0},
    {'data': 8, 'left': 7, 'right': 13, 'parent': 6,
     'height': 2, 'balance_factor': -1},
    {'data': 10, 'left': 'None', 'right': 'None', 'parent': 13,
     'height': 0, 'balance_factor': 0},
    {'data': 13, 'left': 10, 'right': 14, 'parent': 8,
     'height': 1, 'balance_factor': 0},
    {'data': 14, 'left': 'None', 'right': 'None', 'parent': 13,
     'height': 0, 'balance_factor': 0}]

    rep = balancedt.verbose_rep(1)
    rep = sorted(rep, key=op.itemgetter('data'))

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 9

    assert cond

def test_text_to_tree():
    """ The reference paragraph (par nr. 151) reads as follows:
    Und so lang du das nicht hast,
    Dieses: Stirb und werde!
    Bist du nur ein trüber Gast
    Auf der dunklen Erde.
    """
    path = "../data/Goethe.txt"
    regex = "(?<!\d )["+string.punctuation+"](?!\d)"
    treelist = to.text_to_tree(path, regex=regex, balanced=False)

    ref = "Auf Bist Dieses Erde Gast Stirb Und das der du du dunklen ein hast lang nicht nur so trüber und werde \n"
    parnr = 151

    assert treelist[parnr].__str__() == ref

def test_find_word():
    path = "../data/Goethe.txt"
    regex = "(?<!\d )["+string.punctuation+"](?!\d)"
    indIntv = [0, 1000]
    wrd = "Nameh"

    ref = [58, 154, 204, 255, 318, 386, 449, 457, 675, 773, 797, 820]
    res = to.find_word(wrd, indIntv, path, regex=regex, balanced=True)

    assert collections.Counter(res) == collections.Counter(ref)

def test_bnums_to_btree():
    length = 2
    t = to.bnums_to_btree(length)
    rep = t.verbose_rep(1)

    ref_rep = [
    {'data': 0, 'left': 'None', 'right': 'None', 'parent': 0, 'height': 0, 'balance_factor': 0},
    {'data': 0, 'left': 0, 'right': 1, 'parent': 'root', 'height': 1, 'balance_factor': 0},
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 0, 'height': 0, 'balance_factor': 0},
    {'data': 'root', 'left': 0, 'right': 1, 'parent': 'None', 'height': 2, 'balance_factor': 0},
    {'data': 0, 'left': 'None', 'right': 'None', 'parent': 1, 'height': 0, 'balance_factor': 0},
    {'data': 1, 'left': 0, 'right': 1, 'parent': 'root', 'height': 1, 'balance_factor': 0},
    {'data': 1, 'left': 'None', 'right': 'None', 'parent': 1, 'height': 0, 'balance_factor': 0}]

    diff_list = [deepdiff.DeepDiff(n1, n2) for n1, n2 in zip(rep, ref_rep)]
    cond = diff_list == [{}] * 7

    assert cond

def test__init__cbqp():
    cbqp = to.CBQP(2, [[1, 2],[3, 4]], [[1, 0],[0, 1]],[1, 1])
    assert cbqp.binary_length == 2 and cbqp.Q == [[1, 2],[3, 4]] and cbqp.A == [[1, 0],[0, 1]] and cbqp.b == [1, 1]

def test_solve_CBQP(ref_cbqp):
    assert ref_cbqp.solve_CBQP() == ([1, 1, 0], 1.0)

def test_isFeasible(ref_cbqp):
    x = [0, 0, 1]
    assert ref_cbqp._isFeasible(x) == False

def test_evalObjFunc(ref_cbqp):
    x = [0, 0, 1]
    assert ref_cbqp._evalObjFunc(x) == 5.0

def test_solve():
    t = to.bnums_to_btree(3)
    Q = [[2, 3, -1],
         [7, -5, 3],
         [4,  6, 0]]
    A = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
    b = [7, 16, 20]
    cbqp = to.CBQP(3, Q, A, b)
    cbqp._solve(t, t.root, [])
    assert cbqp.optimal_value == -5.0 and cbqp.solution == [0, 1, 0]
