from PyQt5.QtGui import QVector2D
import math, time

def rotate(self, deg, cx=0, cy=0):
    ''' Rotates @deg degrees _clockwise_ about point (@cx, @cy). '''
    a = math.radians(deg)
    x = self.x()
    y = self.y()
    self.setX(round( (x-cx)*math.cos(-a) - (y-cy)*math.sin(-a) + cx, 10 ))
    self.setY(round( (x-cx)*math.sin(-a) + (y-cy)*math.cos(-a) + cy, 10 ))

def toTuple(self):
    ''' Return the vector as a tuple. '''
    return (self.x(), self.y())

# extend QVector2D
QVector2D.rotate = rotate
QVector2D.toTuple = toTuple
############################

class Node(QVector2D):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = None
        self.setX(x)
        self.setY(y)

class Input(Node):
    def __init__(self, port, x, y):
        super().__init__(x,y)
        self.port = port

class Output(Node):
    def __init__(self, port, x, y):
        super().__init__(x,y)
        self.port = port

class Segment:
    def __init__(self, start, end):
        if not (type(start) == Node and type(end) == Node):
            raise ValueError("Start and end must be a type of Nodes!")
        elif not (start.x() == end.x() or start.y() == end.y()):
            raise ValueError("Segment must be strictly horizontal or vertical!")

        self.start = start
        self.end = end

    def __eq__(self, other):
        ''' Overload equality operator. '''
        return (self.start,self.end) in [(other.start,other.end),(other.end,other.start)]

    def isVertical(self):
        return self.start.x() == self.end.x()
    def isHorizontal(self):
        return self.start.y() == self.end.y()
    def length(self): # since this is always ver or hor, we can just return difference in coords
        return abs(self.start.x()-self.end.x() + self.start.y()-self.end.y())

    def getPoints(self, exclude_nodes=False):
        # delta vector, the vector between each points in this segment
        delta = QVector2D(self.end-self.start).normalized()
        points = []

        nums = range(int(self.length()) + 1)
        if exclude_nodes:
            nums = nums[1:-1] # drop first and last (= nodes)
        for i in range(int(self.length()) + 1):
            points.append(self.start + i*delta)
        return []

''' Collection of segments. '''
class Wire:
    '''
    nodes = [Node(2,0), Node(4,1), Node(2,1)]
    # 1) all nodes must be in at least one segment
    # 2) at least one node of a segment must appear in another segment
    # 3) nodes in segment must be codirectional (i.e. crossProduct(A,B) == 0 or A[0]==B[0] and A[1]==B[1])
    segments = [(nodes[0], nodes[2]), (nodes[2], nodes[1])]
    segments = [
        Segment(nodes[0], nodes[2]),
        Segment(nodes[2], nodes[1]),
        # Segment(nodes[2], Node(3,2))
    ]
    Wire(segments)
    '''
    def __init__(self, segments):
        self.segments = segments

    def getPoints(self, exclude_nodes=False):
        ''' Point refers to any grid point that the wire crosses, not only nodes. '''
        points = []
        for segment in self.segments:
            for point in segment.getPoints(exclude_nodes):
                if point not in points: # only add distinct points
                    points.append(point)
        return points

    def getNodes(self):
        ''' Get the nodes (points of connection) of the wire. '''
        nodes = []
        for segment in self.segments:
            if segment.start not in nodes: # only add distinct nodes
                nodes.append(segment.start)
            if segment.end not in nodes:
                nodes.append(segment.end)
        return (nodes)


class PortType:
    NONE = 0
    SOURCE = 1
    PRIMITIVE = 2 # AND, OR, NOT, XOR, ... = MISO
    # MISO = 2 # multiple-input-single-output
    CUSTOM = 3

