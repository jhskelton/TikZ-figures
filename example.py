
import matplotlib.pyplot as plt
import numpy as np


import contours
import write_csv


#from skimage import measure

"""
Key ideas of this example:
- create surface z=z(x,y)
- Compute contours
- downsample the contour curves using the Ramer-Douglas-Peucker algorithm
- compare, visually, the original and downsampled contours
- save the data to a csv file, ready for TikZ to process it

Please vary the 'eps' variable to get tighter or more polygonal fits.

"""

eps = 0.1



## set up the x,y,z values

X = np.linspace(-1,1,1000)
Y = np.linspace(-1,1,1000)
Xs,Ys = np.meshgrid(X,Y)
Zs = np.sin(6*Xs) + np.sin(6*Ys)



# compute the contours!
levels = [-1.6,-1.4 -0.8, -0.5, 0, 0.5, 0.8, 1.4, 1.8]

CS, level_values = contours.get_contours(Xs,Ys,Zs, levels)


####  Now try to downsample the contour plots and compare!

CS_downsample = contours.downsample_contour_RDP(CS, eps)



# show difference!
og_len = 0
new_len = 0
for contour in CS: og_len += len(contour[0,:])
for contour in CS_downsample: new_len += len(contour[0,:])

print("Downsampled from {0} points to {1} points!".format(og_len, new_len))



## plot surface to see if okay

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#ax.plot_surface(U_mesh, PU_mesh, Gs)
ax.plot_surface(Xs, Ys, Zs)


for curve in CS:
	X = curve[:,0]
	Y = curve[:,1]
	Z = np.sin(6*X) + np.sin(6*Y)

	ax.plot3D(X,Y,Z, '--', linewidth=5)

ax.set_xlabel("x")
ax.set_ylabel("y")



# plot the contours on the x,y plane!

plt.figure()
for contour in CS:
	plt.plot( contour[0,:], contour[1,:])
plt.xlabel("x")
plt.ylabel("y")



plt.figure()
for contour in CS:
	plt.plot( contour[0,:], contour[1,:])

for contour in CS_downsample:
	plt.plot( contour[0,:], contour[1,:], "r--")

plt.xlabel("x")
plt.ylabel("y")



plt.show()



write_csv.write_contour_csv("example.csv", "x,y,z", CS_downsample, level_values)



