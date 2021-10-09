from Scigol import *

schema = Schema()
src1 = SourcePort()
src2 = SourcePort()
and1 = AndPort()

# HOX: schema.addConnection(and1.output, and1.inputs[0], and2.inputs[1])
schema.addConnection(src1.output, and1.inputs[0])
schema.addConnection(src2.output, and1.inputs[1])

src1.set(1)
src2.set(1)
schema.simulate()

print(src1.output)
print(and1.output)
