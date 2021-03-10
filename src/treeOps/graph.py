from enum import Enum
from collections import deque

class node_status(Enum):
    '''
    List of all possible visit status of each node (graph traversal)
    '''
    UNVISITED = 0
    VISITED = 1
    VISITING = 2

class graph(object):
    def __init__(self):
        self.vertices = {}

    class graphNode(object):
        def __init__(self, data, status=node_status.UNVISITED):
            self.data = data
            self.children = {}
            self.status = status
