import numpy as np
from PyQt5.QtGui import QVector2D

def flatten(l):
    return [y for x in l for y in x]

'''
https://www.geeksforgeeks.org/hash-map-in-python
'''
class HashMap:
    def __init__(self, size):
        self.size = size
        self.table = self.createBuckets()
  
    def createBuckets(self):
        return [[] for _ in range(self.size)]

    def getItem(self, key):
        # Get the index from the key using
        # hash function
        hashedKey = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.table[hashedKey]

        found = False
        recordVal = None
        for index, record in enumerate(bucket):
            recordKey, recordVal = record

            if recordKey == key:
                found = True
                break

        # if no record was found, return 'None'
        if not found:
            recordVal = None

        return recordVal

    def setItem(self, key, val):
        
        # Get the index from the key
        # using hash function
        hashedKey = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.table[hashedKey]
  
        found = False
        for index, record in enumerate(bucket):
            recordKey, recordVal = record
              
            # check if the bucket has same key as
            # the key to be inserted
            if recordKey == key:
                found = True
                break
  
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

def pointKey(x,y):
    ''' https://stackoverflow.com/a/26981910/3081830; limits: 2^16 => [-65536, 65535] '''
    return (x << 16) + y
def lineKey(p1,p2):
    return (pointKey(*p1) << 16) + pointKey(*p2)

class HashMap2D(HashMap):
    def __init__(self, size):
        super().__init__(size)
    def _getKey(self, x, y):
        return pointKey(x,y)
    def getItem(self, x, y):
        return super().getItem( self._getKey(x,y) )
    def setItem(self, x, y, val):
        super().setItem( self._getKey(x,y), val )

class GridElement:
    def __init__(self, x, y):
        pass
    def toVector(self):
        return QVector2D(x,y)

class Node(GridElement):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.state = None
        self.x = x
        self.y = y
    def setState(self, state):
        self.state = state

    def getKey(self):
        return pointKey(self.x, self.y)
    def getHash(self):
        return hash(self.getKey())
    def __eq__(self, other):
        if type(other) == Node:
            return self.getKey() == other.getKey()
        elif type(other) in [tuple, list]:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
    def __str__(self):
        return "<Node ({}, {})={}>".format(self.x, self.y, self.state)

class Segment:
    def __init__(self, p1, p2):
        # order: pointKey(p1) < pointKey(p2)
        if pointKey(*p1) > pointKey(*p2):
            p1,p2 = p2,p1 # swap
        self.p1 = p1
        self.p2 = p2
    def getKey(self): # ~ 1.5 us
        return lineKey(self.p1, self.p2)
    def getHash(self): # ~ 1.6 us
        return hash(self.getKey())
    def getNodes(self):
        return [self.p1, self.p2]
    def getPoints(self, excludeNodes=False): # ~ 12 us
        length = self.length()
        points = [None]*(length + 1 - excludeNodes)
        if length > 0:
            vert = self.isVertical()
            delta = (self.p2[vert] - self.p1[vert]) // length
            a = self.p1[not vert]
            # to exclude the nodes, skip the first and last one
            for i in range(excludeNodes, length + (not excludeNodes)):
                # b: traverse points along axis while the other (a) stays constant
                b = self.p1[vert] + i*delta
                points[i] = [a,b] if vert else [b,a]
        return points[excludeNodes:]

    def includesPoint(self, point): # ~ 0.8 us
        return (self.p1[0] <= point[0] <= self.p2[0] and self.p1[1] <= point[1] <= self.p2[1])
    def includesMidPoint(self, point): # ~ 0.8 us
        if self.isVertical():
            return self.p1[0] == point[0] and (self.p1[1] < point[1] < self.p2[1])
        else:
            return self.p1[1] == point[1] and (self.p1[0] < point[0] < self.p2[0])
    def isVertical(self): # ~ 0.6 us
        return self.p1[0] == self.p2[0]
    def isHorizontal(self): # ~ 0.6 us
        return self.p1[1] == self.p2[1]
    def length(self): # since this is always ver or hor, we can just return difference in coords
        return abs(self.p1[0]-self.p2[0] + self.p1[1]-self.p2[1])

    def __eq__(self, other): # ~ 0.5 us
        ''' Since segments are always in certain order, it is enough to compare one way. '''
        return self.p1 == other.p1 and self.p2 == other.p2
    def __str__(self):
        return "<Segment "+str(self.p1)+"->"+str(self.p2)+">"

