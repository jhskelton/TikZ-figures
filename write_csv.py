import os



def write_contour_csv(name, header, CS, level_values):
	"""
	Function takes in name of output file, the header string, and a set of contour curves.
	Save all of the information faithfully as a csv file.

	PGFPlots uses double line breaks to separate segments.
	Hence, contours will be separated by a double spacing in the csv file.

	CS is formatted as:
	- list of contours
	- Each contour is 2d numpy array, first index is x or y, second index is which vertex.
	"""

	# "cs" means contour sets
	with open(name, "w") as f:
		f.write(header+"\n")


		for i, contour in enumerate(CS):
			level_value = level_values[i]

			row_num = len( contour[0,:] )
			for i in range(0, row_num):
				x = contour[0,i]
				y = contour[1,i]

				# Write coordinates and a comma to separate path segments
				string = f"{x},{y},{level_value}\n"
				f.write(string)

			f.write("\n\n") # PGFPlots uses double line breaks to separate curves


