import time
import pytest

'''
   0  1  2  3  4  5  6  7  8
0  .  .  .  .  .  .  .  .  .
1  .  .  .  .  .  .  .  .  .
2  .  .  .  .  .  .  .  .  .
3  .  .  .  .  .  .  .  .  .
4  .  .  .  .  .  .  .  .  .
5  .  .  .  .  .  .  .  .  .
'''

def isBetweenA(px, p1, p2):
	''' Compare both always. '''
	return (
		((p1[0] <= px[0] <= p2[0]) or (p2[0] <= px[0] <= p1[0]))
		and
	    ((p1[1] <= px[1] <= p2[1]) or (p2[1] <= px[1] <= p1[1])))

def isBetweenB(px, p1, p2):
	''' Check which is smaller and compare once. '''
	res = True
	# compare X
	if p1[0] < p2[0]:
		if not (p1[0] <= px[0] <= p2[0]):
			return False
	else:
		if not (p2[0] <= px[0] <= p1[0]):
			return False
	# compare Y
	if p1[1] < p2[1]:
		if not (p1[1] <= px[1] <= p2[1]):
			return False
	else:
		if not (p2[1] <= px[1] <= p1[1]):
			return False
	return True

def isBetweenC(px, p1, p2):
	''' Compare both always. '''
	if (p1[0] <= px[0] <= p2[0]):
		if (p1[1] <= px[1] <= p2[1]):
			return True
		if (p2[1] <= px[1] <= p1[1]):
			return True
	if (p2[0] <= px[0] <= p1[0]):
		if (p1[1] <= px[1] <= p2[1]):
			return True
		if (p2[1] <= px[1] <= p1[1]):
			return True
	return False

tests = [
	#...px....p1....p2....expected
	( (2,0),(1,0),(4,0),  True ),
	( (5,0),(1,0),(4,0),  False ),
	( (0,0),(-1,0),(1,0), True ),
	( (1,2),(1,1),(1,0),  False ),
	( (3,0),(3,1),(3,-1), True ),
	( (2,0),(3,1),(3,-1), False ),
	( (2,2),(2,5),(2,1),  True )
]

@pytest.mark.parametrize("px,p1,p2,expected", tests)
def test_A(px, p1, p2, expected):
	assert(isBetweenA(px, p1, p2) == expected)
@pytest.mark.parametrize("px,p1,p2,expected", tests)
def test_B(px, p1, p2, expected):
	assert(isBetweenB(px, p1, p2) == expected)
@pytest.mark.parametrize("px,p1,p2,expected", tests)
def test_C(px, p1, p2, expected):
	assert(isBetweenC(px, p1, p2) == expected)

timesA = []
timesB = []
timesC = []
N = 1000000
for i in range(N):
	px, p1, p2, _ = tests[i % len(tests)]
	
	sA = time.time()
	isBetweenA(px, p1, p2)
	timesA.append(time.time()-sA)
	
	sB = time.time()
	isBetweenB(px, p1, p2)
	timesB.append(time.time()-sB)

	sC = time.time()
	isBetweenC(px, p1, p2)
	timesC.append(time.time()-sC)

print("A:", sum(timesA)*1E6/N) # A: 0.47869 us
print("B:", sum(timesB)*1E6/N) # B: 0.55207 us
print("C:", sum(timesC)*1E6/N) # C: 0.51596 us

'''
After 1 000 000 tests:
	A: 0.5143229484558105
	B: 0.5579521656036377
	C: 0.5372418403625489
'''