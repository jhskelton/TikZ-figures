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
	
	def f_(X,Y, ignore_NAN=ignore_NAN):

		if ignore_NAN:
			if np.isnan(X) and np.isnan(Y):
				return np.nan
		# otherwise
		return f(X,Y)


	x_is_np_array = type(x) == type(np.array([0]))
	y_is_np_array = type(y) == type(np.array([0]))

	if x_is_np_array or y_is_np_array:
		shape = None

		if x_is_np_array and not y_is_np_array:    shape = x.shape
		elif not x_is_np_array and y_is_np_array:  shape = y.shape
		else:
			### if both inputs are arrays: check if the shapes are the same
			# if they are not: raise value error

			if x.shape != y.shape: raise ValueError("Shape of input array are not equal. x.shape={0}  y.shape={1}".format(x.shape,y.shape))
			else:
				shape = x.shape

		# format output
		z = np.zeros(shape, dtype=complex)

		if x_is_np_array and not y_is_np_array:
			# check if x is a 1-dimensional array
			if x.ndim != 1: raise ValueError("Incompatible objects: x={0}  y={1}".format(x,y))

			for i in range(0, len(x)):
				z[i] = f_(x[i],y)

		elif not x_is_np_array and y_is_np_array:
			# check if y is a 1-dimensional array
			if y.ndim != 1: raise ValueError("Incompatible objects: x={0}  y={1}".format(x,y))

			for i in range(0, len(y)):
				z[i] = f_(x,y[i])

		else:
			# check if both objects are matrices!
			if x.ndim != 2: raise ValueError("Incomptiable objects, must be matrices: x={0}  y={1}".format(x,y))

			for i in range(0,len(x)):
				for j in range(0,len(x[i])):

					z[i][j] = f_(x[i][j], y[i][j])

		# output result
		return z

	else:
		# x,y are numerical values (not a numpy array - so simplify evaluate)
		return f_(x,y)


		



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





def solve_multi(xs,ys,f,g,c,eps, sigfig=6):
	X,Y = get_xy_mesh(xs,ys,eps)

	# get the bounding boxes
	X,Y,Zf,containf = get_bounding_box(X,Y,f,c[0])
	X,Y,Zg,containg = get_bounding_box(X,Y,g,c[1])

	containfg = containf*containg

	def fnc(p):
		x=p[0]; y=p[1]
		return( f(x,y)-c[0], g(x,y)-c[1] )

	sols = set()

	active_indices = np.argwhere(containfg)
	for i, j in active_indices:
				
		# set to be the centre of the box
		x0 = (X[i,j] + X[i,j+1])/2
		y0 = (Y[i,j] + Y[i+1,j])/2
				
		# run local root finder
		sol, info, ier, mesg = fsolve(fnc, (x0, y0), full_output=True)

		# check if fsolve converged successfully (ier == 1)
		if ier == 1:
			# round to avoid duplicates
			rounded_sol = (round(sol[0], sigfig), round(sol[1], sigfig))
			sols.add(rounded_sol)
		else:
			print("Warning:  Solution failed to converge\n(x0,y0)=({0},{1})".format(x0,y0))

	return list(sols)



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
