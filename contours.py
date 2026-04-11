
import numpy as np
from contourpy import contour_generator

import curves




def get_contours(Xs,Ys,Zs, levels):
	"""
	Return the contours as a list of curves with connected components.
	"""
	cont_gen = contour_generator(x=Xs, y=Ys, z=Zs)
	cs = cont_gen.multi_lines(levels)

	# separate level sets into separate individual curves
	CS = []
	level_values = []

	for i,level_sets in enumerate(cs):
		for curve in level_sets:
			N = len(curve)
			X = [ curve[i][0] for i in range(0, N) ]
			Y = [ curve[i][1] for i in range(0, N) ]

			CS += [ np.array([X,Y])]
			level_values += [ levels[i] ]

	return CS, level_values






def downsample_contour_RDP(CS, eps):

	CS_downsample = []

	# downsample the contours!
	for i, contour in enumerate(CS):
		# split into sections separated by critical points
		Xs = contour[0,:]
		Ys = contour[1,:]

		RDP_indices = curves.downsample_curve_RDP(Xs,Ys,eps)

		### We have now constructed the set of indices!
		Xs_RDP = [Xs[i] for i in RDP_indices]
		Ys_RDP = [Ys[i] for i in RDP_indices]

		new_contour = np.array( [Xs_RDP, Ys_RDP] )
		CS_downsample += [ new_contour ]

	return CS_downsample

