## fractalTree
## by Mike Phillips, 6/17/2017
##
## for creating and drawing a simple fractal "tree"
## * features / options :
##      custom colors -- including 'leaves' and the depth where they begin
##      branches -- elementary number of branches at each point
##      depth -- total number of generations, i.e. number of branching repetitions
##      angle of separation -- total angle between outer branches (halved : relative to vertical)
##      random mode -- True/False to activate or not, and fractions for standard deviations of sampling
##      
## 

# get numerical and plotting tools
import numpy as np
import matplotlib.pyplot as plt

# give plot/graphical options
BG = "black"    #.background color
COLOR = "brown" #.color name / code (initial branches)
LEAF_COLOR = "green"    #.color name / code (later branches/leaves)
BRANCHES = 2    #.number of branches to draw from each branch endpoint (1,2,3 only for now)
DEPTH = 12      #.depth of branching points (initial trunk counts as branch zero)
LEAF_DEPTH = 6  #.depth at which to begin coloring as leaves
SIZE = 8        #.figure size (inches[?])
BASE = [0., 0.] #.base point (i.e. origin)
nextBASE = []   #.list of next base points (initialized empty - should not be modified)
nextANG = []    #.list of next base angles
ang_sep = 75/2  #.angle (degrees) of deviation for (outer) branches away from their base angles
RANDOM = True   #.choose whether or not to randomize branch lengths/angles
ang_rand , len_rand = 2/3 , 1/8     #.fractions governing the std.dev. of random sampling

# chosen function for randomizing branch lengths and angles (normal distribution)
def RandN(mean, stdev_frac = 1/3) :
    if RANDOM :
        shift_frac = stdev_frac * np.random.randn()
    else :
        shift_frac = 0
    return (mean * (1 + shift_frac))

# define the golden ratio
phi = (1+ (5**(0.5)) )/2

# convenient trig functions (taking degrees)
DEGtoRAD = np.pi/180  #.conversion from degrees (for trig)
def Sin(deg) :
    return np.sin(deg * DEGtoRAD)
def Cos(deg) :
    return np.cos(deg * DEGtoRAD)

# rotation function (clockwise rotation of a vector)
def Rotate(vec, deg) :
    rot = np.array([ [Cos(deg), Sin(deg)] , [-Sin(deg), Cos(deg)] ])
    return np.dot(rot, vec)

# base line (trunk)
ANGLE = 0                   #.initial angle of trunk (degrees clockwise from vertical)
LENGTH = phi**2             #.(initial) length of branches
unit = np.array([0,1])      #.unit vector (vertical) used for everything
vec = LENGTH * Rotate(unit, ANGLE)  #.inital vector of trunk (after rotation)
x = BASE[0] + np.array([0, vec[0]]) #.list of x-points for trunk
y = BASE[1] + np.array([0, vec[1]]) #.list of y-points for trunk
nextBASE.append([x[1], y[1]])       #.add the endpoint to the list of new base points
nextANG.append(ANGLE)               #.add the current angle to the list of new angles

# define figure and axes
yrng = 1.1 * (2*phi + 1)/(phi - 1)#.plot height scale (from geometric sum of [inverse] golden ratio)
xrng = yrng / phi           #.plot width scale (enough to contain tree)
spillover = phi/8           #.spillover amount (give tree base some space)
fig = plt.figure("Golden Fractal Tree : depth %i" % DEPTH, (SIZE, SIZE), facecolor = BG)
ax = fig.add_subplot(111, facecolor = BG, aspect = "equal")
ax.set_xlim( BASE[0] - xrng - spillover, BASE[0] + xrng + spillover )
ax.set_ylim( BASE[1] - spillover, BASE[1] + yrng + spillover )
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# plot initial line (trunk)
ax.plot(x, y, "-", color = COLOR)


# make list of angle deviations given the number of branches
GOOD_DEVS = True        #.track whether a good (safe) choice is made

if RANDOM :             #.use nonzero deviations if drawing randomly
    mid_angle = ang_sep/10
else :
    mid_angle = 0
    
if BRANCHES == 0 :      #.check for a good choice & set up list of deviations
    print("\nYou should probably draw at least one branch...")
    DEVS = [ ]
    GOOD_DEVS = False
elif BRANCHES == 1 :
    DEVS = [mid_angle]
elif BRANCHES == 2 :
    DEVS = [ang_sep, -ang_sep]
elif BRANCHES == 3 :
    DEVS = [ang_sep, mid_angle, -ang_sep]
else :
    print("\nYou should probably draw fewer branches...")
    DEVS = list(np.linspace(ang_sep, -ang_sep, BRANCHES))
    GOOD_DEVS = False

# kill the tree if choices are not good
if not GOOD_DEVS :
    COLOR = "red"
    eff_DEPTH = 1
else :
    eff_DEPTH = DEPTH

# loop for adding branches
for d in range(eff_DEPTH) :
    BASE = nextBASE     #.make base (list) equal to the collection of current endpoints
    nextBASE = []       #.reset the "next" list for upcoming endpoints
    ANGLE = nextANG     #.angle (list) equal to current angles
    nextANG = []        #.reset the "next" list for upcoming angles
    LENGTH = LENGTH / phi   #.rescale the branch length
    if d > LEAF_DEPTH and COLOR != LEAF_COLOR :
        COLOR = LEAF_COLOR
    for i in range(len(ANGLE)) :
        for dev in DEVS :
            l = abs(RandN(LENGTH, len_rand))   #.randomize the length of EACH branch
            base = BASE[i]
            angle = ANGLE[i] + RandN(dev, ang_rand) #.angle is shifted by randomized deviation
            vec = l * Rotate(unit, angle)
            x = base[0] + np.array([0, vec[0]])
            y = base[1] + np.array([0, vec[1]])
            nextBASE.append([x[1], y[1]])
            nextANG.append(angle)
            ax.plot(x, y, "-", color = COLOR)


# show the tree
plt.show()


# make sure any figure is closed
plt.close("all")

# function for counting branches, if interested
def branch_count(num=2, power=5) :
	s = 0
	f = 1
	mx = power + 1
	for p in range(0, mx) :
		s += f
		f *= num
		if p == power :
			print("\nup to " + str(num) + "^" + str(power),":")
	print("\ttotal number of branches =", s, "\n")

branch_count(len(DEVS), DEPTH)

# clear out namespaces
del plt, np
# clear out functions
del RandN, Sin, Cos, Rotate, branch_count
