#
import graph
import heapq as hq
from collections import deque

def graph_to_adjmat(g):
    """Given a graph returns the corresponding adjacency matrix.
    
    Args:
        g (graph): a graph object.
    Returns:
        (2D - nested - list) adjacency matrix: a_ij = 1 if vi and vj are adjacent , 0 otherwise.
        (2D - nested - list) adjacency matrix: a_ij = weight of the edges between adjacent vertices vi and vj , empty list otherwise.
    """
    vertices = g._getVerticesDict()
    nvx = len(vertices)

    vxdata = []
    for vx in vertices.keys():
        vxdata.append(vx._getData())

    adjMat = [[0 for i in range(nvx)] for j in range(nvx)]
    adjMatw = [[[] for i in range(nvx)] for j in range(nvx)]

    for vx, vxchildren in vertices.items():
        for child, weight in vxchildren.items():
            r = vxdata.index(vx._getData())
            c = vxdata.index(child._getData())
            adjMat[r][c] = 1
            adjMatw[r][c] = weight
    
    return adjMat, adjMatw

def adjmat_to_graph(adjMat, vxdatalist=[], directed=False):
    """Given an adjacency matrix retruns the corresponding (multi)graph.

    Args:
        adjMat (2d - nested - list): the adjacency matrix.
        vxdatalist (list): list of data to be assigned to the verices of the graph.
    Returns:
        (graph) a graph that has the same adjacency matrix as the given matrix.
    """
    assert(adjMat), "The adjacency matrix is empty."

    g = graph.graph()

    nvx = len(adjMat)
    if vxdatalist:
        assert(nvx == len(vxdatalist)), "Provide the right number of vertex data or leave the list empty."

    if not vxdatalist:
        for i in range(nvx):
            vxdatalist.append(str(i))

    for vxdata in vxdatalist:
        g.add_vertex(vxdata)

    if _adjmatType(adjMat) is list:
        for i in range(nvx):
            for j in range(nvx):
                for w in adjMat[i][j]:
                    g.add_edge(vxdatalist[i], vxdatalist[j], weight=w, directed=directed)
    elif _adjmatType(adjMat) is int:
        for i in range(nvx):
            for j in range(nvx):
                if adjMat[i][j] == 1:
                    g.add_edge(vxdatalist[i], vxdatalist[j], directed=directed)
    else:
        print("Warning: The adjacency matrix contains unsupported data type!")

    return g

def edges_to_graph(edges, directed=False):
    """Converts a set of edges into a graph.

    Args:
        edges (set of tuples): set of edges represented as tuples (v1, v2, w).
        directed (boolean): whether or not the graph is a directed graph.
    Returns:
        (graph) a graph object that has vertices and edges matching with the given edge data.
    """
    g = graph.graph()

    vxdata = set()
    for edge in edges:
        vxdata.add(edge[0])
        vxdata.add(edge[1])

    for vx in vxdata:
        g.add_vertex(vx)

    for edge in edges:
        g.add_edge(edge[0], edge[1], weight=edge[2], directed=directed)

    return g

def file_to_graph(fin, directed=False):
    """Constructs a graph based on data stored in a file.

    NOTE:
        - The file must have the following format:
          The first line is the number of vertices.
          The second line is the number of edges.
          The rest of the file is in the form of 3 space-separated columns storing edge information as v1 v2 w.

    Args:
        fin (str): path to the file.
        directed (boolean): whether or not the graph is a directed graph.
    Returns:
        (graph) a graph object that has vertices and edges matching with the loaded data from the input file.
    """
    g = graph.graph()

    edges = set()
    with open(fin, 'r') as fid:
        nvx = int(fid.readline())
        ne = int(fid.readline())
        for _, line in enumerate(fid):
            edge = line.strip().split()
            edges.add((edge[0], edge[1], float(edge[2])))

    vxdata = set()
    for edge in edges:
        vxdata.add(edge[0])
        vxdata.add(edge[1])

    for vx in vxdata:
        g.add_vertex(vx)

    # we might have isolated nodes
    if nvx > len(vxdata):
        nvx_extra = nvx - len(vxdata)
        print("Warning! based on the provided data, {} isolated vertices had to be added to the graph.".format(nvx_extra))
        for i in range(nvx_extra):
            g.add_vertex(str(i))
    elif nvx < len(vxdata):
        print("Warning! the number of vertices (the first line of the file) doesn't match with the edge data.\n"+
              "A graph is constructed based on the edge data.")

    for edge in edges:
        g.add_edge(edge[0], edge[1], weight=edge[2], directed=directed)

    return g

