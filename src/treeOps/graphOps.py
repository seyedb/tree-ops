#
import graph
from collections import deque

def graph_to_adjmat(g):
    '''
    Given a graph returns the corresponding adjacency matrix
    
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
        vxdata.append(vx.data)

    adjMat = [[0 for i in range(nvx)] for j in range(nvx)]
    adjMatw = [[[] for i in range(nvx)] for j in range(nvx)]

    for vx, vxchildren in vertices.items():
        for child, weight in vxchildren.items():
            r = vxdata.index(vx.data)
            c = vxdata.index(child.data)
            adjMat[r][c] = 1
            adjMatw[r][c] = weight
    
    return adjMat, adjMatw

def adjmat_to_graph(adjMat, vxdatalist=[]):
    '''
    Given an adjacency matrix retruns the corresponding (multi)graph

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
    '''
    (helper function) retruns <class 'int'> if the adjacency matrix is a (0,1)-matrix, and
    returns <class 'list'> if the adjacency matrix contains edge weights, and returns None if
    neither of the cases occurs.

    args:
        adjMat (2D - nested - list): tha adjacency matrix
    returns:
        (type) the type of the adjacency matrix as explained above
    '''
    checktype = {all(isinstance(entry, list) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return list

    checktype = {all(isinstance(entry, int) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: return int

    return None    

def dfs_in_adjmat(adjMat, start, visited, path):
    '''
    Performs DFS in a (0,1) adjacency matrix 
    NOTE : the result is a list of the indices of the vertices. The indices are in accordance with the 
    indexing that has led to the adjacency matrix. 

    args:
        adjMat (2D - nested - list): tha adjacency matrix
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
    '''
    Same as dfs_in_adjmat but works with an adjacency matrix that contains edge weights
    '''
    visited[start] = True

    nvx = len(adjMatw)
    for i in range(nvx):
        if adjMatw[start][i] and not visited[i]:
            path.append(i)
            dfs_in_adjmatw(adjMatw, i, visited, path)

def bfs_in_adjmat(adjMat, start, visited):
    '''
    Performs BFS in a (0,1) adjacency matrix 
    NOTE : the result is a list of the indices of the vertices. The indices are in accordance with the 
    indexing that has led to the adjacency matrix. 

    args:
        adjMat (2D - nested - list): tha adjacency matrix
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
    '''
    Same as bfs_in_adjmat but works with an adjacency matrix that contains edge weights
    '''
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