class Wire:
    def __init__(self, schema, segmentoids):
        self.schema = schema
        self.segments = []
        for p1, p2 in segmentoids:
            self.segments.append( Segment(p1, p2) )

        self._refresh_cache()

    def _refresh_cache(self):
        ''' Caches nodes and points for faster use. '''
        self.nodes = flatten([s.getNodes() for s in self.segments])
        self.points = flatten([s.getPoints() for s in self.segments])

    def includesMidPoint(self, point):
        # includes if: point is within any segment
        includes = False
        for segment in self.segments:
            if segment.includesMidPoint(point):
                includes = True
                break
        return includes

    def includesPoint(self, point):
        # includes if: point is within any segment
        includes = False
        for segment in self.segments:
            if segment.includesPoint(point):
                includes = True
                break
        return includes

    def segmentAt(self, point):
        ''' Currently recognizes only mid points, since
            nodes may have multiple segments. '''
        for segment in self.segments:
            if segment.includesMidPoint(point):
                return segment
        return None

    def mergeWith(self, other):
        # Merge @other to @self
        while len(other.segments) > 0:
            other_segment = other.segments.pop()

            # 0 or 1 common nodes
            #   -> other's node in self's points -> split(!)
            #   -> otherwise just merge
            # 2 common nodes -> skip (duplicate)
            if other_segment in self.segments:
                continue
            else:
                # Ok, not a duplicate. Now we are interested if one or two of the other's
                # nodes are self's points -> would need to split segments.

                # other's node is on self's point -> need to split
                splitPoints = []
                if self.includesMidPoint(other_segment.p1):
                    splitPoints.append(other_segment.p1)
                if self.includesMidPoint(other_segment.p2):
                    splitPoints.append(other_segment.p2)

                #print(other_segment.p1, other_segment.p2)
                #print([str(s) for s in self.segments])

                # need to split...
                if len(splitPoints) > 0:
                    for splitPoint in splitPoints: # just 1 or 2 loops
                        segment = self.segmentAt(splitPoint)
                        #print("Segment to split: " + str(segment))
                        if segment is not None:
                            self.splitSegment(segment, splitPoint)
                        else:
                            print("Splitpoint: " + str(splitPoint))

                # let's just merge the other segment to this...
                else:
                    self.segments.append(other_segment)

        self._refresh_cache()
        return self

    # TODO: need to improve for non-triial cases:
    # 1) parallel overlap (2 point overlap) -> produces 3 segments
    # 2) perpendicular (one point overlap) -> produces 3 segments
    def splitSegment(self, segment, point):
        newSegments = (
            Segment( segment.p1, point ),
            Segment( point, segment.p2 )
        )
        # remove the original segment
        del self.segments[self.segments.index(segment)]
        self.segments += newSegments
        #print("Splitted segment to: "+str(newSegments[0])+" and "+str(newSegments[1]))
    
    def __add__(self, other):
        return self.mergeWith(other)
    def __str__(self):
        segments = "".join(map(lambda s: "\t"+str(s)+"\n", self.segments))
        return "<Wire ["+str(segments)+"]>"


class Config:
    initialNodes = 1024
    initialSegments = 512
    #initialWires = 512
    initialPorts = 128
class Schema:
    def __init__(self):
        self.nodes = HashMap2D(Config.initialNodes)
        self.segments = HashMap2D(Config.initialSegments)
        self.wires = []
        self.ports = []

    def addWire(self, segmentoids):
        #wire = self.wireAt(segmentoids) or Wire()
        wire = Wire(self, segmentoids)

        # collision: a NODE of the new wire equals
        # to any POINT of an existing wire
        # i.e. a NODE of the new wire is ON a SEGMENT of an existing wire
        collidesWith = []
        for existingWire in self.wires:
            for node in wire.nodes:
                if existingWire.includesPoint(node):
                    collidesWith.append(existingWire)
                    break # next wire

        if len(collidesWith) > 0:
            # TODO: find the smallest wire and merge it to larger ones in order
            # finally merge all to the largest one
            while True:
                w = collidesWith.pop()
                wire = w.mergeWith(wire) # build up a 'combined wire'
                
                # if there are still wires to merge,
                # delete this one from the schema
                if len(collidesWith) > 0:
                    del self.wires[self.wires.index(w)]
                else:
                    break
        else:
            # no collisions -> just add a new wire
            self.wires.append(wire)


    def addPort(self, port, pos):
        port.position = pos
        self.ports.setItem(port)

    def wireAt(self, segmentoids):
        wire = None
        for p1, p2 in segmentoids:
            if wire.includesPoint(p1) or wire.includesPoint(p2):
                return wire
        return None

    def nodeAt(self, x, y):
        node = self.nodes.getItem(x,y)
        
        # not found yet -> create one
        if node is None:
            node = Node(x,y)
            self.nodes.setItem(x,y,node)

        return node

    def segmentAt(self, p1, p2):
        segment = self.segments.getItem(p1, p2)
        
        # not found yet -> create one
        if node is None:
            node = Node(x,y)
            self.nodes.setItem(x,y,node)

        return node


# usage
schema = Schema()
schema.addWire([
    ((0,0), (0,2))
])
'''
for w in schema.wires:
    print(w)
'''
schema.addWire([
    ((0,1), (-1,1))
])

