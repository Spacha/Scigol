################################################################################
# Functions
# A collection of proven good (i.e. fast) methods for simple tasks.
################################################################################

def is_between(px, p1, p2):
	'''Returns true if point @px is between points @p1 and @p2
	   on either horizontal or vertical axis (NOT DIAGONAL).
	   See is_between.py for study.
	   * Execution time: 0.514 us
	'''
	return (((p1[0] <= px[0] <= p2[0]) or (p2[0] <= px[0] <= p1[0])) and
	        ((p1[1] <= px[1] <= p2[1]) or (p2[1] <= px[1] <= p1[1])))

# Hashing: use dicts!