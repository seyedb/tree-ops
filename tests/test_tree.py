# these tests are designed for pytest framework

import pytest
import tree as Tree

@pytest.fixture
def dflt_tree():
    '''Retunrs a default initialized tree object'''
    return Tree.tree()

@pytest.fixture
def dflt_treeNode():
    '''Retunrs a default initialized treeNode object'''
    return Tree.tree().treeNode()

@pytest.fixture
def simple_tree():
    '''Retunrs a simple tree with 3 nodes: root, its left and right nodes'''
    smpl_tree = Tree.tree()
    root = Tree.tree().treeNode('root')
    left = Tree.tree().treeNode('left')
    right = Tree.tree().treeNode('right')
    smpl_tree.root = root
    root.left = left
    root.right = right

    return smpl_tree

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

def test__str__(simple_tree):
    tree_str = simple_tree.__str__()
    assert tree_str == "left root right \n"