class Port:
    port_type = PortType.NONE
    label = ''
    inputs = []
    output = None
    
    # only for MISO ports at the moment
    def __init__(self, port_type, inputs, label=''):
        self.port_type = port_type
        inputsCoords, outputCoord, centerPoint = self.nodeConfig(inputs or 1) # 1, if inputs == 0
        self.inputs = []
        self.output = Output(self, *outputCoord.toTuple())
        self.label = label

        for i in range(0,inputs):
            self.inputs.append(Input(self, *inputsCoords[i].toTuple()))

    def inputStates(self):
        states = []
        for i in self.inputs:
            states.append(i.state)
        return states
    def inputState(self, input=0):
        return self.inputs[input]

    def nodeConfig(self, N):
        '''
        NOTE: This is a static function -> we could just pre-calculate these values for N = 0, ..., N = 32 or so.
        This calculates the node coordinates for a basic MISO (multiple-input-single-output) port.
        The coordinates are returned with respect to the center point of the port.
        Example (Ix = input z, Ox = output x, C = center):
            N = 1           N = 2           N = 3           N = 4
        (I0)(  )(O0)    (I0)(  )(  )    (I0)(  )(  )    (I0)(  )(  )
                        (  )(C )(O0)    (I1)(  )(O0)    (I1)(  )(  )
                        (I1)(  )(  )    (I2)(C )(  )    (  )(C )(O0)
                                                        (I2)(  )(  )
                                                        (I3)(  )(  )
        Returns:
            (inputsCoords, outputCoord, centerCoord)
        '''
        centerPoint = QVector2D(1, N//2)
        outputNode = QVector2D(1,0) + centerPoint
        portHeight = int(2*outputNode.y() + 1)
        inputNodes = []
        for i in range(0,portHeight):
            if i == N/2: # skip the 'middle point' for even numbers of input
                continue
            inputNodes.append( QVector2D(0,i)-centerPoint )
        return (inputNodes, outputNode-centerPoint, centerPoint)

    def draw(self, p):
        pass


class AndPort(Port):
    def __init__(self, inputs=2, label=''):
        super().__init__(PortType.PRIMITIVE, inputs, label)
    def simulate(self):
        self.output = int(all(self.inputStates()))

class SourcePort(Port):
    def __init__(self, label = ''):
        super().__init__(PortType.SOURCE, 0, label)
        self.internalState = 0
    def simulate(self):
        self.output = self.internalState
    def set(self, state):
        self.internalState = state
    def toggle(self):
        self.internalState = int(not self.internalState)




class Schema:
    '''
    NODES:
      Nodes are managed by Schema. Their existence outside Schema is questionable.
      1) There can exist one node per grid point
        * More nodes are created on the fly as they are needed
    '''
    nodes = []
    segments = []
    ports = []
    '''
    WIRES:
      1) two wires cannot share a node
        - if so, they are merged to one
      2) wire cannot run over another wire's node (but CAN over another wire segment)
        - if so, they are merged to one
    '''
    wires = []

    def __init__(self):
        self.ports = []
        self.wires = []

    def addPort(self, port):
        self.ports.append(port)

    def addWire(self, segmentoids):
        # convert the segmentoids (list of tuples) to a list of segments
        segments = []
        for (s,e) in segmentoids:
            segments.append(self.segmentBetween(s,e))
        wire = Wire(segments)

        # check if there are common nodes with existing wires
        # if so, just add these nodes to the other wire (only distinct ones)
        removables = []
        for existing_wire in self.wires:
            points = existing_wire.getPoints()
            for node in wire.getNodes():
                if node in points: # ok, wire and existing_wire should be merged
                    print("Overlapping wires!")
                    removables.append(existing_wire)
                    self.mergeWires(wire,existing_wire)
                    break # next wire

        if len(removables) > 0: # need to merge
            # TODO: might be good to use linked list to make removing more efficient!
            # remove the existing ones as they have been merged to the new one
            for w in removables:
                del self.wires[self.wires.index(w)]

                #del self.wires[self.wires.index(w)]
        self.wires.append(wire)
        #print(self.wires)

    def mergeWires(self, w1, w2):
        for s in w1.segments:
            for p1 in s.getPoints(exclude_nodes=True):
                for node in w2.getNodes():
                    if node == p1:
                        print(node.toTuple())


    def nodeIn(self, x, y):
        # first check if the node already exists
        for node in self.nodes:
            if (x,y) == (node.x(), node.y()):
                return node
        # create a new node
        node = Node(x,y)
        self.nodes.append(node)
        return node

    def segmentBetween(self, start, end):
        for segment in self.segments:
            if (segment.start.toTuple(), segment.end.toTuple()) in [(start,end), (end,start)]:
                return segment
        # create a new node
        segment = Segment(self.nodeIn(*start), self.nodeIn(*end))
        self.segments.append(segment)
        return segment

    def stateOf(self, x, y):
        return self.nodeIn(x,y).state

    def simulate(self):
        portq = []
        # find all sources
        for port in self.ports:
            if port.type == PortType.SOURCE:
                portq.append(port)

        while portq > 0:
            # 1. dequeue next port
            # 2. simulate port (set output)
            # 3. assign values connected inputs, add input ports to queue
            # 4. repeat until queue is empty
            port = portq.pop()
            if port.simulate():
                portq += port.children()

    def report(self):
        nodes = list(map(lambda n: n.toTuple(), self.nodes))
        segments = list(map(lambda s: (s.start.toTuple(), s.end.toTuple()), self.segments))
        wires = list(map(lambda w: list(map(lambda s: (s.start.toTuple(), s.end.toTuple()), w.segments)), self.wires))
        return {
            "nodes":    ["Total: "+str(len(nodes)), nodes],
            "segments": ["Total: "+str(len(segments)), segments],
            "wires":    ["Total: "+str(len(wires)), wires],
            "ports":    ["Total: "+str(len(self.ports)), self.ports]
        }

###############################################################################
startTime = time.time()

schema = Schema()
schema.addWire([
    ((2,0),(2,1)),
    ((2,1),(4,1))
])
schema.addWire([
    ((2,0),(2,1)),
    ((2,1),(4,1))
])
print("----------------------------------")
print( schema.report() )

'''
nodes = [Node(2,0), Node(4,1), Node(2,1)]
segments = [
    Segment(nodes[0], nodes[2]),
    Segment(nodes[2], nodes[1]),
    # Segment(nodes[2], Node(3,2))
]
w1 = Wire(segments)
#assert( w1.getPoints() == [QVector2D(2.0, 0.0), QVector2D(2.0, 1.0), QVector2D(3.0, 1.0), QVector2D(4.0, 1.0)] )
#assert( w1.getNodes() == [QVector2D(2.0, 0.0), QVector2D(2.0, 1.0), QVector2D(4.0, 1.0)] )

src1 = SourcePort()
and1 = AndPort()
schema.addPort(src1)
schema.addPort(and1)
src1.set(1)
print(schema.ports[0].internalState)
src1.toggle()
print(schema.ports[0].internalState)

schema.addWire(w1)
schema.addWire(w1)
'''

sleep_extra = 0.001
time.sleep(sleep_extra)
print("\n> Took: {} ms".format(1000*(time.time() - startTime - sleep_extra)))
###############################################################################
