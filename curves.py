from downsample import RDP


def form_intervals(indices,N):
	"""
	Suppose that indices represent where critical / turning points occur.
	Form arrays of indices

	N = length of original list
	"""

	I = [0] + sort(indices) + [N-1]

	output = []
	for i in range(0, len(indices)-1):
		index0 = indices[i]
		index1 = indices[i+1]

		output += [ [j for j in range( index0, index1+1 )] ]
	return output




def find_turning_points(X):
	"""
	Find indices that correspond to turning points of X.
	Do not include start and end index.
	"""

	indices = []
	for i in range(1, len(X)-1):

		# check if the interval x_{i-1}, x_i, x_{i+1} is monotonic
		monotonic = False
		if X[i-1] <= X[i] and X[i] <= X[i+1]:  monotonic = True
		elif X[i-1] >= X[i] and X[i] >= X[i+1]:  monotonic = True

		if not monotonic:
			indices += [i]

	return indices





def downsample_curve_RDP(X,Y,eps):
	"""
	Given a curve X,Y, find the indices to downsample it.
	"""

	X_turning_pts = find_turning_points(X)
	Y_turning_pts = find_turning_points(Y)

	# Construct the intervals of indices ending on each critical point
	interval_pts = sorted(set( [0] + X_turning_pts + Y_turning_pts + [len(X)-1] ) )

	# on each interval apply the Ramer-Douglas-Peucker algorithm to downsample the number of points
	RDP_indices = []
	for i in range(0, len(interval_pts)-1):
		start = interval_pts[i]
		end = interval_pts[i+1]

		indices_ = RDP.RDP(X,Y, eps, start=start, end=end)
		RDP_indices += indices_

	# remove duplicates
	return sorted(set(RDP_indices))







if __name__ == "__main__":

	X = [1,2,3,4,3,2,1,0,-1,0,1,2,3,2,1,2,3,4,5]

	intervals = split_into_fncs(X)

	for inter in intervals:
		X_inter = [ X[i] for i in inter ]
		print(X_inter)




"""
def split_into_fncs(X):
	Suppose X is the X component of a curve [X,Y],
	and we want to make y=y(x) a function!

	key idea: find intervals of X where it is monotonically increasing / decreasing

	Return list of lists with indices.  Start and end points will overlap.

	# first identify the turning points
	# append start and end values to make easier to process
	turning_indices = [0] + find_turning_points(X) + [len(X)-1]


	# now construct the output
	output = []

	i0 = 0
	for i in range(0, len(turning_indices)-1):
		output += [ [j for j in range( turning_indices[i], turning_indices[i+1]+1 )] ]

	return output
"""
