import sys, pytest, timeit

from Scigol import *

'''
	Description...
'''


'''
O1 = S1 + (S2 * S3)
'''
@pytest.mark.parametrize("test_input,expected", [
    ( (0,0,0), 0 ),
    ( (0,0,1), 0 ),
    ( (0,1,0), 0 ),
    ( (0,1,1), 1 ),
    ( (1,0,0), 1 ),
    ( (1,0,1), 1 ),
    ( (1,1,0), 1 ),
    ( (1,1,1), 1 ),
])
def test_3SRC_AND_OR_1OUT(test_input, expected):
    # setup (TODO: this same thing is repeated for each test_input!)
    schema = Schema()
    src1    = SourcePort()
    src2    = SourcePort()
    src3    = SourcePort()
    and1    = AndPort()
    or1     = OrPort()
    schema.addConnection(src1.output, or1.inputs[0])
    schema.addConnection(src2.output, and1.inputs[0])
    schema.addConnection(src3.output, and1.inputs[1])
    schema.addConnection(and1.output, or1.inputs[1])
    
    src1.set(test_input[0])
    src2.set(test_input[1])
    src3.set(test_input[2])
    schema.simulate()
    assert(or1.output == expected)
