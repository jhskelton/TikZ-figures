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




def find_turning_points_ind(X, skip_rpts=True):
	"""
	Find indices that correspond to turning points of X.
	Do not include start and end index.

	if skip_rpts=True, then only include the first index for a sequence of constant values.
	"""

	lnX = len(X)

	if lnX==2:
		return []

	indices = []
	i=1
	while i < lnX-1:

		# if the prev_element = cur_element or cur_element = next_element
		# then this may obsfuscate that there exists a local critical point(s)
		# find the last and next vals that are different
		i_prev = i-1
		i_next = i+1
		while X[i_prev] == X[i] and i_prev>0: i_prev -= 1
		while X[i_next] == X[i] and i_next<lnX-1: i_next += 1

		# check if the interval x_{i_prev}, x_i, x_{i_next} is monotonic
		monotonic = False
		if X[i_prev] < X[i] and X[i] < X[i_next]:  monotonic = True
		elif X[i_prev] > X[i] and X[i] > X[i_next]:  monotonic = True

		if not monotonic:
			# add the index, since a local critical pt
			indices += [i]

		if skip_rpts:
			# update the i index to be the next element different to X[i]
			i=i_next
		else:
			i+=1

	return indices





def downsample_curve_RDP_ind(X,Y,eps):
	"""
	Given a curve X,Y, find the indices to downsample it.
	"""

	# find the indices that give turning points
	X_turning_pts = find_turning_points_ind(X)
	Y_turning_pts = find_turning_points_ind(Y)

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
