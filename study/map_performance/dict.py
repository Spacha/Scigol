import time
import math
import sys
import numpy as np

# No hashmap of any kind. Iterate list like a stupid.

class Node:
    def __init__(self, x, y):
        self.state = None
        self.x = x
        self.y = y
    def setState(self, state):
        self.state = state

class HashTable:
    def __init__(self, size):
        self.nodes = dict()
    def get_node(self, x, y):
        try:
            node = self.nodes[x,y]
        except KeyError:
            # create new
            node = Node(x,y)
            self.nodes[x,y] = node
            return node

if __name__ == "__main__":
    m = HashTable(50**2) # = 2500

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
    
    print("New nodes - Average: {} us / 100 reads".format(round(np.average(times)*1E6, 3)))

    times = np.empty(MC)
    for mc in range(MC):
        # benchmark: find 100 non-initialized and 100 initialized nodes
        node = None
        startTime = time.time()
        for i in range(100):
            node = m.get_node(i//2, i//2)
        times[mc] = time.time() - startTime

    print("Existing nodes - Average: {} us / 100 reads".format(round(np.average(times)*1E6, 3)))
    print("Final memory use: {} bytes".format(sys.getsizeof(m)))

    print("******************************************************************")

    n = HashTable(1)
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
    print(n.get_node(-100, -120))    
    print("New nodes without initialization - Average: {} us / 100 reads".format(round(np.average(times)*1E6, 3)))
    print("Final memory use: {} bytes".format(sys.getsizeof(n)))

'''
New nodes - Average: 73.791 us / 100 reads
Existing nodes - Average: 35.882 us / 100 reads
Final memory use: 64 bytes
******************************************************************
Initial memory use: 64 bytes
<__main__.Node object at 0x7fa4b229a290>
New nodes without initialization - Average: 79.107 us / 100 reads (cant be initialized!)
Final memory use: 64 bytes
'''