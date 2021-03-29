# these tests are designed for pytest framework
import pytest
import graph as Graph
import graphOps as go
from collections import Counter

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

def _compare(GP, g):
    petersen_vertices = GP._getVerticesDict()
    petersen_vxs = []
    for vx in petersen_vertices.keys():
        petersen_vxs.append(vx)
    petersen_nvx = len(petersen_vxs)
    petersen_vxlist = []
    petersen_edgelist = []
    petersen_adjlist = []
    for i in range(petersen_nvx):
        v = petersen_vxs[i]
        petersen_vxlist.append(v.data)
        for child, weight in v.children.items():
            petersen_edgelist.append((v.data, child.data, *weight))
        for j in range(petersen_nvx):
            w = petersen_vxs[j]
            petersen_adjlist.append((v.data, w.data, *petersen_vertices[v][w]))

    vertices = g._getVerticesDict()
    g_vxs = []
    for vx in vertices.keys():
        g_vxs.append(vx)
    g_nvx = len(g_vxs)
    g_vxlist = []
    g_edgelist = []
    g_adjlist = []
    for i in range(g_nvx):
        v = g_vxs[i]
        g_vxlist.append(v.data)
        for child, weight in v.children.items():
            g_edgelist.append((v.data, child.data, *weight))
        for j in range(g_nvx):
            w = g_vxs[j]
            g_adjlist.append((v.data, w.data, *vertices[v][w]))

    return Counter(g_vxlist) == Counter(petersen_vxlist) and  \
           Counter(g_edgelist) == Counter(petersen_edgelist) and \
           Counter(g_adjlist) == Counter(petersen_adjlist)

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

