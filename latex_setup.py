"""
export Matplotlib plots as latex pdf format -->  PGFPLOTS

Some notes:

For markersize, matplotlib measures the diameter, whereas tikz measures the radius



Comparison between Matplotlib and TikZ/PGFPlots (defaults)

Matplotlib plot Line Width: 1.5 pt
PGFPlots   plot Line Width: 0.4 pt
"""

###   LATEX PRESETS

import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter


import os
import platform

os.environ["PATH"] += os.pathsep + '/Library/TeX/texbin'
os.environ["PATH"] += os.pathsep + '/usr/local/texlive/2026/bin/universal-darwin'



# Exact xcolor core palette definitions
LATEX_BLACK = '#000000'
LATEX_BLACK90 = '#1A1A1A'
LATEX_BLACK85 = '#262626'

LATEX_DARKGRAY  = '#404040'  # 75% black (This is what you want)
LATEX_GRAY      = '#808080'  # 50% black
LATEX_LIGHTGRAY = '#BFBFBF'  # 25% black

LATEX_WHITE = '#FFFFFF'

LATEX_RED = '#FF0000'
LATEX_BLUE = '#0000FF'
LATEX_DARKGREEN = '#008000'
LATEX_PURPLE = '#A020F0'

LATEX_GREEN = '#00A64F'

MPL_BLUE = '#1f77b4'


TIKZ_ULTRA_THIN = 0.1
TIKZ_VERY_THIN = 0.2
TIKZ_THIN = 0.4
TIKZ_SEMI_THICK = 0.6
TIKZ_THICK = 0.8
TIKZ_VERY_THICK = 1.2
TIKZ_ULTRA_THICK = 1.6



# For standard \usepackage{fullpage} (6.5 inches wide)
ratio = 0.8625
#ratio = 3/4
# ratio = 0.618 # golden ratio

LATEX_FULLWIDTH = 6.5

#width = 6.5*0.49; # not a fullpage but only half!
#height = width * ratio


# --> used for plot().  Not scatter(), since scatter uses pt^2
# Recall.  Matplotlib uses diameter, whereas tikz/pgf uses the radius
MARKERSIZE = {
	'small': 2, # 2pt
	'normalsize': 4, # 4pt
	'large': 8, # 8pt
}


# TODO:  for most plots I was using a markersize of 7pts.  Not sure why...




###  Define the fontsizes

fontsize = 12

# see here for documentation:  https://tug.org/texinfohtml/latex2e.html#Font-sizes
# I think it is hardcoded?

# write a dictionary to look up the LaTeX font sizes
LATEX_FONT_SIZES = {
	10: {
		'tiny': 5, 'scriptsize': 7, 'footnotesize': 8, 'small': 9, 'normalsize': 10, 
		'large': 12, 'Large': 14.4, 'LARGE': 17.28, 'huge': 20.74, 'Huge': 24.88
	},
	11: {
		'tiny': 6, 'scriptsize': 8, 'footnotesize': 9, 'small': 10, 'normalsize': 10.95, 
		'large': 12, 'Large': 14.4, 'LARGE': 17.28, 'huge': 20.74, 'Huge': 24.88
	},
	12: {
		'tiny': 6, 'scriptsize': 8, 'footnotesize': 10, 'small': 10.95, 'normalsize': 12, 
		'large': 14.4, 'Large': 17.28, 'LARGE': 20.74, 'huge': 24.88, 'Huge': 24.88
	}
}

def get_latex_fontsize(name, base=fontsize):
	if not isinstance(name,str):
		print("Overwriting LaTeX font size with size={name} font size.")
		return name
	if base not in LATEX_FONT_SIZES:
		raise ValueError(f"Invalid fontsize.  Must be 10pt, 11pt, or 12pt.  Not {base}pt.")
	else:
		return LATEX_FONT_SIZES[base][name]



# set line thickness
#normal_line = LATEX_THICK
#thick_line = LATEX_VERY_THICK

pagewidth = LATEX_FULLWIDTH



