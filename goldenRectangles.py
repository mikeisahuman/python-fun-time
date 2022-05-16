## goldenRectangles
## by Mike Phillips, 6/12/2017
##
## for creating and drawing nested golden rectangles, and interpolating the spiral
## 

# get numerical and plotting tools
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# give plot/graphical options
BG = "k"    #.background color
STY = "b-"  #.style code (rectangles)
DEPTH = 12   #.number of rectangles to draw
SIZE = 8    #.figure size (inches[?])
BASE = [0., 0.] #.base point (i.e. origin)
L = 10      #.initial rectangle size (length) on axes
SPIRAL = True   #.choose whether to show the spiral
S_STY = "y."    #.style code (spiral points)

# define the golden ratio
phi = (1+ (5**(0.5)) )/2

# lists for vertices of rectangle (ordered clockwise)
base = np.array(BASE)  #.base point of rectangle (lower-left corner)
width = L*phi           #.width of initial rectangle
height = L              #.height of initial rectangle
x = base[0] + width * np.array([0, 0, 1, 1, 0])
y = base[1] + height * np.array([0, 1, 1, 0, 0])

# initialization list of (x,y) points associated with the spiral
spiral = np.zeros((DEPTH + 1, 2))
spiral[0] = base.copy()     #.first (zeroth) spiral point is the initial base point

# define figure and axes
spillover = L / (phi ** 5)  #.spillover amount (image padding)
fig = plt.figure("Golden Rectangles : depth %i" % DEPTH, (SIZE, SIZE), facecolor = BG)
ax = fig.add_subplot(111, facecolor = BG, aspect = "equal")
ax.set_xlim( np.min(x) - spillover, np.max(x) + spillover )
ax.set_ylim( np.min(y) - spillover, np.max(y) + spillover )

# plot initial rectangle
ax.plot(x, y, STY)

# square off the rectangle repeatedly, and plot
mode = "right"   #.rectangle mode - cycle through the directions to make the spiral pattern
for rect in range(1, DEPTH + 1) :
    if mode == "right" :
        sqline_x = ( base[0] + height ) * np.ones(2)    #.pair of x-points for new line
        sqline_y = base[1] + np.array([0, height])      #.pair of y-points for new line
        width = width - height                          #.new rectangle dimension (width or height)
        base[0] += height                               #.shift the base point (if needed)
        mode = "bottom"                                 #.switch mode to the next one
    elif mode == "bottom" :
        sqline_x = base[0] + np.array([0, width])
        sqline_y = ( base[1] + (height - width) ) * np.ones(2)
        height = height - width
        #base stays the same
        mode = "left"
    elif mode == "left" :
        sqline_x = ( base[0] + (width - height) ) * np.ones(2)
        sqline_y = base[1] + np.array([height, 0])
        width = width - height
        #base stays the same
        mode = "top"
    elif mode == "top" :
        sqline_x = base[0] + np.array([width, 0])
        sqline_y = ( base[1] + width ) * np.ones(2)
        height = height - width
        base[1] += width
        mode = "right"
    else :
        print("\n\tSOMETHING WENT WRONG!!\n\n")
        break
    spiral[rect] = np.array([sqline_x[1], sqline_y[1]])     #.add a point to the spiral
    ax.plot(sqline_x, sqline_y, STY)            #.plot the new line


# plot & show the figure with the spiral (if desired)
if SPIRAL :
    spiral = spiral.transpose()
    spiral_x, spiral_y = spiral[0,:], spiral[1,:]
    tck, u = interpolate.splprep([spiral_x,spiral_y], k = 4, s = 0 )
    unew = np.arange( np.min(u), np.max(u), (np.max(u)-np.min(u))/200 )
    spiral_out = interpolate.splev(unew, tck)
    ax.plot(spiral_x, spiral_y, S_STY, spiral_out[0], spiral_out[1], "y-")
    
plt.show()

# clear out unused namespaces!
del plt, np, interpolate
