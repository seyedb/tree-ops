#
import graph

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

    # check the kind of the adjacency matrix, 0 and 1 type or a matrix that contains edge weights
    islist, isint = False, False
    checktype = {all(isinstance(entry, list) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: islist = True
    checktype = {all(isinstance(entry, int) for entry in row) for row in adjMat}
    if len(checktype) == 1 and checktype.pop() == True: isint = True

    if islist:
        for i in range(nvx):
            for j in range(i, nvx):
                for w in adjMat[i][j]:
                    g.add_edge(vxdatalist[i], vxdatalist[j], weight=w)
    elif isint:
        for i in range(nvx):
            for j in range(i, nvx):
                if adjMat[i][j] != 0:
                    g.add_edge(vxdatalist[i], vxdatalist[j])
    else:
        print("Warning: The adjacency matrix contains unsupported data type!")

    return g
