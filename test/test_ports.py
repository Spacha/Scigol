import sys, pytest, timeit

from Scigol import *

'''
	Description...
'''

@pytest.mark.parametrize("test_input,expected", [
    ( (0,0), 0 ),
    ( (0,1), 0 ),
    ( (1,0), 0 ),
    ( (1,1), 1 ),
])
def test_port_AND(test_input, expected):
	''' . '''

	# setup
	schema = Schema()
	src1 = SourcePort()
	src2 = SourcePort()
	and1 = AndPort()
	schema.addConnection(src1.output, and1.inputs[0])
	schema.addConnection(src2.output, and1.inputs[1])
	
	src1.set(test_input[0])
	src2.set(test_input[1])
	schema.simulate()
	assert(and1.output == expected)

@pytest.mark.parametrize("test_input,expected", [
    ( (0,0), 0 ),
    ( (0,1), 1 ),
    ( (1,0), 1 ),
    ( (1,1), 1 ),
])
def test_port_OR(test_input, expected):
	''' . '''

	# setup
	schema = Schema()
	src1 = SourcePort()
	src2 = SourcePort()
	or1 = OrPort()
	schema.addConnection(src1.output, or1.inputs[0])
	schema.addConnection(src2.output, or1.inputs[1])
	
	src1.set(test_input[0])
	src2.set(test_input[1])
	schema.simulate()
	assert(or1.output == expected)
