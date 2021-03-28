# these tests are designed for pytest framework
import pytest
import graph as Graph
from collections import Counter, defaultdict
import deepdiff

@pytest.fixture
def dflt_graph():
    """Returns a default initialized graph object."""
    return Graph.graph()

@pytest.fixture
def dflt_graphNode():
    """Returns a default initialized graphNode object."""
    return Graph.graph().graphNode()

@pytest.fixture
def generic_graph():
    """Returns a simple graph with three vertices: A, B, C and edges A -- B, A -- C"""
    g = Graph.graph()
    na = Graph.graph().graphNode('A')
    nb = Graph.graph().graphNode('B')
    nc = Graph.graph().graphNode('C')
    na.children[nb], nb.children[na] = [0.0], [0.0]
    na.children[nc], nc.children[na] = [0.0], [0.0]
    g.vertices[na][nb], g.vertices[nb][na] = [0.0], [0.0]
    g.vertices[na][nc], g.vertices[nc][na] = [0.0], [0.0]

    vx_tuple = (na, nb, nc)

    return g, vx_tuple

@pytest.fixture
def generic_graphNode():
    """Returns a simple graphNode."""
    n = Graph.graph().graphNode('X')
    return n

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

def test_default_graph(dflt_graph):
    assert dflt_graph.vertices == defaultdict(None, {})

def test_default_graphNode(dflt_graphNode):
    dflt_data = (dflt_graphNode.data == None)
    dflt_children = (dflt_graphNode.children == defaultdict(list, {}))
    dflt_status = (dflt_graphNode.status == Graph.node_status.UNVISITED)
    dflt_distance = (dflt_graphNode.distance == float('inf'))
    dflt_previous = (dflt_graphNode.previous == None)
    assert dflt_data and dflt_children and dflt_status and dflt_distance and dflt_previous

def test__lt__():
    n1 = Graph.graph().graphNode('A')
    n2 = Graph.graph().graphNode('B')
    n3 = Graph.graph().graphNode('C')
    assert (n1 < n2 and n3 > n2)

def test__le__():
    n1 = Graph.graph().graphNode('A')
    n2 = Graph.graph().graphNode('A')
    assert (n2 <= n1)

def test_graphNode__str__(generic_graphNode):
    graphNode_str = generic_graphNode.__str__()
    ref_str = "'X': []"
    assert graphNode_str == ref_str

def test_getStatus(generic_graphNode):
    assert generic_graphNode._getStatus() == Graph.node_status.UNVISITED

def test_setStatus(generic_graphNode):
    generic_graphNode._setStatus(Graph.node_status.VISITED)
    assert generic_graphNode.status == Graph.node_status.VISITED

def test_getData(generic_graphNode):
    assert generic_graphNode._getData() == 'X'

def test_setData(generic_graphNode):
    generic_graphNode._setData('Y')
    assert generic_graphNode.data == 'Y'

def test_addAdjNode(generic_graphNode):
    adj_node = Graph.graph().graphNode('Y')
    generic_graphNode._addAdjNode(adj_node, weight=2)
    l = [[k.data, v] for k, v in generic_graphNode.children.items()]
    assert l == [['Y', [2]]]

def test_getChildren(generic_graphNode):
    adj_node = Graph.graph().graphNode('Y')
    generic_graphNode._addAdjNode(adj_node, weight=2)
    l = [n.data for n in generic_graphNode._getChildren()]
    assert l == ['Y']

def test_getDistance(generic_graphNode):
    assert generic_graphNode._getDistance() == float('inf')

def test_setDistance(generic_graphNode):
    generic_graphNode._setDistance(2.2)
    assert generic_graphNode.distance == 2.2

def test_getPrevious(generic_graphNode):
    assert generic_graphNode._getPrevious() == None

def test_setPrevious(generic_graphNode):
    n = Graph.graph().graphNode('Y')
    generic_graphNode._setPrevious(n)
    assert generic_graphNode.previous == n

def test_getWeight(generic_graphNode):
    adj_node = Graph.graph().graphNode('Y')
    generic_graphNode._addAdjNode(adj_node, weight=2)
    assert generic_graphNode._getWeight(adj_node) == [2.0]

def test_isAdjacent(generic_graphNode):
    n = Graph.graph().graphNode('Y')
    adj_node = Graph.graph().graphNode('Y')
    generic_graphNode._addAdjNode(adj_node, weight=2)

    assert generic_graphNode._isAdjacent(adj_node) and not generic_graphNode._isAdjacent(n)