def remap_vertex_data(g, new_vxdata):
    """Remaps vertex data to a new list.

    Args:
        g (graph): a graph object.
        new_vxdata (list): a new list of data to be assigned to the graph nodes.
    Returns:
        (graph) the input graph with new data assigned to its vertices.
    """
    vertices = g._getVerticesDict()
    nvx = len(vertices)
    assert(nvx == len(new_vxdata)), "Provide the right number of vertex data."

    vxdata = []
    for vx in vertices.keys():
        vxdata.append(vx._getData())

    datamap = {}
    for i in range(nvx):
        datamap[vxdata[i]] = new_vxdata[i]
    print("The vertex data are remapped according to the following mapping:\n", datamap)

    i = 0
    for vx in vertices.keys():
        # make sure the mapping goes according to the plan
        if vx._getData() == vxdata[i]:
            vx._setData(new_vxdata[i])
        i += 1

    return g

def _adjmatType(adjMat):
    """(helper function) retruns <class 'int'> if the adjacency matrix is a (0,1)-matrix, and
    returns <class 'list'> if the adjacency matrix contains edge weights, and returns None if
    neither of the cases occurs.

    Args:
        adjMat (2D - nested - list): the adjacency matrix.
    Returns:
        (type) the type of the adjacency matrix as explained above.
    """
    checktype = {all(isinstance(entry, list) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return list

    checktype = {all(isinstance(entry, int) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return int

    return None    

def dfs_in_adjmat(adjMat, start, visited, path):
    """Performs DFS in a (0,1) adjacency matrix.

    NOTE:
        - The result is a list of the indices of the vertices. The indices are in accordance with the 
        indexing that has led to the adjacency matrix. 

    Args:
        adjMat (2D - nested - list): the adjacency matrix.
        start (int): the index of the vertex where the procedure starts.
        visited (list of boolean): a list keeping track of the visit status of the vertices.
        path (list of int): the DFS path.
    Returns:
        (list of int) the full DFS path starting from the given vertex.
    """
    visited[start] = True

    nvx = len(adjMat)
    for i in range(nvx):
        if adjMat[start][i] == 1 and not visited[i]:
            path.append(i)
            dfs_in_adjmat(adjMat, i, visited, path)

def dfs_in_adjmatw(adjMatw, start, visited, path):
    """Same as dfs_in_adjmat but works with an adjacency matrix that contains edge weights."""
    visited[start] = True

    nvx = len(adjMatw)
    for i in range(nvx):
        if adjMatw[start][i] and not visited[i]:
            path.append(i)
            dfs_in_adjmatw(adjMatw, i, visited, path)

def bfs_in_adjmat(adjMat, start, visited):
    """Performs BFS in a (0,1) adjacency matrix.

    NOTE:
        - The result is a list of the indices of the vertices. The indices are in accordance with the 
        indexing that has led to the adjacency matrix. 

    Args:
        adjMat (2D - nested - list): the adjacency matrix.
        start (int): the index of the vertex where the procedure starts.
        visited (list of boolean): a list keeping track of the visit status of the vertices.
    Returns:
        (list of int) the full BFS path starting from the given vertex.
    """
    nvx = len(adjMat)

    visited[start] = True
    path = []

    Q = deque()
    Q.append(start)
    while Q:
        k = Q.popleft()

        for i in range(nvx):
            if adjMat[k][i] == 1 and not visited[i]:
                visited[i] = True
                Q.append(i)

        visited[k] = True
        path.append(k)

    return path

def bfs_in_adjmatw(adjMatw, start, visited):
    """Same as bfs_in_adjmat but works with an adjacency matrix that contains edge weights."""
    nvx = len(adjMatw)

    visited[start] = True
    path = []

    Q = deque()
    Q.append(start)
    while Q:
        k = Q.popleft()

        for i in range(nvx):
            if adjMatw[k][i] and not visited[i]:
                visited[i] = True
                Q.append(i)

        visited[k] = True
        path.append(k)

    return path

def connected_components(adjMat):
    """Returns the connected components of a graph (Uses DFS).

    Args:
        adjMat (2D - nested - list): the adjacency matrix.
    Returns:
        (nested list) list of connected components. Every component is a list of indices representing 
        vertices of the graph. The indices agree with the matrix indexing.
    """
    components = []

    nvx = len(adjMat)
    visited = [False for i in range(nvx)]

    if _adjmatType(adjMat) is list:
        for i in range(nvx):
            if not visited[i]:
                start = i
                path = [start]
                dfs_in_adjmatw(adjMat, start, visited, path)
#                path = bfs_in_adjmatw(adjMat, start, visited)
                components.append(path)
    elif _adjmatType(adjMat) is int:
        for i in range(nvx):
            if not visited[i]:
                start = i
                path = [start]
                dfs_in_adjmat(adjMat, start, visited, path)
#                path = bfs_in_adjmat(adjMat, start, visited)
                components.append(path)
    else:
        print("The adjacency matrix contains unsupported data type.")

    return components

def Dijkstra(g, source, destination):
    """Dijkstra's shortest path algorithm.

    Args:
        g (graph): a graph object.
        source (node val data type): the data of the source node.
        destination (node val data type): the data of the destination node.
    Returns:
        (list) the shortest path from the source to the destination : list of the (data of the) vertices on the path.
        (float) the length of the shortest path (sum of the weights of the constituent edges).
    """
    assert (not g._isMultigraph()), "The Dijkstra's algorithm is not implemented for multigraphs!"

    start = g._getVertex(source)
    end = g._getVertex(destination)

    start._setDistance(0)
    vertices = g._getVerticesDict()
    nvx = len(vertices)

    Q = [(vx._getDistance(), vx) for vx in vertices.keys()]
    hq.heapify(Q)

    while len(Q):
        _, u = hq.heappop(Q)
        u._setStatus(graph.node_status.VISITED)

        if u == end: break

        for child in u._getChildren():
            if child._getStatus() == graph.node_status.VISITED:
                continue
            alt = u._getDistance() + float(u._getWeight(child)[0])

            if alt < child._getDistance():
                child._setDistance(alt)
                child._setPrevious(u)
                hq.heappush(Q, (alt, child))

    SPT = []
    x = end
    if (x._getPrevious() is not None) or (x == start):
        while x is not None:
            SPT.insert(0, x._getData())
            x = x._getPrevious()

    distance = end._getDistance()

    return SPT, distance

def Dijkstra_shortest_path(g, source):
    """Returns the shortest path between a source and all the other verices of a graph using the Dijkstra's algorithm.

    Args:
        g (graph): a graph object.
        source (node val data type): the data of the source node.
    Returns:
        (list) the shortest path from the source to all the vertices : elements are [src, dest, distance].
    """
    assert (not g._isMultigraph()), "The Dijkstra's algorithm is not implemented for multigraphs!"
    g.reset()

    start = g._getVertex(source)
    start._setDistance(0)
    vertices = g._getVerticesDict()
    nvx = len(vertices)

    Q = [(vx._getDistance(), vx) for vx in vertices.keys()]
    hq.heapify(Q)

    while len(Q):
        _, u = hq.heappop(Q)
        u._setStatus(graph.node_status.VISITED)

        for child in u._getChildren():
            if child._getStatus() == graph.node_status.VISITED:
                continue
            alt = u._getDistance() + float(u._getWeight(child)[0])

            if alt < child._getDistance():
                child._setDistance(alt)
                child._setPrevious(u)
                hq.heappush(Q, (alt, child))

    sp = []
    for vx in vertices.keys():
        sp.append([source, vx._getData(), vx._getDistance()])

    return sp

def Bellman_Ford(g, source, destination):
    """Bellman-Ford shortest path algorithm.

    NOTE:
        - It is a dynamic programming algorithm.
        - Compared to Dijkstra, handles multigraphs as well as graphs with negative edge weights.

    Args:
        g (graph): a graph object.
        source (node val data type): the data of the source node.
        destination (node val data type): the data of the destination node.
    Returns:
        (list) the shortest path from the source to the destination : list of the (data of the) vertices on the path.
        (float) the length of the shortest path (sum of the weights of the constituent edges).
    """
    g.reset()

    edges = g._getEdges()
    ne = len(edges)

    start = g._getVertex(source)
    end = g._getVertex(destination)

    start._setDistance(0)

    for _ in range(ne):
        for a, b, w in edges:
            alt = a._getDistance() + float(w)
            if alt < b._getDistance():
                b._setDistance(alt)
                b._setPrevious(a)

    for a, b, w in edges:
        alt = a._getDistance() + float(w)
        if alt < b._getDistance():
            print("Error! graph contains a negative-weight cycle.")

    spt = []
    x = end
    if (x._getPrevious() is not None) or (x == start):
        while x is not None:
            spt.insert(0, x._getData())
            x = x._getPrevious()

    return spt, end._getDistance()

def BF_shortest_path(g, source):
    """Returns the shortest path between a source and all the other verices of a graph using the Bellman-Ford algorithm.

    Args:
        g (graph): a graph object.
        source (node val data type): the data of the source node.
    Returns:
        (list) the shortest path from the source to all the vertices : elements are [src, dest, distance].
    """
    g.reset()

    edges = g._getEdges()
    ne = len(edges)

    start = g._getVertex(source)
    start._setDistance(0)

    for _ in range(ne):
        for a, b, w in edges:
            alt = a._getDistance() + float(w)
            if alt < b._getDistance():
                b._setDistance(alt)
                b._setPrevious(a)

    for a, b, w in edges:
        alt = a._getDistance() + float(w)
        if alt < b._getDistance():
            print("Error! graph contains a negative-weight cycle.")

    vertices = g._getVerticesDict()
    sp = []
    for vx in vertices.keys():
        sp.append([source, vx._getData(), vx._getDistance()])

    return sp