def load_latex_pgf(plotfontsize='normalsize', axeslabelsize='normalsize', titlesize='normalsize', ticksize='normalsize', legendsize='normalsize',
				linewidth=TIKZ_THIN, axiswidth=TIKZ_THIN, tickwidth=TIKZ_VERY_THIN, legendwidth=TIKZ_THIN):
	"""
	DEFAULTS:
	axis line width:  thin
	tick line width:  very thin
	line width: thin

	major tick length: 0.15cm
	minor tick length: 0.15cm
	"""

	#### export plots as latex pdf format -->  PGFPLOTS

	mpl.use("pgf")  # Directs matplotlib to use LaTeX's pgf engine for output

	mpl.rcParams.update({
	    "pgf.texsystem": "pdflatex",        # Or "lualatex" / "xelatex"
	    "text.usetex": True,                # Use native LaTeX to render all text
	    # font
	    "font.family": "serif",
	    "font.serif": [],                  # Leave empty so it inherits the TeX preamble font
	    "font.sans-serif": [],
	    # font sizes
	    "font.size": get_latex_fontsize(plotfontsize),   # Set default font size to match the document
	    "axes.labelsize": get_latex_fontsize(axeslabelsize),
	    "axes.titlesize": get_latex_fontsize(titlesize),
	    "xtick.labelsize": get_latex_fontsize(ticksize),
	    "ytick.labelsize": get_latex_fontsize(ticksize),
	    "legend.fontsize": get_latex_fontsize(legendsize),
	    # set axes & ticks line thickness
	    "axes.linewidth": axiswidth,
	    "xtick.major.width": tickwidth,
	    "ytick.major.width": tickwidth,
	    # set the tick lengths
	    "xtick.major.size": cm_to_tex_pt(0.15),
	    "ytick.major.size": cm_to_tex_pt(0.15),
	    "xtick.minor.size": cm_to_tex_pt(0.1),
	    "ytick.minor.size": cm_to_tex_pt(0.1),
	    # set the legend frame style
	    "legend.frameon": True,
		"legend.facecolor": "white",
		"legend.framealpha": 1.0,        # opaque white background
		"legend.edgecolor": "inherit",
		"legend.fancybox": False,        # Sharp corners instead of rounded (Matplotlib default is rounded)
		"legend.handlelength": 1.7,      # Length of legend line samples
		"patch.linewidth": legendwidth,
		# set the linewidth
		"lines.linewidth": linewidth,
	    # latex premable
	    "pgf.preamble": (
	        r"\usepackage[utf8]{inputenc}"
	        r"\usepackage[T1]{fontenc}"
	        r"\usepackage{pgfplots}"
	        r"\usepackage{amsmath,pgfplots}"
	        r"\pgfplotsset{compat=1.18}"
	        #r"\pgfplotsset{set layers}" # render the layers using matplotlibs zorder
	    )
	})

	return



def style_axes_box(fig,ax,xlabel,ylabel, ylabel_pad=6, trim_floats=False, 
					xlim=None, ylim=None, xpad=0.1,ypad=0.1, 
					enable_autoscale=False, enable_limpad=False):
	"""
	Style the matplotlib box to make it resemble a tikz pgfplots box.

	Default Matlab:
	xpad=0.05 --> 5% padding / margin on each side of the plot
	ypad=0.05

	Default PGF
	xpad=0.1
	ypad-0.1

	TODO:
	Is there an error with doing set_lim before ax.margin ?  Or vice versa?  Does it matter?
	Need to test!!!
	"""

	def get_lim_pad(lim, pad):
		if not enable_limpad:
			return lim
		else:
			lim_len = lim[1]-lim[0]
			return [ lim[0] - pad*lim_len, lim[1] + pad*lim_len ]

	
	#if xlim is not None:  ax.set_xlim( (1+xpad)*np.asarray(xlim) )
	#if ylim is not None:  ax.set_ylim( (1+ypad)*np.asarray(ylim) )

	# update limits first if they exist  -->  automatically this disables autoscale
	if xlim is not None:  
		ax.set_xlim( get_lim_pad(xlim,xpad) )

	if ylim is not None:  
		ax.set_ylim( get_lim_pad(xlim,ypad) )

	# turn back on autoscale (this allows for margins around the x,y lims)
	if enable_autoscale:  ax.set_autoscalex_on(True); 


	# Style the structural framework to mimic a PGFPlots axis environment
	ax.spines[ ['top','right'] ].set_visible(True)

	# Inward ticks & ensure ticks sit on top of the curves by high zorder
	ax.tick_params(direction='in', which='both', top=True, right=True, zorder=10) 

	# update padding on the axes  -->  set padding xpad% for x, and ypad% for y
	ax.margins(x=xpad, y=ypad)

	# Add native LaTeX math strings for labels
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel, rotation=0, labelpad=ylabel_pad, verticalalignment='center')

	if trim_floats:
		# Apply a dynamic string formatter to strip trailing zeros
		# {x:g} automatically fstrips unnecessary decimal zeros (general floats)
		ax.xaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
		ax.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))




