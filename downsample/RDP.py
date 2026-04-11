"""
Ramer-Douglas-Peucker Algorithm, downsample.

https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm#Pseudocode
"""
import numpy as np

def perpendicular_distance(x1,y1,x2,y2,a,b):
	"""
	Find the perpendicular distance of (a,b) from the line connecting (x1,y1) and (x2,y2).

	Assume line takes the form:
	Ax+By+C=0
	"""
	A = 1
	B = 1
	C = 1

	if (x1==x2 and y1==y2):
		raise ValueError("Cannot compute perpendicular distance of line represented by a single point.")

	elif (x1==x2):
		B=0
		C=-x1

	elif (y1==y2):
		A=0
		C=-y1

	else:
		A = -(y2-y1)/(x2-x1)
		C = (y2*x1-x2*y1)/(x2-x1)

	# now apply the formula to the line:
	d = np.abs(A*a+B*b+C)/np.sqrt(A**2+B**2)
	return d




def RDP(X,Y,eps, start=0, end=-1):
	"""
	Let X,Y be a list of x,y values of a curve.
	We want to downsample, and let

	Should manually select the start and ending points of the curve to initiate the algorithm with.
	For example, a circle is a closed loop, so should do: start=0, end=end/2.


	Function will break if curve is a closed loop!  Need to manually slip into two.
	"""

	# The default is -1 means end value.  Change this to mean the final index
	if end==-1: end = len(X)-1


	# find the point with maximum distance from the line connected the first and last points

	max_dist = 0
	index = 0

	for i in range(start+1, end-1):
		d = perpendicular_distance( X[start],Y[start], X[end], Y[end], X[i], Y[i] )

		if d>max_dist:
			max_dist = d
			index = i


	output_indices = []

	# if the max distance is greater than the tolerance eps, iterate recursively.
	if max_dist < eps:
		output_indices = [start, end]

	else:
		# partition list into [start, mid, end]
		left_output = RDP(X,Y,eps, start=start, end=index)
		right_output = RDP(X,Y,eps, start=index, end=end)

		# merge
		output_indices = left_output[0:-1] + right_output

	return output_indices




