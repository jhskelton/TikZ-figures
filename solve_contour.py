import numpy as np
from scipy.optimize import fsolve 
from scipy.integrate import solve_ivp

import matplotlib.pyplot as plt



def compute_contour_segment(z0,fx,fy,t_end,a=1, max_dt=np.inf, atol=1e-6, rtol=1e-3, r=1, t_bnd=1, maxz=[+np.inf, +np.inf], minz=[-np.inf, -np.inf], crt_thresh=1e-16):
	"""
	Compute contour in the forwards driection

	Define event to check if to terminal the numerical integration


	Solution curve is formed by integrating the gradient
	grad F = [f_x,f_y]

	Issues can arise if we hit/reach a critical point: grad F = 0


	CURRENT PROBLEM:  Cannot actually reach or extend to the critical point.
	Since I give the gradient functions, it should not be too hard to actually solve for the crtitical point
	"""

	x0,y0=z0
	maxx,maxy=maxz
	minx,miny=minz

	z0 = np.asarray(z0, dtype=float)


	def near_start(t, z):
		# check if ||z0-z|| < r
		#d = np.sqrt( (x0-z[0])**2 + (y0-z[1])**2 )
		d = np.linalg.norm(z - z0)
		if t>t_bnd:  
			# check if enough time has passed
			return d-r
		else:
			return 1


	def out_of_bnds(t,z):
		# check if min_x < x < max_x fails
		# make the fnc continuous to works well with solve_ivp root finding algo
		return min(maxx-z[0], maxy-z[1], z[0]-minx, z[1]-miny)


	def critical_pt(t,z):
		# compute the magnitude of the gradient vector, 
		# and check if it is less than some threshold
		return np.sqrt( fx(z[0],z[1])**2 + fy(z[0],z[1])**2 ) - crt_thresh



	near_start.terminal = True
	near_start.direction = -1

	out_of_bnds.terminal = True
	out_of_bnds.direction = -1

	critical_pt.terminal = True
	critical_pt.direction = -1


	# define dy/dt(t,y)
	ode = lambda t,z: np.array([ a*fy(*z), -a*fx(*z) ])

	sol = solve_ivp(ode, [0,t_end], z0, max_step=max_dt, atol=atol, rtol=rtol, events=[near_start, out_of_bnds, critical_pt])
	return sol.t, sol.y, sol.t_events, sol.y_events






if __name__ == "__main__":

	# as an example
	f = lambda x,y: x**2 + y**2

	fx = lambda x,y: 2*x
	fy = lambda x,y: 2*y

	p = np.array([1,0])

	_, sol,_,_ = compute_contour_segment(p,fx,fy,100,a=-1, max_dt=0.001, t_bnd=1, r=.001, minz=[-2, -np.inf])

	plt.figure()
	plt.plot(sol[0], sol[1])
	plt.show()



	# hyperbola w/ a critical point
	fx = lambda x,y: 2*x
	fy = lambda x,y: -2*y

	p = np.array([1,1])

	_, sol, tevent, yevent = compute_contour_segment(p,fx,fy,100,a=1, max_dt=0.001, t_bnd=1, r=.001, minz=[-2, -np.inf])

	sol2 = []

	if len(tevent[2]) != 0:
		x0 = yevent[2][0][0]
		y0 = yevent[2][0][1]
		print(f"Hit critical point! at t={tevent[2][0]:.3g}, (x,y)=({x0:.3g},{y0:.3g})")


		fnc = lambda z: (fx(z[0],z[1]), fy(z[0],z[1]) )
		# Run local root finder
		sol2, info, ier, mesg = fsolve(fnc, (x0, y0), full_output=True)

		print("critical point is at: ", sol2)


	plt.figure()
	plt.plot(sol[0], sol[1])

	if len(sol2) > 0:
		plt.plot(sol2[0], sol2[1], "r*")


	plt.show()