def style_axes_centre(fig,ax,xlabel,ylabel, xlab_pos=(1,0.5), ylab_pos=(0.5,1), trim_floats=False, 
					xlim=None, ylim=None, xpad=0.05,ypad=0.05, xlabelbottom=True, enable_autoscale=False, enable_limpad=False,
					draw_toparrow=True, draw_rightarrow=True):
	"""
	Style the matplotlib box to make it resemble a tikz pgfplots.
	Replicate PGFPlots "axis lines=middle" (Spines through origin)

	Default Matlab:
	xpad=0.05 --> 5% padding / margin on each side of the plot
	ypad=0.05

	Default PGF
	xpad=0.1
	ypad-0.1

	# enable_limpad has to work differently.

	TODO:
	Is there an error with doing set_lim before ax.margin ?  Or vice versa?  Does it matter?
	Need to test!!!
	"""
	def get_lim_pad(lim, pad):
		if not enable_limpad:
			return lim
		else:
			lim_len = lim[1]-lim[0]
			return [ lim[0] - pad*lim_len, lim[1] + pad*lim_len ]


	print("Warning: Please ensure that the x & y limits are set before configuring centre axis style.\nOR put xlim & ylim as keyword arguments")
	# Style the structural framework to mimic a PGFPlots axis environment

	# update limits first if they exist  -->  automatically this disables autoscale
	if xlim is not None:  ax.set_xlim( get_lim_pad(xlim,xpad) )
	if ylim is not None:  ax.set_ylim( get_lim_pad(ylim,ypad) )

	# turn back on autoscale (this allows for margins around the x,y lims)
	if enable_autoscale:  ax.set_autoscalex_on(True); 


	# update the spines to make them be centred at zero
	ax.spines[ ["left","bottom", "top", "right"] ].set_position("zero")
	# make the top and right spines invisible
	ax.spines[ ["top", "right"] ].set_visible(False)
	
	ax.tick_params(direction='inout', which='both', top=False, right=False)
	ax.xaxis.set_tick_params(labeltop=not xlabelbottom, labelbottom=xlabelbottom)

	# update padding on the axes  -->  set padding xpad% for x, and ypad% for y
	ax.margins(x=xpad, y=ypad)

	# Add native LaTeX math strings for labels
	ax.set_xlabel(xlabel, loc="right") # place label at the end of the axis
	ax.set_ylabel(ylabel, rotation=0)

	# move the axis labels (x,y) represent percentages from bottom left to top right
	ax.yaxis.set_label_coords(*ylab_pos)
	ax.xaxis.set_label_coords(*xlab_pos)

	"""
	# TODO  !!!

	# Set bounds with a slight offset to leave room for arrows
    x_offset = (xmax - xmin) * 0.05
    y_offset = (ymax - ymin) * 0.05
    
    ax.spines["bottom"].set_bounds(xmin, xmax - x_offset)
    ax.spines["left"].set_bounds(ymin, ymax - y_offset)

    # Add dynamic arrows to the axis tips based on data span
    arrow_dx = (xmax - xmin) * 0.1
    arrow_dy = (ymax - ymin) * 0.1

	"""

	#decorate the axes lines with arrow heads
	draw_arrowheads(fig,ax, top=draw_toparrow, right=draw_rightarrow)

	if trim_floats:
		# Apply a dynamic string formatter to strip trailing zeros
		# {x:g} automatically fstrips unnecessary decimal zeros (general floats)
		ax.xaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
		ax.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))


	# remove the zero labels
	xticks = ax.get_xticks()
	yticks = ax.get_yticks()

	ax.set_xticklabels( ["" if t==0 else label.get_text() for t, label in zip(xticks, ax.get_xticklabels())] )
	ax.set_yticklabels( ["" if t==0 else label.get_text() for t, label in zip(yticks, ax.get_yticklabels())] )
	#ax.set_xticklabels( ["" if t=="0"or t=="$0" else t for t in ax.get_xticklabels() ] ) 

	print("Zero marks removed from x and y axes.")


	"""
	# Doesnt work

	# 3. Explicitly set tick labels zorder manually across major ticks
	for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
		tick.tick1line.set_zorder(100)
		tick.tick2line.set_zorder(100)
		tick.label1.set_zorder(100)
		tick.label2.set_zorder(100)
	"""