for w in schema.wires:
    print(w)
'''
w1 = Wire(schema, [((0,0), (0,2)), ((0,2), (2,2))])
print(w1)

w2 = Wire(schema, [((0,0), (0,1))])
w1.mergeWith(w2)

print(w1)
'''

#ib = schema.library()
#lib.intialize("default.json") # initialize the port library?

#and1 = AndPort(2)
#schema.placePort(and1, (5,5))
#schema.simulate()

###############################################################################
# BENCHMARKS
###############################################################################

import time, random
class Benchmark:
    def __init__(self, N=100000):
        self.N = N

        self.segmentoids = []
        for i in range(100):
            a = random.randint(0,100)-50
            b = random.randint(0,100)-50
            c = random.randint(0,100)-50
            # must be either vertical or horiontal
            p1,p2 = ((a,b),(a,c)) if random.randint(0,1) == 0 else ((b,a),(c,a))
            self.segmentoids.append( (p1,p2) )

        self.segments = []
        for i in range(100):
            a = random.randint(0,100)-50
            b = random.randint(0,100)-50
            c = random.randint(0,100)-50
            # must be either vertical or horiontal
            p1,p2 = ((a,b),(a,c)) if random.randint(0,1) == 0 else ((b,a),(c,a))
            self.segments.append( Segment(p1,p2) )

    def benchmark_nodeAt(self):
        s = time.time()
        for i in range(self.N):
            n = schema.nodeAt(random.randint(0,100)-50, random.randint(0,100)-50)
        print(n)
        print((time.time()-s)*1E6/self.N) # 135 ms = 13.5 us per node

    def bm_segment_comparison(self):
        times = []
        for i in range(self.N):
            s1 = self.segments[random.randint(0,99)]
            s2 = self.segments[random.randint(0,99)]
            s = time.time()
            same = s1 == s2
            times.append(time.time()-s)
        print("Segment comparison: ", end='')
        print(sum(times)*1E6/self.N) # ~1 us per segment comparison

    def bm_segment_getKey(self):
        times = []
        for i in range(self.N):
            s1 = self.segments[random.randint(0,99)]
            s = time.time()
            s1.getKey()
            times.append(time.time()-s)
        print("Segment getKey(): ", end='')
        print(sum(times)*1E6/self.N) # ~1 us per segment comparison

    def bm_segment_getHash(self):
        times = []
        for i in range(self.N):
            s1 = self.segments[random.randint(0,99)]
            s = time.time()
            s1.getHash()
            times.append(time.time()-s)
        print("Segment getHash(): ", end='')
        print(sum(times)*1E6/self.N) # ~1 us per segment comparison

    def bm_getPoints(self):
        times = []
        for i in range(self.N):
            s1 = self.segments[random.randint(0,99)]
            excludeNodes = random.randint(0,1)
            s = time.time()
            s1.getPoints(excludeNodes)
            times.append(time.time()-s)

        print(sum(times)*1E6/self.N)

    def bm_addWire(self):
        times = []
        schema = Schema()
        for i in range(self.N):
            sx = [self.segmentoids[random.randint(0,99)] for _ in range(3)]
            s = time.time()
            schema.addWire(sx)
            times.append(time.time()-s)

        print(sum(times)*1E6/self.N)

bm = Benchmark()
# bm.bm_getPoints()
# bm.bm_addWire()
#s = Segment((0,1),(0,5))
#print(s.getPoints())
#s = Segment((-4,3),(2,3))
#print(s.getPoints())

###############################################################################
# TESTS
###############################################################################

import pytest
@pytest.mark.parametrize("segmentoid,excludeNodes,expected", [
    ( (( 0,1),(0,5)), False, [[0,1],[0,2],[0,3],[0,4],[0,5]] ),
    ( ((-4,3),(2,3)), False, [[-4,3],[-3,3],[-2,3],[-1,3],[0,3],[1,3],[2,3]] ),
    ( ((-4,3),(2,3)), True,  [[-3,3],[-2,3],[-1,3],[0,3],[1,3]] ),
    ( (( 0,0),(1,0)), False, [[0,0],[1,0]] ),
    ( (( 0,0),(1,0)), True,  [] ),
])
def test_getPoints(segmentoid, excludeNodes, expected):
    segment = Segment(*segmentoid)
    assert( segment.getPoints(excludeNodes) == expected )

@pytest.mark.parametrize("segmentoid,point,expected", [
    ( ((0,0), (0,5)), (0,2), True ),
    ( ((3,1), (-2,1)), (1,1), True ),
    ( ((3,1), (-2,1)), (-1,1), True ),
    ( ((3,1), (-2,1)), (-1,0), False ),
    ( ((-2,2), (2,2)), (2,0), False )
])
def test_includesMidPoint(segmentoid, point, expected):
    segment = Segment(*segmentoid)
    assert( segment.includesMidPoint(point) == expected )
