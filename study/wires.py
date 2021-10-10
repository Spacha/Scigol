class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Wire:
    def __init__(self, points):
        self.nodes = []
        for point in points:
            if point not in self.nodes:
                self.nodes.append(Node(*point))

wires = []
wires.append( Wire([(3,0), (2,1), (4,1)]) )

for wire in wires:
    for node in wire.nodes:
        print(str((node.x, node.y)))
