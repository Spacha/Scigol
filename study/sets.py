'''
a = set([1,2,3,4,5])
b = set([2,3,8])


print(a.union(b))
print(a | b)

print(a.intersection(b))
print(a & b)

print(a.difference(b))
print(a - b)

print(a.symmetric_difference(b))
print(a ^ b)
'''
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __add__(self, other):
        if (isinstace(other, Node)): # list of nodes
            # one node can split a segment to two new segments
            if self.p1[0] <= other.x <= self.p2[0] and self.p1[1] <= other.y <= self.p2[1]:
                pass
class Wire:
    def __init__(self, segmentoids):
        self.segments = set(segmentoids)
    def __or__(self, other):
        return Wire(self.segments | other.segments)
    def __xor__(self, other):
        return Wire(self.segments ^ other.segments)

'''
a:
xxxxx
    x
b:
    x
    xxxxx
c = a | b:
xxxxx
    xxxxx
'''
a = Wire([(0,0), (1,0), (1,1)])
b = Wire([(1,0), (1,1), (2,1)])
print(a.segments)
print(b.segments)

c = a | b
d = a ^ b

print(c.segments)
print(d.segments)