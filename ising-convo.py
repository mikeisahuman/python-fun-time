##  Mike Phillips, 02/04/2020
##  A simulation of an Ising-like (voter-like) model of classroom conversations.
##  An M x N grid of individuals is used. At each time-step, every individual is assessed --
##  an individual will change their behavior state (speaking <-> silent) according to a
##  given probability function (dependent only on nearest-neighbors), generating a fully
##  new state vector. Square lattice interaction topology is assumed.
##
##  UPDATE: MODE="all" corresponds to the above; MODE="single" assesses a single (random) student
##  at each time-step, instead of the whole population at once.

import numpy as np
import random as rn
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Button

M = 5           # rows
N = 6           # columns
Ntot = M*N      # total number of individuals
Tsteps = 1500     # maximum number of time-steps
t = 0           # initialize time
eps = 0.02      # chance to stop talking, even when many are talking
eps2 = 0.01     # chance to begin talking, even when nobody around is talking

MODE = ["all", "single"][1]

grid = np.zeros((M,N), dtype=int)   # initialize grid of individual states
##change = np.zeros((M,N), dtype=int) # initialize grid of state-change values
##total = np.zeros(Tsteps+1, dtype=int) # initialize list of total number speaking
total = []

#   samples
##grid[0][0] = 1
grid[3][2] = 1
##grid[0][4] = 1

#   function for nearest-neighbors of individual (i,j)
##def nn(i,j):
##    if (i in [0,M-1]) and (j in [0,N-1]):   # corner
##        return 2
##    elif (i in [0,M-1]) or (j in [0,N-1]):  # edge
##        return 3
##    else:                               # bulk
##        return 4

#   function for nearest-neighbors of individual (i,j) , and their state total
def snn(i,j):
    if i==0 and j==0:
        n = 2           # corner
        s = grid[i][j+1]
        s += grid[i+1][j]
    elif i==M-1 and j==0:
        n = 2           # corner
        s = grid[i][j+1]
        s += grid[i-1][j]
    elif i==0 and j==N-1:
        n = 2           # corner
        s = grid[i][j-1]
        s += grid[i+1][j]
    elif i==M-1 and j==N-1:
        n = 2           # corner
        s = grid[i][j-1]
        s += grid[i-1][j]
    elif i==0:
        n = 3           # edge
        s = grid[i+1][j]
        for q in (1,-1):
            s += grid[i][j+q]
    elif i==M-1:
        n = 3           # edge
        s = grid[i-1][j]
        for q in (1,-1):
            s += grid[i][j+q]
    elif j==0:
        n = 3           # edge
        s = grid[i][j+1]
        for q in (1,-1):
            s += grid[i+q][j]
    elif j==N-1:
        n = 3           # edge
        s = grid[i][j-1]
        for q in (1,-1):
            s += grid[i+q][j]
    else:
        n = 4           # bulk
        s = 0
        for q in (1,-1):
            s += grid[i+q][j]
            s += grid[i][j+q]
    return (n,s)

#   define probability function for inidividual (i,j) changing behavior
def p(i,j):
    s = grid[i][j]
    (nn, stot) = snn(i,j)
    if stot==nn:
        dlt = 1
    else:
        dlt = 0
    fs = (stot - nn*dlt) / (nn - 1)
    if s==0:
##        return fs
        return ( (1-eps2)*fs + eps2*(1-dlt) )
    else:
        return ( (1-eps)*(1-fs) + eps )

#   button functions
def step_one(event):    # take a single step
    global t, total
    change = np.zeros((M,N), dtype=int) # initialize grid of state-change values
    if t < Tsteps:
        t += 1
        if MODE == "all":
            for i in range(M):
                for j in range(N):
                    if rn.random() < p(i,j):
                        change[i][j] = 1
            for i in range(M):
                for j in range(N):
                    if change[i][j]==1:
                        s = grid[i][j]
                        grid[i][j] = 1 - s
        elif MODE == "single":
            selected = round(rn.random()*(Ntot-1))  # selected random student number
            i = selected // N                   # row of selcte student
            j = selected % N                    # column of selected student
            if rn.random() < p(i,j):
                        s = grid[i][j]
                        grid[i][j] = 1 - s
        total += [np.sum(grid)]
        im.set_data(grid)
        ax.set_title(axtitle(t), fontsize=fsize)
        plt.draw()
    else:
        print("\n\tMaximum number of steps reached.\n")
def step_func(event, steps):
    global t
    q = 0
    qmax = steps
    while (q < qmax) and (t < Tsteps):
        q += 1
        step_one(event)
    if t == Tsteps:
        print("\n\tMaximum number of steps reached.\n")
def step_ten(event):
    step_func(event, 10)
def step_fifty(event):
    step_func(event, 50)
def step_hundy(event):
    step_func(event, 100)


size = 7.5
if N > M:
    width = size*N/M
    if width > 12:
        width = 11.5
bg = "w"
fsize = 15
fig = plt.figure("State Grid", figsize=(width,size), facecolor=bg)
ax = fig.add_subplot(111, facecolor=bg)
im = ax.imshow( grid , cmap=cm.binary, origin='lower', aspect='equal', vmin=0, vmax=1)

total += [np.sum(grid)]
axtitle = lambda t: ( "t = %i  ,  speaking = %i" % (t, total[t]) )
ax.set_title(axtitle(t), fontsize=fsize)

##cbar = plt.colorbar(im, format = "%1.1f", fraction=0.046, pad=0.04)   # magic colorbar numbers!
##cbar.ax.get_yaxis().labelpad = 12
##ax.set_xlabel("")
##ax.set_ylabel("")
ax.tick_params(bottom=False, top=False, left=False, right=False,
               labelbottom=False, labeltop=False, labelleft=False, labelright=False)

b1 = Button(plt.axes([0.85, 0.01, 0.14, 0.07]), "1 step", color="0.9", hovercolor="0.6")
b1.on_clicked(step_one)

b10 = Button(plt.axes([0.7, 0.01, 0.14, 0.07]), "10 steps", color="0.9", hovercolor="0.6")
b10.on_clicked(step_ten)

b50 = Button(plt.axes([0.55, 0.01, 0.14, 0.07]), "50 steps", color="0.9", hovercolor="0.6")
b50.on_clicked(step_fifty)

b100 = Button(plt.axes([0.4, 0.01, 0.14, 0.07]), "100 steps", color="0.9", hovercolor="0.6")
b100.on_clicked(step_hundy)

##fig.tight_layout()
plt.show()
plt.close()

##print("total speaking:\n", total, "\n")

fig2 = plt.figure("Total speaking", figsize=(size,size))
ax2 = fig2.add_subplot(111, facecolor=bg)
ax2.plot(range(len(total)), total, "b+-")
ax2.set_title("total number speaking at time-step t", fontsize=fsize)
ax2.set_xlabel("t")
ax2.set_ylabel("total")
ax2.grid(True)

fig2.tight_layout()
plt.show()
plt.close()

del np, plt, rn, cm, Button
