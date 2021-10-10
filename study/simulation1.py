from PyQt5.QtGui import QVector2D
import math

class QVector2D(QVector2D):
    def __init__(self, *args):
        super().__init__(*args)

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

class Node(QVector2D):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.state = None
        self.x = x
        self.y = y

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
        elif not (start.x == end.x or start.y == end.y):
            raise ValueError("Segment must be strictly horizontal or vertical!")

        self.start = start
        self.end = end

    def isVertical(self):
        return self.start[0] == self.end[0]
    def isHorizontal(self):
        return self.start[1] == self.end[1]
    def length(self): # since this is always ver or hor, we can just return difference in coords
        return abs(self.start.x-self.end.x + self.start.y-self.end.y)

    def getPoints(self):
        # delta vector, the vector between each points in this segment
        delta = QVector2D(self.end-self.start).normalized()
        points = []
        for i in range(self.length() + 1):
            points.append(self.start + i*delta)
        return points

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

    def getPoints(self):
        ''' Point refers to any grid point that the wire crosses, not only nodes. '''
        points = []
        for segment in self.segments:
            for point in segment.getPoints():
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

###############################################################################
nodes = [Node(2,0), Node(4,1), Node(2,1)]
segments = [
    Segment(nodes[0], nodes[2]),
    Segment(nodes[2], nodes[1]),
    # Segment(nodes[2], Node(3,2))
]
w1 = Wire(segments)
print( w1.getPoints() )
print( w1.getNodes() )

###############################################################################
class PortTypes:
    NONE = 0
    SOURCE = 1
    PRIMITIVE = 2 # AND, OR, NOT, XOR, ...

class Port:
    port_type = PortTypes.NONE
    label = ''
    inputs = []
    output = None
    
    def __init__(self, port_type, inputs, label=''):
        self.port_type = port_type
        self.inputs = []
        self.output = Output(self)
        
        self.label = label

        for i in range(0,inputs):
            self.inputs.append(Input(self))

    def inputStates(self):
        states = []
        for i in self.inputs:
            states.append(i.state)
        return states

    def inputState(self, input=0):
        return self.inputs[input]


class AndPort(Port):
    def __init__(self):
        super().__init__(self, PortTypes.PRIMITIVE, )

    def simulate(self):
        self.output = int(all(self.inputStates()))



class Schema:
    ports = []
    '''
    WIRES:
      1) two wires cannot share a node
        - if so, they are merged to one
      2) wire cannot run over another wire's node (but CAN over another wire segment)
        - if so, they are merged to one
    '''
    wires = []

    def addPort(self, port):
        pass

    def addWire(self, wire):
        # check if there are common nodes with existing wires
        # if so, just add these nodes to the other wire (only distinct ones)
        for existing_wire in self.wires:
            for node in wire.nodes:
                if node in existing_wire.nodes:
                    pass

        self.wires.append()

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
