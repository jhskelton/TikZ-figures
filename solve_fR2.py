import numpy as np
from scipy.optimize import fsolve 




def pointwise_eval(x,y,f, ignore_NAN=False):
	"""
	evaluate f(x,y) where x,y may be matrices or vectors
	Return corresponding object - either matrix or vector

	Three options:
	 - 1) both are scalars
	 - 2) either x or y is a vector, the other must be a scalar.
	 - 3) both are matrices (of equal shapes)
	"""


	x_is_arr = isinstance(x, np.ndarray)
	y_is_arr = isinstance(y, np.ndarray)

	fnc = lambda x,y: np.nan if ignore_NAN and np.isnan(x) or np.isnan(y) else f(x,y)


	# check shapes and sizes

	if not x_is_arr and not y_is_arr:
		# just 2 numbers
		return fnc(x,y)


	elif x_is_arr and y_is_arr:
		if x.shape != y.shape: 
			raise ValueError("Shape of input array are not equal. x.shape={0}  y.shape={1}".format(x.shape,y.shape))

		# check if both are matrices
		if x.ndim != 2:
			raise ValueError(f"Must be 2d Matrices: x.shape={x.shape}  y.shape={y.shape}")

	elif x_is_arr:
		if x.ndim != 1: raise ValueError("Vector x must be 1d: x.dim={x.dim}")
	elif y_is_arr:
		if y.ndim != 1: raise ValueError("Vector y must be 1d: y.dim={y.dim}")


	vectorise_fnc = np.vectorize(fnc,otypes=[complex])

	return vectorise_fnc(x,y)
	



def get_xy_mesh(xs,ys,eps):
	x0,x1 = xs[0], xs[1]
	y0,y1 = ys[0], ys[1]

	x_arr = np.arange(x0,x1,eps)
	y_arr = np.arange(y0,y1,eps)

	X,Y = np.meshgrid(x_arr,y_arr)
	return X,Y



def get_bounding_box(X,Y,f,c):

	Z = np.real( pointwise_eval(X,Y, f) )

	# classify if above or below the F=c value

	B = np.greater(Z, c)

	# enumerate over all of the bounding boxes
	(Nx,Ny) = B.shape
	contain = np.zeros((Nx-1, Ny-1))

	# extract the grid corners
	TL = B[:-1, :-1]
	TR = B[1:, :-1]
	BL = B[:-1, 1:]
	BR = B[1:, 1:]

	# a contour passes through the the cell if the corners are all not true or all note false
	contain = ~( (TL==TR) * (TR==BL) * (BL==BR) )

	return X,Y,Z,contain





def solve_fR2(xs,ys,f,g,c,eps, sigfig=6):
	"""
	Input for c can either be a pair of scalars
	c = [c1,c2]
	
	A list of pairs
	c = [ [c11,c12], [c21,c22], [c31,c32] ]

	Or a matrix
	c = [ [c11,c12,c13,...,c1n], ..., [cm1,...,cmn] ] 
	"""

	X,Y = get_xy_mesh(xs,ys,eps)

	Zf = np.real( pointwise_eval(X,Y, f) )
	Zg = np.real( pointwise_eval(X,Y, g) )

	sol_list = None

	def solve_fR2_scalar(c0):
		# For a given scalar c0, find the set of solutions
	
		# get the bounding boxes
		containf = get_bounding_box(X,Y,Zf,c0[0])
		containg = get_bounding_box(X,Y,Zg,c0[1])

		containfg = containf*containg

		def fnc(p):
			x=p[0]; y=p[1]
			return( f(x,y)-c0[0], g(x,y)-c0[1] )

		sols = set()

		active_indices = np.argwhere(containfg)

		for i, j in active_indices:

		#Nx,Ny = containfg.shape
		#for i in range(0,Nx):
		#	for j in range(0,Ny):
		#		if containfg[i,j]:
					
			# set to be the centre of the box
			x0 = (X[i,j] + X[i,j+1])/2
			y0 = (Y[i,j] + Y[i+1,j])/2
					
			# Run local root finder
			sol, info, ier, mesg = fsolve(fnc, (x0, y0), full_output=True)

			# Check if fsolve converged successfully (ier == 1)
			if ier == 1:
				# Round to avoid duplicates
				rounded_sol = (round(sol[0], sigfig), round(sol[1], sigfig))
				sols.add(rounded_sol)
			else:
				print("Warning:  Solution failed to converge\nat (x0,y0)=({0},{1})".format(x0,y0))

		return list(sols)


	if not isinstance(c, np.ndarray) and not isinstance(c, list) and not isinstance(c, tuple)
		raise ValueError(f"Constant c needs to be a pair of numbers [c1,c2] or a list of them.\nInstead c={c}")

	if not isinstance(c[0], np.ndarray) and not isinstance(c[0], list) and not isinstance(c[0], tuple):
		# check if scalar
		sol_list = solve_f_scalar(c)

	else:
		# assume list of c values
		sol_list = [ solve_f_scalar(c0) for c0 in c ]

	return sol_list





if __name__ == "__main__":

	# as an example
	f = lambda x,y: x**2 - y**2
	g = lambda x,y: 2*x*y

	a = 1
	b = 2

	xs = [-10,10]
	ys = [-10,10]


	sols = solve_multi(xs, ys, f, g, c=(a,b), eps=0.05, sigfig=8)
	
	# print solutions
	for sol in sols:
		x,y=sol
		print("x={0},  y={1},  f={2:.5f},  g={3:.5f}".format(x,y,f(x,y),g(x,y)))
