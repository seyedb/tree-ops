# these tests are designed for pytest framework
import pytest
import graph as Graph
import graphOps as go

@pytest.fixture
def petersen():
    """Returns a Petersen graph - GP(5,2)."""
    GP = Graph.graph()
    na = Graph.graph().graphNode('a')
    nb = Graph.graph().graphNode('b')
    nc = Graph.graph().graphNode('c')
    nd = Graph.graph().graphNode('d')
    ne = Graph.graph().graphNode('e')
    nf = Graph.graph().graphNode('f')
    ng = Graph.graph().graphNode('g')
    nh = Graph.graph().graphNode('h')
    ni = Graph.graph().graphNode('i')
    nj = Graph.graph().graphNode('j')

    na.children[nb], nb.children[na] = [0.0], [0.0]
    na.children[nf], nf.children[na] = [0.0], [0.0]
    na.children[ne], ne.children[na] = [0.0], [0.0]
    nb.children[nc], nc.children[nb] = [0.0], [0.0]
    nb.children[ng], ng.children[nb] = [0.0], [0.0]
    nc.children[nd], nd.children[nc] = [0.0], [0.0]
    nc.children[nh], nh.children[nc] = [0.0], [0.0]
    nd.children[ne], ne.children[nd] = [0.0], [0.0]
    nd.children[ni], ni.children[nd] = [0.0], [0.0]
    ne.children[nj], nj.children[ne] = [0.0], [0.0]
    nf.children[nh], nh.children[nf] = [0.0], [0.0]
    nf.children[ni], ni.children[nf] = [0.0], [0.0]
    ng.children[ni], ni.children[ng] = [0.0], [0.0]
    ng.children[nj], nj.children[ng] = [0.0], [0.0]
    nh.children[nj], nj.children[nh] = [0.0], [0.0]

    GP.vertices[na][nb], GP.vertices[nb][na] = [0.0], [0.0]
    GP.vertices[nb][nc], GP.vertices[nc][nb] = [0.0], [0.0]
    GP.vertices[nc][nd], GP.vertices[nd][nc] = [0.0], [0.0]
    GP.vertices[na][ne], GP.vertices[ne][na] = [0.0], [0.0]
    GP.vertices[na][nf], GP.vertices[nf][na] = [0.0], [0.0]
    GP.vertices[nb][ng], GP.vertices[ng][nb] = [0.0], [0.0]
    GP.vertices[nc][nh], GP.vertices[nh][nc] = [0.0], [0.0]
    GP.vertices[nd][ne], GP.vertices[ne][nd] = [0.0], [0.0]
    GP.vertices[nd][ni], GP.vertices[ni][nd] = [0.0], [0.0]
    GP.vertices[ne][nj], GP.vertices[nj][ne] = [0.0], [0.0]
    GP.vertices[nf][nh], GP.vertices[nh][nf] = [0.0], [0.0]
    GP.vertices[nf][ni], GP.vertices[ni][nf] = [0.0], [0.0]
    GP.vertices[ng][ni], GP.vertices[ni][ng] = [0.0], [0.0]
    GP.vertices[ng][nj], GP.vertices[nj][ng] = [0.0], [0.0]
    GP.vertices[nh][nj], GP.vertices[nj][nh] = [0.0], [0.0]

    vx_tuple = (na, nb, nc, nd, ne, nf, ng, nh, ni, nj)

    return GP, vx_tuple

def test_graph_to_adjmat(petersen):
    g,_ = petersen
    adjMat, adjMatw = go.graph_to_adjmat(g)

    ref_adjMat = [
    [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 0, 0]]

    ref_adjMatw = [
    [[], [0.0], [], [], [0.0], [0.0], [], [], [], []],
    [[0.0], [], [0.0], [], [], [], [0.0], [], [], []],
    [[], [0.0], [], [0.0], [], [], [], [0.0], [], []],
    [[], [], [0.0], [], [0.0], [], [], [], [0.0], []],
    [[0.0], [], [], [0.0], [], [], [], [], [], [0.0]],
    [[0.0], [], [], [], [], [], [], [0.0], [0.0], []],
    [[], [0.0], [], [], [], [], [], [], [0.0], [0.0]],
    [[], [], [0.0], [], [], [0.0], [], [], [], [0.0]],
    [[], [], [], [0.0], [], [0.0], [0.0], [], [], []],
    [[], [], [], [], [0.0], [], [0.0], [0.0], [], []]]

    assert adjMat == ref_adjMat and adjMatw == ref_adjMatw
