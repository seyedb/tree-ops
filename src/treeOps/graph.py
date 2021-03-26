from enum import Enum
from collections import deque, defaultdict
from functools import partial

class node_status(Enum):
    """List of possible visit status of graph nodes (graph traversal)."""
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class graph(object):
    def __init__(self):
        """Initializes a graph with a nested defaultdict of graphNodes.
        example: {'A': {'B': [2, 3], 'C': [5, 1]}}
        """
        self.vertices = defaultdict(partial(defaultdict, list))

    class graphNode(object):
        def __init__(self, data, status=node_status.UNVISITED):
            """Initializes a graph node.
            Attributes:
                data (any type): the node value.
                children (dict): a dictionary of the children (adjacent nodes).
                status (node_status): the visit status of the node (graph traversal).
                distance (float): the distance from a source node to this node.
                previous (graphNode): predecessor of this node in an optimal path from 
                a predefined source in a shortest path algorithm.
            """
            self.data = data
            self.children = defaultdict(list)
            self.status = status
            self.distance = float('inf')
            self.previous = None

        # comparison operators
        def __lt__(self, other):
            return self.data < other.data

        def __le__(self, other):
            return self.data < other.data or self.data == other.data

        # the following are optional
#        def __ne__(self, other):
#            return self.data != other.data
#
#        def __gt__(self, other):
#            return self.data > other.data
#
#        def __ge__(self, other):
#            return self.data > other.data or self.data == other.data

        def __str__(self):
            """Prints the data assigned to this node, and list of its children with the weight of the 
            edges connecting them.
            """
            res = "'{}': {}".format(self._getData(), 
                            [[node._getData(), self._getWeight(node)] for node in self._getChildren()])
            return res

        def _getStatus(self):
            """Returns the current visit status of a node."""
            return self.status

        def _setStatus(self, status):
            """Sets the visit status of a node.

            Args:
                status (node_status): the new visit status.
            Returns:
                (graphNode) the node with its status updated with the given status.
            """
            self.status = status

        def _getData(self):
            """Returns the data assigned to this node."""
            return self.data
       
        def _setData(self, data):
            """Sets the data of this node to a given value.

            Args:
                data (node val data type): the new data to be assigned to this node.
            Returns:
                (graphNode) the node with updated data.
            """ 
            self.data = data

        def _addAdjNode(self, node, weight=0):
            """Adds an adjacent node to this node.

            Args:
                node (graphNode): the new adjacent node.
                weight (int): the weight of the edge connecting this node to the new node.
            Returns:
                (graphNode) this node with its dictionary of children updated with a new node added.
            """
            self.children[node].append(weight) if weight not in self.children[node] \
                                               else self.children[node]

        def _getChildren(self):
            """Returns the keys of the dict of children of this node.

            Returns:
                (dict_keys) keys of the dictionary of children of this node.
            """
            return self.children.keys()

        def _getDistance(self):
            """Returns the value of the distance instance attribute of this node."""
            return self.distance

        def _setDistance(self, distance):
            """Sets the instance attribute distance to a given value.

            Args:
                distance (float): the new distance.
            Returns:
                (graphNode) the node with its distance updated with the given value.
            """
            self.distance = distance

        def _getPrevious(self):
            """Returns the value of the previous instance attribute of this node."""
            return self.previous

        def _setPrevious(self, node):
            """Sets the instance attribute previous to a given node.

            Args:
                node (graphNode): the new previous.
            Returns:
                (graphNode) this node with its previous updated with the given node.
            """
            self.previous = node

        def _getWeight(self, adjNode):
            """Returns the weight of the edge between this node and the given node if they are adjacent,
            otherwise returns None.
            """
            if adjNode in self.children:
                return self.children[adjNode]
            else:
                return None

        def _isAdjacent(self, node):
            """Returns True of this node is adjacent to the give node, else False.

            Returns:
                (boolean) whether or not this node and the given node are adjacent.
            """
            return node in self.children

    def __str__(self):
        """Returns a string representing the vertices and edges of this graph."""
        res = ''
        for vertex in self._getVerticesDict():
            res += vertex.__str__() + '\n'

        return res

    def reset(self):
        """Resets the attributes of all the nodes in a graph to their default values."""
        for vx in self._getVerticesDict():
            vx._setStatus(node_status.UNVISITED)
            vx._setDistance(float('inf'))
            vx._setPrevious(None)

    def __contains__(self, VxData):
        """Checks whether or not the graph contains a given data.

        Args:
            VxData (node val data type): the data to be searched for.
        Returns:
            (boolean) True if VxData is found, otherwise False.
        """
        data = [k._getData() for k in self._getVerticesDict().keys()]
        return VxData in data

    def _getVerticesDict(self):
        """(helper function) Returns a nested (default) dictionary of the vertices of the graph.

        Returns:
            (defaultdict) the default dictionary of vertices of the graph.
        """
        return self.vertices

    def _getEdges(self):
        """Returns a set of edges of the graph. 
        NOTE:
            - If there is an edge between v1, v2 with weight w, both (v1, v2, w) and (v2, v1, w) are
            included. This is necessary for Bellman-Ford shortest path algorithm and also make it general
            for directed graphs.
        
        Returns:
            (set of tuples): set of edges represented as (v1, v2, w).
        """
        vertices = self._getVerticesDict()

        edges = set()
        for vx, vxchildren in vertices.items():
            for child, weight in vxchildren.items():
                # uncomment the following line to have only unique edges
