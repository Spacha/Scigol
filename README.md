# Planning & design

## Hierarchy
* Node
  * Input
  * Output
* Grid
  * Schema
    * Element
      * Port
      * Wire
      * Annotation
        * Text
      * Circuit

```
Grid:           Interface between user events and simulation. Captures mouse/keyboard
                events, interprets them and sends and modifies schema if needed.
Schema:         (Or simulation) takes care of the actual logic and simulation. Holds
                information of all elements, wires etc.

Node:           A point on the grid that has a state (0/1/unknown). Inputs and outputs
                are extensions of nodes having a state as well. Wires are collections
                of nodes.
Element:        Port, Wire, Annotation and everything that goes to the grid, is
                a special case of an element. Element always has grid coordinates.
Port:           An elementary gate that takes one or more inputs and converts them
                to one output.
Wire:           Series of segments on the grid that connects with nodes of all types.
                Wire connects nodes so that they share a state.
```

## Connections

|            | A = INPUT                                                                                                             | A = OUTPUT                                                                          |
|------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| B = INPUT  | A and B are bound to be the same value. If something is connected to A, it's connected to B as well (and vice versa). | Normal situation. A is defined by B.                                                |
| B = OUTPUT | Normal situation. B is defined by A.                                                                                  | Unless A = B, this is invalid situation since there is a disagreement of the state. |

Connections must always be tuples of format `(output, input)`. If we connect two inputs together, that is not considered a connection (at least not a logical one). Only when a connection from an output is made to either of those inputs, both inputs will be connected to the output.

```python
addConnection(and1.output, and1.input[0])
addConnection(and1.output, and1.input[1])
```

## Frontend

Drawing stuff. Takes care of the "physical" properties of connections (wires), ports and annotations: position, rotation, appearance etc. 

### Rotation

We have port with input and output nodes: `port_nodes = port.inputs + [port.output] = [(0,0),(0,2),(2,1)]`. 
To rotate it `a = 90` degrees clockwise, we need to make a simple matrix multiplication with rotation matrix R:
````
R = / cos(a) -sin(a) \   /x\
    \ sin(a)  cos(a) / * \y/
```
The same multiplication in simple algebraic form:
```
x_rotated = x*cos(a) - y*sin(a)
y_rotated = x*sin(a) + y*cos(a)
```

### Wiring logic

This is something between frontend and backend. Wiring logic receives mouse actions and outputs nets of ports and wires (not connections).

Value of a wire is always defined by the output that it's connected to it. If there are no outputs connected to it, it's state is unknown.

Fundamentally, only one of the 4 ways mentioned in the "Connections" section, but in practice, the user might create connection as follows:
1. Connect two ports by wire (inputs or outputs)
  Form a connection between the inputs and outputs
2. Connect two _wires_. Both can be connected to a number of ports
  

## Backend

Takes care of running the simulations. Requires a valid graph (i.e. no output-output connections, )
