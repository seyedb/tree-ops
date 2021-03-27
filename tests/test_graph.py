# these tests are designed for pytest framework
import pytest
import graph as Graph
from collections import defaultdict

@pytest.fixture
def dflt_graph():
    """Returns a default initialized graph object."""
    return Graph.graph()

@pytest.fixture
def dflt_graphNode():
    """Returns a default initialized graphNode object."""
    return Graph.graph().graphNode()

@pytest.fixture
def generic_graphNode():
    """Returns a default initialized graphNode object."""
    n = Graph.graph().graphNode('A')
    return n

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
    ref_str = "'A': []"
    assert graphNode_str == ref_str

def test_getStatus(generic_graphNode):
    assert generic_graphNode._getStatus() == Graph.node_status.UNVISITED

def test_setStatus(generic_graphNode):
    generic_graphNode._setStatus(Graph.node_status.VISITED)
    assert generic_graphNode.status == Graph.node_status.VISITED

def test_getData(generic_graphNode):
    assert generic_graphNode._getData() == 'A'

def test_setData(generic_graphNode):
    generic_graphNode._setData('B')
    assert generic_graphNode.data == 'B'