def draw_arrowheads(fig,ax, top=True, right=True):
	"""
	Try to draw arrow heads on the axes.  Doesn not work super well yet.

	mutation_scale -> in units of points, default is plot fontsize

	https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.ArrowStyle.html#:~:text=The%20scale%20of%20the%20brackets.%20arrow%20%3D,filled%20triangle%20head%20at%20the%20end.%20Parameters%3A

	For the arrow types -|> and ->
	head_length = 0.4
	head_width = 0.2
	(in units of pts, scaled by mutation scale)
	"""

	xmin, xmax = ax.get_xlim()
	ymin, ymax = ax.get_ylim()

	"""
	# check the line width of the spines
	spine_width = ax.spines["bottom"].get_linewidth()
	"""

	mutation_scale = 9 # units of pts

	# a nub clips through the arrow head --> have to clip the axes a little short

	# Add dynamic arrows, based on fig size
	arrow_len = mutation_scale * 0.4

	xdiff, ydiff = convert_display_to_data(fig,ax, arrow_len/2) # <-- convert arrow_len (pts) to x&y data
	print("WARNING: cannot adjust figure (width,height) after drawing axis arrow heads.\n")

	# set up the arrow properties
	arrow_props = dict(arrowstyle="-|>", color=LATEX_BLACK, lw=0, shrinkA=0, shrinkB=0, mutation_scale=mutation_scale)

	if right:
		# stop the spine x% short of the max limit
		ax.spines["bottom"].set_bounds(xmin, xmax - xdiff)
		# add arrows to the axes
		ax.annotate('', xy=(xmax, 0), xytext=(xmax-xdiff, 0), arrowprops=arrow_props)

	if top:
		ax.spines["left"].set_bounds(ymin, ymax - ydiff)
		ax.annotate('', xy=(0, ymax), xytext=(0, ymax-ydiff),arrowprops=arrow_props)


	# xy -> controls the position of the tip of the arrow head
	# xytext relative to xy -> controls the direction of the arrow head
	#ax.annotate('', xy=(xmax, 0), xytext=(xmax-1.8, 0), arrowprops=arrow_props)
	#ax.annotate('', xy=(0, ymax), xytext=(0, ymax-1.8),arrowprops=arrow_props)
	#ax.annotate('', xy=(xmax+0.1, 0), xytext=(xmax-0.2, 0), arrowprops=dict(arrowstyle="->", color=LATEX_BLACK, lw=spine_width, shrinkA=0, shrinkB=0) )
	#ax.annotate('', xy=(0, ymax+0.1), xytext=(0, ymax-0.2),arrowprops=dict(arrowstyle="->", color=LATEX_BLACK, lw=spine_width, shrinkA=0, shrinkB=0) )

	# experimenting with arrows...
	#ax.text(0, ymin, r'$\downarrow$',fontsize=14, ha='center', va='center', color='black')
	return






