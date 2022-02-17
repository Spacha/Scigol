import numpy as np
import time
import math
import sys

class Node:
    def __init__(self, x, y):
        self.state = None
        self.x = x
        self.y = y
    def setState(self, state):
        self.state = state

'''
Numpy implementation: 2-D array with keying: (x,y)
(+) Simple
(+) Fast?
(-) Wastes a lot of space! Very fragmented memory.
(-) Expensive to extend?
(-) What about negative coordinates??
'''
class NumpyMap:
    def __init__(self, size):
        self.sizeX = math.ceil(math.sqrt(size))
        self.sizeY = math.ceil(math.sqrt(size))
        # print("({},{} => {})".format(self.sizeX, self.sizeY, self.sizeX*self.sizeY))
        self.store = np.empty((self.sizeX, self.sizeY), dtype=Node)

    def get_node(self, x, y):
        try:
            '''
            if x >= self.sizeX or y >= self.sizeY:
                # extend the map (most likely very expensive)
                pass
            '''
            node = self.store[x][y]
        except:
            return # extend the map...

        if node is None:
            self.store[x][y] = Node(x,y)
            return self.store[x][y]
        else:
            return node

    def __sizeof__(self):
        return sys.getsizeof(self.store) + sys.getsizeof(self.sizeX) + sys.getsizeof(self.sizeY)


if __name__ == "__main__":
    m = NumpyMap(50**2) # = 2500
    print("Initial memory use: {} bytes".format(sys.getsizeof(m)))
    #print(m.get_node(4,4))

    # 10 Monte-Carlo loops
    MC = 10
    times = np.empty(MC)
    for mc in range(MC):
        # benchmark: find 100 non-initialized and 100 initialized nodes
        node = None
        startTime = time.time()
        for i in range(100):
            node = m.get_node(i//2, i//2)
            node = m.get_node(i//2, i//2)
        times[mc] = time.time() - startTime
    
    print("New nodes - Average: {} ms/100 reads".format(np.average(times)*1000))

    times = np.empty(MC)
    for mc in range(MC):
        # benchmark: find 100 non-initialized and 100 initialized nodes
        node = None
        startTime = time.time()
        for i in range(100):
            node = m.get_node(i//2, i//2)
        times[mc] = time.time() - startTime
    
    print("Existing nodes - Average: {} ms/100 reads".format(np.average(times)*1000))
    print("Final memory use: {} bytes".format(sys.getsizeof(m)))

    print("******************************************************************")

    n = NumpyMap(1)
    print("Initial memory use: {} bytes".format(sys.getsizeof(n)))

    # 10 Monte-Carlo loops
    MC = 10
    times = np.empty(MC)
    for mc in range(MC):
        # benchmark: find 100 non-initialized and 100 initialized nodes
        node = None
        startTime = time.time()
        for i in range(100):
            node = n.get_node(i//2, i//2)
            node = n.get_node(i//2, i//2)
        times[mc] = time.time() - startTime
    
    print("New nodes without initialization - Average: {} ms/100 reads".format(np.average(times)*1000))
    print("Final memory use: {} bytes".format(sys.getsizeof(n)))

    # NumpyMap:
    # - New nodes:      ~200 us per 100 new nodes
    # - Existing nodes: ~100 us per 100 existing nodes
    # - Memory usage:   20184 bytes
    #
    # NumpyMap (no pre-initialized table):
    # - New nodes:      ~700 us per 100 new nodes (!)
    # - Existing nodes: no change
    # - Memory usage:   132 bytes (!)
