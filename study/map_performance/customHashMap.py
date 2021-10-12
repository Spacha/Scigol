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
Hash map implementation: calculate unique hash based on 2 integers.
According to this, implementation gives unique hash over [-65536, 65535], which is more than enough:
    https://stackoverflow.com/a/26981910/3081830
Table implementation from here:
    https://www.geeksforgeeks.org/hash-map-in-python/
(+) Fast
(+) Well packed -> doesn't waste a lot of space
(+) Very easy to extend
(+) No problem with negative coordinates
(-) ?
'''
class HashTable:
  
    # Create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()
  
    def create_buckets(self):
        return [[] for _ in range(self.size)]
  
    def get_key(self, x, y):
        return (x << 16) + y # limits to: 2^16 = 65536

    def get_item(self, key):
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
  
        found_key = False
        record_val = None
        for index, record in enumerate(bucket):
            record_key, record_val = record
              
            # check if the bucket has same key as 
            # the key being searched
            if record_key == key:
                found_key = True
                break

        if not found_key:
            record_val = None

        return record_val

    def set_item(self, key, val):
        
        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
              
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break
  
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    # Return searched value with specific key
    def get_node(self, x, y):
        node = self.get_item( self.get_key(x,y) )

        if node is not None:
            return node
        else:
            node = Node(x,y)
            self.set_item( self.get_key(x,y), node )
            return node
  
    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

    def __sizeof__(self):
        return sys.getsizeof(self.hash_table) + sys.getsizeof(self.size)


if __name__ == "__main__":
    m = HashTable(50**2) # = 2500
    print("Initial memory use: {} bytes".format(sys.getsizeof(m)))
    # print(m.get_node(4,4))

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

    # HashTable:
    # - New nodes:      ~300 us per 100 new nodes
    # - Existing nodes: ~200 us per 100 existing nodes
    # - Memory usage:   21084 bytes (with initialized length)
    #
    # HashTable (no pre-initialized table):
    # - New nodes:      ~700 us per 100 new nodes       (!)
    # - Existing nodes: no change
    # - Memory usage:   132 bytes                       (!)