def adjust_fig_height(fig,ax,axis_ratio=207/240, type='length'):
	"""
	This function sets the axis box to be adjustable rather than data limit.
	And assumes that the x & y limits have already been set.

	Update the figure height to match a certain ratio, 
	and do not change the figure width (need to be predifined).

	Parameters:
	- fig: matplotlib Figure
	- ax: matplotlib Axes
	- axis_ratio: desired axes box aspect ratio (height / width) --> default is pgfplots ratio
	- type:
	  - 'length': the axis_ratio is for the length of the axes
	  - 'data':  the axis_ratio is for the units of data (the axes may have padding so not equal data length)

	Returns:
	-  the updated figure (width,height)

	NOTE:
	- naive option is to do instead:  ax.set_aspect(aspect=axis_ratio, adjustable='box')
	- however, if the fig width and height is already set then
		- this just add extra whitespace around the axis to make it fit
	- instead, this function changes the height to make the figure the right ratio.

	- below, ax.set_aspect(aspect=axis_ratio, adjustable='box')
	- would also work, but as a bug it adds unnecessary white space around the axis.


	The default pdf plots setting is:
	- width (\axisdefaultwidth): 240pt
	- height (\axisdefaultheight): 207pt

	This gives a default axis ratio 207/240
	"""

	if type=='length':
		pass

	elif type=='data':
		# find the length of the axis in data units
		xmin, xmax = ax.get_xlim()
		ymin, ymax = ax.get_ylim()
		x_len = xmax-xmin
		y_len = ymax-ymin
		data_ratio = y_len/x_len
		# update the axis ratio
		axis_ratio = data_ratio * axis_ratio

	else:
		raise ValueError(f"Unknown formatting type '{type}'.")


	# make the axis adjustable
	ax.set_aspect('auto', adjustable='box')

	# draw the figure
	fig.canvas.draw()
	# find the current width & height
	fig_width, cur_fig_height = fig.get_size_inches()

	# find the axis position in the figure --> reutrn Bbox object
	ax_box = ax.get_position()
	# find the current width of the axis (inches) using the scale of the box width (between 0 & 1)
	ax_width = ax_box.width * fig_width

	# new height
	new_ax_height = ax_width * axis_ratio

	# determine the existing padding
	vpad = cur_fig_height * (1-ax_box.height)

	new_fig_height = new_ax_height + vpad

	# reset the figure size
	fig.set_size_inches(fig_width, new_fig_height)
	return fig_width, new_fig_height






# NO DONT USE THIS.  BETTER TO USE:  axes.Axes.set_aspect(...)
"""
def get_axes_ratio(ratio, style):
	Want a 'ratio' between the y:x axes.
	Have x,y ticks and labels.
	Use this to find the ratio of height:width of the overall figure.

	--> this works in the opposite direction to matplotlibe
	--> but this how pgfplots calculate the figure size
	print("WARNING:  Assume no title is enabled.")

	if style=="centre":
		return ratio  # by default all info in the plot is contained within the bounds of the spines --> no padding

"""



def plot_open_pt(ax,x,y,markersize):
	ax.plot(x,y, color=LATEX_BLACK, marker='.', linestyle="None", markersize=markersize, zorder=10)
	ax.plot(x,y, color=LATEX_WHITE, marker='.', linestyle="None", markersize=markersize*0.5, zorder=11 )





def convert_display_to_data(fig,ax, len_pt):
	"""
	Convert from units of points (display coordinates) into data coordinates

	Assume that the data coordinates are in pixels.

	Use this as a template:
	https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html

	Definition:  1pt = 1/72 of an inch
	             DPI = pixels per inch
	             Thus:
	             pixels = (DPI/72)*pts
	"""
	inv = ax.transData.inverted()

	# convert points to pixels --> latex uses its own point system of 72.27
	pxls = (fig.dpi/72.27)*len_pt

	# convert the point & the origin 
	x,_ = inv.transform((pxls,0))
	x_origin,_ = inv.transform((0,0))

	# now repeat for y
	_,y = inv.transform((0,pxls))
	_,y_origin = inv.transform((0,0))

	# find the total delta x length
	return (x - x_origin, y - y_origin)



def cm_to_tex_pt(length):
	return length * 72.27 / 2.54

