class Input:
    parent = None
    state = 0
    
    def __init__(self, parent):
        self.parent = parent


class Output:
    parent = None
    state = 0
    
    def __init__(self, parent):
        self.parent = parent
        self.state = 0


class Port:
    port_type = 'NONE'
    label = ''
    inputs = []
    output = None
    
    def __init__(self, port_type, inputs, label=''):
        # TODO: Validation by port_type (e.g. AND can have 1 output etc...)
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


class Schema:
    ports = []
    connections = []
    
    def __init__(self):
        self.ports = []
        self.connections = []
    
    def addPort(self, port):
        if isinstance(port, list):
            self.ports += port
        else:
            self.ports.append(port)
    
    def addConnection(self, a, b):
        if (a,b) not in self.connections:
            self.connections.append((a,b))
    
    def simulate(self):
        for (a,b) in self.connections:
            b.state = a.state
            b.parent.simulate()


#############################
# PORTS (belong to their own file)
##############################

class AndPort(Port):
    def __init__(self, label = '', inputs = 2):
        Port.__init__(self, 'AND', inputs, label)

    def simulate(self):
        print(self.inputStates())
        self.output = int(all(self.inputStates()))


class SourcePort(Port):
    def __init__(self, label = '', inputs = 0):
        Port.__init__(self, 'SOURCE', inputs, label)

    def simulate(self):
        pass

    def set(self, state):
        self.output = state

    def toggle(self):
        self.output = int(not self.output)