def test_graph__str__(petersen):
    g,_ = petersen
    graph_str = g.__str__()
    ref_str = (
    "'a': [['b', [0.0]], ['f', [0.0]], ['e', [0.0]]]\n"
    "'b': [['a', [0.0]], ['c', [0.0]], ['g', [0.0]]]\n"
    "'c': [['b', [0.0]], ['d', [0.0]], ['h', [0.0]]]\n"
    "'d': [['c', [0.0]], ['e', [0.0]], ['i', [0.0]]]\n"
    "'e': [['a', [0.0]], ['d', [0.0]], ['j', [0.0]]]\n"
    "'f': [['a', [0.0]], ['h', [0.0]], ['i', [0.0]]]\n"
    "'g': [['b', [0.0]], ['i', [0.0]], ['j', [0.0]]]\n"
    "'h': [['c', [0.0]], ['f', [0.0]], ['j', [0.0]]]\n"
    "'i': [['d', [0.0]], ['f', [0.0]], ['g', [0.0]]]\n"
    "'j': [['e', [0.0]], ['g', [0.0]], ['h', [0.0]]]\n")

    assert graph_str == ref_str

def test_reset(petersen):
    g, vxs = petersen

    na = vxs[0]
    nd = vxs[3]
    ng = vxs[6]
    nj = vxs[9]

    # the original values
    orig = []
    for v in g.vertices:
        if v.data == 'a' or v.data == 'd' or v.data == 'g':
            orig.append((v.data, v.status, v.distance, v.previous))

    # for the sake of testing, change attributes of some of the vertices
    na.status = Graph.node_status.VISITED
    nd.distance = 10.0
    ng.previous = nj

    # now reset
    g.reset()
    res = []
    for v in g.vertices:
        if v.data == 'a' or v.data == 'd' or v.data == 'g':
            res.append((v.data, v.status, v.distance, v.previous))

    print(orig == res)

def test__contains__(petersen):
    g,_ = petersen
    assert ('d' in g) and (not 'D' in g)

def test_getVerticesDict(petersen):
    g,_ = petersen
    ref = g.vertices
    diff = deepdiff.DeepDiff(ref, g._getVerticesDict())
    assert diff == {}

def test_getEdges(petersen):
    g,_ = petersen
    ref = [('a','b',0.0), ('b','a',0.0), ('a','f',0.0), ('f','a',0.0),
           ('a','e',0.0), ('e','a',0.0), ('b','g',0.0), ('g','b',0.0),
           ('b','c',0.0), ('c','b',0.0), ('c','h',0.0), ('h','c',0.0),
           ('c','d',0.0), ('d','c',0.0), ('d','i',0.0), ('i','d',0.0),
           ('d','e',0.0), ('e','d',0.0), ('e','j',0.0), ('j','e',0.0),
           ('f','h',0.0), ('h','f',0.0), ('f','i',0.0), ('i','f',0.0),
           ('g','i',0.0), ('i','g',0.0), ('g','j',0.0), ('j','g',0.0),
           ('h','j',0.0), ('j','h',0.0)]

    edges = []
    for e in g._getEdges():
        edges.append((e[0].data, e[1].data, e[2]))

    assert Counter(edges) == Counter(ref)

def test_getVertex(petersen):
    g, vxs = petersen
    nd = vxs[3]
    assert g._getVertex('d') == nd

def test_add_vertex(generic_graph):
    g,_ = generic_graph
    cond1 = 'D' in g
    g.add_vertex('D')
    cond2 = 'D' in g
    assert (not cond1) and cond2

def test_add_edge(generic_graph):
    g,_ = generic_graph
    g.add_edge('B', 'C', 3.14)

    graph_str = g.__str__()
    ref_str = (
    "'A': [['B', [0.0]], ['C', [0.0]]]\n"
    "'B': [['A', [0.0]], ['C', [3.14]]]\n"
    "'C': [['A', [0.0]], ['B', [3.14]]]\n")

    assert graph_str == ref_str

def test_add_edge_directed(generic_graph):
    g,_ = generic_graph
    g.add_edge('B', 'C', 3.14, True)

    graph_str = g.__str__()
    ref_str = (
    "'A': [['B', [0.0]], ['C', [0.0]]]\n"
    "'B': [['A', [0.0]], ['C', [3.14]]]\n"
    "'C': [['A', [0.0]]]\n")

    assert graph_str == ref_str

def test_isMultigraph(generic_graph):
    g,_ = generic_graph
    g.add_edge('A', 'B', 3.14)
    assert g._isMultigraph()

def test_DFS(petersen):
    g,_ = petersen
    ref_dfs = ['a', 'b', 'c', 'd', 'e', 'j', 'g', 'i', 'f', 'h']

    path = []
    g.DFS('a', path)
    dfs = [vx.data for vx in path]

    assert dfs == ref_dfs

def test_BFS(petersen):
    g,_ = petersen
    ref_bfs = ['a', 'b', 'f', 'e', 'c', 'g', 'h', 'i', 'd', 'j']

    path = g.BFS('a')
    bfs = [vx.data for vx in path]

    assert bfs == ref_bfs
