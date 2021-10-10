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

    def inputState(self, input=0):
        return self.inputs[input]


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
        '''
        Types of connections:
            # Logical connections:
            1) OUT(a) -> IN(b)
                * just add
            2) IN(a) -> OUT(b)
                * flip around and add

            3) IN(a) -> IN(b)
                * add to connectedInputs
            4) OUT(a) -> OUT(b)
                * invalid
            * check if IN appears in connectedInputs:
              if so, connect the connected inputs to OUT as well and remove the element
        '''
        if a isinstance(Input):
        if (a,b) not in self.connections:
            self.connections.append((a,b))
    
    def simulate(self):
        for (a,b) in self.connections:
            b.state = a.state
            b.parent.simulate()

    def children(self, port):
        ''' Ports connected to the output of @port. '''
        return


#############################
# PORTS (belong to their own file)
##############################

class AndPort(Port):
    def __init__(self, label = '', inputs = 2):
        Port.__init__(self, 'AND', inputs, label)

    def simulate(self):
        print(self.inputStates())
        self.output = int(all(self.inputStates()))

class OrPort(Port):
    def __init__(self, label = '', inputs = 2):
        Port.__init__(self, 'OR', inputs, label)

    def simulate(self):
        print(self.inputStates())
        self.output = int(any(self.inputStates()))

class NotPort(Port):
    def __init__(self, label = ''):
        Port.__init__(self, 'NOT', 1, label)

    def simulate(self):
        print(self.inputStates())
        self.output = int(not self.inputState())


class SourcePort(Port):
    def __init__(self, label = '', inputs = 0):
        Port.__init__(self, 'SOURCE', inputs, label)

    def simulate(self):
        pass

    def set(self, state):
        self.output = state

    def toggle(self):
        self.output = int(not self.output)
