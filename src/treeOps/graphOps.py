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
