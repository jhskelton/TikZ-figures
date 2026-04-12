# TikZ Figures


This is a collection of code used to preprocess data, so that it may be easily turned into TikZ graphics.

The present purpose of the code is:
1. Take a 2d curve, with enumerable points, and downsample it to a good approximation.
2. Compute contour curves of functions $$f(x,y)$$, and then downsample the curves.




### Downsampling

Vector graphics with many vertices are computationally expensive, slow down rendering, and cannot be processed with TikZ easily.  Instead, we can approximate the original shape by one with less vertices.  One method is to downsample and remove vertices.


The algorithm implemented to downsample is the Ramer–Douglas–Peucker algorithm.
See [wikipedia](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) or an [example demo](https://cartography-playground.gitlab.io/playgrounds/douglas-peucker-algorithm/). See [below](#rdp-algorithm) for a brief explanation.



#### Some applications

This code could be used to, for example,
- Take a high quality solution curve to an ODE (e.g. chaotic), and then downsample to one visually the same.
- Compute high quality contour curves, and then downsample.

If you have any other ideas or suggestions, please contact me.



#### About the example:

Key ideas to demonstrate in `example.py`:
- create surface $$z=z(x,y)$$
- Compute contours
- downsample the contour curves using the RDP algorithm
- compare, visually, the original and downsampled contours
- save the data to a csv file, ready for TikZ to process it

Please vary the `eps` variable to get tighter or more polygonal fits.

The code is easily modifiable to apply to any desired function $$f: R^2 \to R$$, with arbitrary level sets.





##### Importing to LaTeX

```
\documentclass[tikz]{standalone}

\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}
\begin{tikzpicture}
    \begin{axis}[
        view = {0}{90}, % look top down
        ];
            
        \addplot3[
        contour prepared,
        thick,
        smooth,
        tension=0.7,
        empty line=jump, % tells tikz that a blank line means a new curve/contour
        ] table[x=x, y=y, z=z, col sep=comma] {example.csv};
    \end{axis}
\end{tikzpicture}
\end{document}
```



#### Other ideas

- Suppose we know that a polygon $$P$$ represents a smooth curve.  We could interpolate $$P$$ using splines, and then 'downsample' the splines.  We should be able to find points that match the error tolerance.  But this would require a root finding algorithm.





<hr/>

### Algorithms


##### RDP Algorithm

To summarise, the algorithm works by:
- Fix an error parameter $$\varepsilon$$
- Take a `start` and `end` point, imagine a line connecting them
- Compute the perpendicular distance $$d$$ from the line to all other points, one by one
- Find the (first) point with the greatest distance, call this `mid`
- If there are no points with $$d>\varepsilon$$: return `[start, end]`
- Else: 
	- Split the curve into `C1=[start,...,mid]` and `C2=[mid,...,end]`, and repeat recursively!
	- Glue together the resultant curves (remove one `mid`), and return


<!--Return `RDP(C1)[:] + RDP(C2)[1:]`-->