#                tmp = sorted([vx, child])
                tmp = [vx, child]
                for i in range(len(weight)):
                    edges.add((tmp[0], tmp[1], weight[i]))

        return edges

    def _getVertex(self, VxData):
        """(helper function) Returns a graph node that holds the given data.

        Args:
            VxData (node val data type): the data to be searched for.
        Returns:
            (graphNode) the graph node from this graph that has data equal to the given data.
        """
        if VxData not in self:
            print("Vertex {} doesn't exist.".format(VxData))
            return None

        for vertex in self._getVerticesDict():
            if vertex._getData() == VxData:
                return vertex

    def add_vertex(self, VxData):
        """Adds a vertex to the graph.

        Args:
            VxData (node val data type): the data to be added to the graph.
        Returns:
            (graph) this graph with a new node added to it as a new vertex.
        """
        vx = self.graphNode(VxData)

        if VxData in self._getVerticesDict():
            print("Vertex {} already exists.".format(VxData))
        else:
            self.vertices[vx] = defaultdict(list)

    def add_edge(self, fromVxData, toVxData, weight=0.0, directed=False):
        """Adds an edge to the graph given the data stored in the nodes at its ends.

        Args:
            fromVxData (node val data type): data of the "from" node.
            toVxData (node val data type): data of the "to" node.
            weight (float): weight of the edge.
            directed (boolean): whether or not the edge is directed from fromVxData to toVxData.
        Returns:
            (graph) this graph updated with a new edge added to it.
        """
        if fromVxData not in self:
            print("Adding edge failed! Vertex {} doesn't exist.".format(fromVxData))
            return

        if toVxData not in self:
            print("Adding edge failed! Vertex {} doesn't exist.".format(toVxData))
            return

        a = self._getVertex(fromVxData)
        b = self._getVertex(toVxData)

        edges = self._getEdges()
        msg = "The edge ({}, {}, {}) already exists!"
        msgcmpl = msg + " ({}, {}, {}) will be created."

        if directed:
            if (a, b, weight) in edges:
                print(msg.format(fromVxData, toVxData, weight))
                return

            a._addAdjNode(b, weight)
            self.vertices[a][b].append(weight)

        elif not directed:
            if (a, b, weight) in edges and (b, a, weight) not in edges:
                print(msgcmpl.format(fromVxData, toVxData, weight, toVxData, fromVxData, weight))
                b._addAdjNode(a, weight)
                self.vertices[b][a].append(weight)
                return

            elif (b, a, weight) in edges and (a, b, weight) not in edges:
                print(msgcmpl.format(toVxData, fromVxData, weight, fromVxData, toVxData, weight))
                a._addAdjNode(b, weight)
                self.vertices[a][b].append(weight)
                return

            elif (a, b, weight) in edges and (b, a, weight) in edges:
                return

            a._addAdjNode(b, weight)
            b._addAdjNode(a, weight)
            self.vertices[a][b].append(weight)
            self.vertices[b][a].append(weight)

    def _isMultigraph(self):
        """(helper function) Checks whether or not the graph is a multigraph."""
        vertices = self._getVerticesDict()

        for vx, vxchildren in vertices.items():
            for weight in vxchildren.values():
                if len(weight) > 1:
                    return True

        return False

    def DFS(self, start, path=None):
        """Depth-First Search (DFS).

        Args:
            start (node val data type): the key value of the node where the search starts.
            path (list of graphNode): the DFS path (empty path to be filled with nodes).
        Returns:
            (list of graphNode) the full DFS path.
        """
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
                path = self.DFS(child._getData(), path)

        return path

    def BFS(self, start):
        """Breadth-First Search (BFS).

        Args:
            start (node val data type): the key value of the node where the search starts.
        Returns:
            (list of graphNode) the full BFS path.
        """
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