def test_adjmat_to_graph(petersen):
    GP,_ = petersen

    adjMat = [
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

    vxdatalist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    g = go.adjmat_to_graph(adjMat, vxdatalist=vxdatalist, directed=False)

    assert _compare(GP, g)

def test_adjmat_to_graph_adjMatw(petersen):
    GP,_ = petersen

    adjMat = [
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

    vxdatalist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    g = go.adjmat_to_graph(adjMat, vxdatalist=vxdatalist, directed=False)

    assert _compare(GP, g)

def test_edges_to_graph(petersen):
    GP,_ = petersen

    edges = {('a', 'b', 0.0), ('a', 'e', 0.0), ('a', 'f', 0.0),
             ('b', 'a', 0.0), ('b', 'c', 0.0), ('b', 'g', 0.0),
             ('c', 'b', 0.0), ('c', 'd', 0.0), ('c', 'h', 0.0),
             ('d', 'c', 0.0), ('d', 'e', 0.0), ('d', 'i', 0.0),
             ('e', 'a', 0.0), ('e', 'd', 0.0), ('e', 'j', 0.0),
             ('f', 'a', 0.0), ('f', 'h', 0.0), ('f', 'i', 0.0),
             ('g', 'b', 0.0), ('g', 'i', 0.0), ('g', 'j', 0.0),
             ('h', 'c', 0.0), ('h', 'f', 0.0), ('h', 'j', 0.0),
             ('i', 'd', 0.0), ('i', 'f', 0.0), ('i', 'g', 0.0),
             ('j', 'e', 0.0), ('j', 'g', 0.0), ('j', 'h', 0.0)}

    g = go.edges_to_graph(edges, directed=False)

    assert _compare(GP, g)

def test_file_to_graph(petersen):
    GP,_ = petersen

    fin = "../data/petersen.dat"
    g = go.file_to_graph(fin, directed=False)

    assert _compare(GP, g)

def test_remap_vertex_data(petersen):
    GP,_ = petersen
    vxdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    go.remap_vertex_data(GP, vxdata)
    graph_str = GP.__str__()
    ref_str = (
    "'0': [[1, [0.0]], [5, [0.0]], [4, [0.0]]]\n"
    "'1': [[0, [0.0]], [2, [0.0]], [6, [0.0]]]\n"
    "'2': [[1, [0.0]], [3, [0.0]], [7, [0.0]]]\n"
    "'3': [[2, [0.0]], [4, [0.0]], [8, [0.0]]]\n"
    "'4': [[0, [0.0]], [3, [0.0]], [9, [0.0]]]\n"
    "'5': [[0, [0.0]], [7, [0.0]], [8, [0.0]]]\n"
    "'6': [[1, [0.0]], [8, [0.0]], [9, [0.0]]]\n"
    "'7': [[2, [0.0]], [5, [0.0]], [9, [0.0]]]\n"
    "'8': [[3, [0.0]], [5, [0.0]], [6, [0.0]]]\n"
    "'9': [[4, [0.0]], [6, [0.0]], [7, [0.0]]]\n")

    assert graph_str == ref_str

def test_adjmatType():
    A = [[0, 1, 1, 1],
         [1, 0, 0, 0],
         [1, 0, 0, 0],
         [1, 0, 0, 0]]

    B = [[[],    [0.0], [0.0], [0.0]],
         [[0,0], [],    [],    []   ],
         [[0.0], [],    [],    []   ],
         [[0.0], [],    [],    []   ]]

    typeofA = go._adjmatType(A)
    typeofB = go._adjmatType(B)

    assert typeofA == int and typeofB == list

def test_dfs_in_adjmat():
    adjMat = [
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

    # the following corresponds to ['a', 'b', 'c', 'd', 'e', 'j', 'g', 'i', 'f', 'h']
    ref_dfs = [0, 1, 2, 3, 4, 9, 6, 8, 5, 7]

    nvx = len(adjMat)
    visited = [False for i in range(nvx)]
    start = 0
    dfs = [start]
    go.dfs_in_adjmat(adjMat, start, visited, dfs)

    assert dfs == ref_dfs

def test_dfs_in_adjmatw():
    adjMat = [
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

    # the following corresponds to ['a', 'b', 'c', 'd', 'e', 'j', 'g', 'i', 'f', 'h']
    ref_dfs = [0, 1, 2, 3, 4, 9, 6, 8, 5, 7]

    nvx = len(adjMat)
    visited = [False for i in range(nvx)]
    start = 0
    dfs = [start]
    go.dfs_in_adjmatw(adjMat, start, visited, dfs)

    assert dfs == ref_dfs

def test_bfs_in_adjmat():
    adjMat = [
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

    # the following corresponds to ['a', 'b', 'e', 'f', 'c', 'g', 'd', 'j', 'h', 'i']
    ref_bfs = [0, 1, 4, 5, 2, 6, 3, 9, 7, 8]

    nvx = len(adjMat)
    visited = [False for i in range(nvx)]
    start = 0
    bfs = go.bfs_in_adjmat(adjMat, start, visited)

    assert bfs == ref_bfs

def test_bfs_in_adjmatw():
    adjMat = [
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

    # the following corresponds to ['a', 'b', 'e', 'f', 'c', 'g', 'd', 'j', 'h', 'i']
    ref_bfs = [0, 1, 4, 5, 2, 6, 3, 9, 7, 8]

    nvx = len(adjMat)
    visited = [False for i in range(nvx)]
    start = 0
    bfs = go.bfs_in_adjmatw(adjMat, start, visited)

    assert bfs == ref_bfs

def test_connected_components():
    adjMat = [[0, 1, 1, 1, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 1, 1],
              [0, 0, 0, 0, 1, 0, 1],
              [0, 0, 0, 0, 1, 1, 0]]

    adjMatw = [[[], [0.0], [0.0], [0.0], [],    [],    []],
               [[0,0], [],    [],    [], [],    [],    []],
               [[0.0], [],    [],    [], [],    [],    []],
               [[0.0], [],    [],    [], [],    [],    []],
               [[],    [],    [],    [], [], [0.0], [0.0]],
               [[],    [],    [],    [], [0.0], [], [0.0]],
               [[],    [],    [],    [], [0.0], [0.0], []]]

    components_adjmat = go.connected_components(adjMat)
    components_adjmatw = go.connected_components(adjMatw)
    ref = [[0, 1, 2, 3], [4, 5, 6]]

    assert components_adjmat == components_adjmatw == ref

