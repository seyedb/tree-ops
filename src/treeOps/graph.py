from enum import Enum
from collections import deque, defaultdict
from functools import partial

class node_status(Enum):
    '''
    List of possible visit status of graph nodes (graph traversal)
    '''
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class graph(object):
    def __init__(self):
        '''
        Initializes a graph with a nested defaultdict of graphNodes.
        example: {'A': {'B': [2, 3], 'C': [5, 1]}}
        '''
        self.vertices = defaultdict(partial(defaultdict, list))

    class graphNode(object):
        def __init__(self, data, status=node_status.UNVISITED):
            '''
            Initializes a graph node. A graph node has the following attributes:
            data (any type), children ({adj node: [weight]}, ex: {'B': [2, 3], 'C': [5, 1]}), 
            status (node_status)  
            '''
            self.data = data
            self.children = defaultdict(list)
            self.status = status

        def __str__(self):
            '''
            Prints the data assigned to this node, and list of its children with the weight of the 
            edges connecting them.
            '''
            res = "'{}': {}".format(self.data, 
                            [[node.data, self._getWeight(node)] for node in self._getChildren()])
            return res

        def _getStatus(self):
            '''
            Returns the current visit status of a node.
            '''
            return self.status

        def _setStatus(self, status):
            '''
            Sets the visit status of a node.

            args:
                status (node_status): the new visit status
            returns:
                (graphNode) the node with its status updated with the given status
            '''
            self.status = status

        def _addAdjNode(self, node, weight=0):
            '''
            Adds an adjacent node to this node.

            args:
                node (graphNode): the new adjacent node
                weight (int): the weight of the edge connecting this node to the new node
            returns:
                (graphNode) this node with its dictionary of children updated with a new node added
            '''
            self.children[node].append(weight) if weight not in self.children[node] \
                                               else self.children[node]

        def _getChildren(self):
            '''
            Returns the keys of the dict of children of this node.

            returns:
                (dict_keys) keys of the dictionary of children of this node
            '''
            return self.children.keys()

        def _getWeight(self, adjNode):
            '''
            Returns the weight of the edge between this node and the given node if they are adjacent,
            otherwise returns None.
            '''
            if adjNode in self.children:
                return self.children[adjNode]
            else:
                return None

        def _isAdjacent(self, node):
            '''
            Returns True of this node is adjacent to the give node, else False.

            returns:
                (boolean) whether or not this node and the given node are adjacent
            '''
            return node in self.children

    def __str__(self):
        '''
        Prints the vertices and edges of this graph
        ''' 
        res = ""
        for vertex in self._getVerticesDict():
            res += vertex.__str__() + "\n"

        return res

    def __contains__(self, VxData):
        '''
        Checks whether or not the graph contains a given data

        args:
            VxData (node val data type): the data to be searched for
        returns:
            (boolean) True if VxData is found, otherwise False
        '''
        data = [k.data for k in self._getVerticesDict().keys()]
        return VxData in data

    def _getVerticesDict(self):
        '''
        (helper function) Returns a nested (default) dictionary of the vertices of the graph.

        returns:
            (defaultdict) the default dictionary of vertices of the graph
        '''
        return self.vertices

    def _getVertex(self, VxData):
        '''
        (helper function) Returns a graph node that holds the given data 

        args:
            VxData (node val data type): the data to be searched for
        returns:
            (graphNode) the graph node from this graph that has data equal to the given data
        '''
        if not self.__contains__(VxData):
            print("Vertex {} doesn't exist.".format(fromVxData))
            return None

        for vertex in self._getVerticesDict():
            if vertex.data == VxData:
                return vertex

    def add_vertex(self, VxData):
        '''
        Adds a vertex to the graph.

        args:
            VxData (node val data type): the data to be added to the graph
        returns:
            (graph) this graph with a new node added to it as a new vertex
        '''
        vx = self.graphNode(VxData)

        if VxData in self._getVerticesDict():
            print("Vertex {} already exists.".format(VxData))
        else:
            self.vertices[vx] = defaultdict(list)

    def add_edge(self, fromVxData, toVxData, weight=0):
        '''
        Adds an edge to the graph given the data stored in the nodes at its ends

        args:
            fromVxData (node val data type): data of the "from" node
            toVxData (node val data type): data of the "to" node
            weight (int): weight of the edge
        returns:
            (graph) this graph updated with a new edge added to it 
        '''
        if not self.__contains__(fromVxData):
            print("Adding edge failed! Vertex {} doesn't exist.".format(fromVxData))
            return

        if not self.__contains__(toVxData):
            print("Adding edge failed! Vertex {} doesn't exist.".format(toVxData))
            return

        a = self._getVertex(fromVxData)
        b = self._getVertex(toVxData)

        a._addAdjNode(b, weight)
        b._addAdjNode(a, weight)

        self.vertices[a][b].append(weight)
        self.vertices[b][a].append(weight)

    def DFS(self, start, path=None):
        '''
        Depth-First Search (DFS)
        args:
            start (node val data type): the key value of the node where the search starts
            path (list of graphNode): the DFS path (empty path to be filled with nodes)
        returns:
            (list of graphNode) the full DFS path
        '''
        if path is None:
            path = []

        s = self._getVertex(start)
        if s is None:
            return

        if len(path) == 0: path.append(s)

        s._setStatus(node_status.VISITED)

        for child in s._getChildren():
            if child._getStatus() == node_status.UNVISITED:
                path.append(child)
                path = self.DFS(child.data, path)

        return path

    def BFS(self, start):
        '''
        Breadth-First Search (BFS)
        args:
            start (node val data type): the key value of the node where the search starts
        returns:
            (list of graphNode) the full BFS path
        '''
        s = self._getVertex(start)
        if s is None:
            return
        s._setStatus(node_status.VISITED)
        path = []

        Q = deque()
        Q.append(s)
        while Q:
            k = Q.popleft()

            for child in k._getChildren():
                if child._getStatus() == node_status.UNVISITED:
                    child._setStatus(node_status.VISITED)
                    Q.append(child)

            k._setStatus(node_status.VISITED)
            path.append(k)

        return path

    def reset_status(self):
        '''
        Resets the visit status of all the nodes in a graph to UNVISITED
        '''
        for vx in self._getVerticesDict():
            vx._setStatus(node_status.UNVISITED)
