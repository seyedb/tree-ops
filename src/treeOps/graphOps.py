#
import graph
import heapq as hq
from collections import deque

def graph_to_adjmat(g):
    '''Given a graph returns the corresponding adjacency matrix.
    
    args:
        g (graph): a graph object
    retruns:
        (2D - nested - list) adjacency matrix: a_ij = 1 if vi and vj are adjacent , 0 otherwise) 
        (2D - nested - list) adjacency matrix: a_ij = weight of the edges between adjacent vertices vi and vj , empty list otherwise)   
    '''
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

def adjmat_to_graph(adjMat, vxdatalist=[]):
    '''Given an adjacency matrix retruns the corresponding (multi)graph.

    args:
        adjMat (2d - nested - list): the adjacency matrix
        vxdatalist (list): list of data to be assigned to the verices of the graph
    returns:
        (graph) a graph that has the same adjacency matrix as the given matrix
    '''
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
            for j in range(i, nvx):
                for w in adjMat[i][j]:
                    g.add_edge(vxdatalist[i], vxdatalist[j], weight=w)
    elif _adjmatType(adjMat) is int:
        for i in range(nvx):
            for j in range(i, nvx):
                if adjMat[i][j] == 1:
                    g.add_edge(vxdatalist[i], vxdatalist[j])
    else:
        print("Warning: The adjacency matrix contains unsupported data type!")

    return g

def _adjmatType(adjMat):
    '''(helper function) retruns <class 'int'> if the adjacency matrix is a (0,1)-matrix, and
    returns <class 'list'> if the adjacency matrix contains edge weights, and returns None if
    neither of the cases occurs.

    args:
        adjMat (2D - nested - list): the adjacency matrix
    returns:
        (type) the type of the adjacency matrix as explained above
    '''
    checktype = {all(isinstance(entry, list) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return list

    checktype = {all(isinstance(entry, int) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return int

    return None    

def dfs_in_adjmat(adjMat, start, visited, path):
    '''Performs DFS in a (0,1) adjacency matrix.

    NOTE : the result is a list of the indices of the vertices. The indices are in accordance with the 
    indexing that has led to the adjacency matrix. 

    args:
        adjMat (2D - nested - list): the adjacency matrix
        start (int): the index of the vertex where the procedure starts
        visited (list of boolean): a list keeping track of the visit status of the vertices
        path (list of int): the DFS path 
    returns:
        (list of int) the full DFS path starting from the given vertex 
    '''
    visited[start] = True

    nvx = len(adjMat)
    for i in range(nvx):
        if adjMat[start][i] == 1 and not visited[i]:
            path.append(i)
            dfs_in_adjmat(adjMat, i, visited, path)

def dfs_in_adjmatw(adjMatw, start, visited, path):
    '''Same as dfs_in_adjmat but works with an adjacency matrix that contains edge weights.'''
    visited[start] = True

    nvx = len(adjMatw)
    for i in range(nvx):
        if adjMatw[start][i] and not visited[i]:
            path.append(i)
            dfs_in_adjmatw(adjMatw, i, visited, path)

def bfs_in_adjmat(adjMat, start, visited):
    '''Performs BFS in a (0,1) adjacency matrix.
    NOTE : the result is a list of the indices of the vertices. The indices are in accordance with the 
    indexing that has led to the adjacency matrix. 

    args:
        adjMat (2D - nested - list): the adjacency matrix
        start (int): the index of the vertex where the procedure starts
        visited (list of boolean): a list keeping track of the visit status of the vertices
    returns:
        (list of int) the full BFS path starting from the given vertex 
    '''
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
    '''Same as bfs_in_adjmat but works with an adjacency matrix that contains edge weights.'''
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
    '''Returns the connected components of a graph (Uses DFS).

    args:
        adjMat (2D - nested - list): the adjacency matrix
    returns:
        (nested list) list of connected components. Every component is a list of indices representing 
        vertices of the graph. The indices agree with the matrix indexing.
    '''
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
    '''Dijkstra's shortest path algorithm.

    args:
        g (graph): a graph object
        source (node val data type): the data of the source node 
        destination (node val data type): the data of the destination node
    retruns:
        (list) the shortest path from the source to the destination : list of the (data of the) vertices on the path
        (float) the length of the shortest path (sum of the weights of the constituent edges) 
    '''
    assert (not g._isMultigraph()), "The Dijkstra's algorithm is not implemented for multigraphs!"

    start = g._getVertex(source)
    end = g._getVertex(dest)

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
