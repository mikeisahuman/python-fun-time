##  Michael Phillips, 8/25/2019
##  adding separate waves to see beats, etc.


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# make list of triplets: (amp, freq, phase)
N = 6                   # number of strings/channels
##allpars = [ [1, 100, 0] for i in range(N) ]
allpars = [ (1, 220, 0), (1, 330, 0), (1, 440, 0), (1, 275, 0), (1, 385, 0), (1, 495, 0) ]

# make waves
tmax = 0.025             # maximum time (seconds)
Nsamp = 400             # number of time-steps to reach tmax
t = np.linspace(0, tmax, Nsamp)
waves = []
total = np.zeros(Nsamp)
for i in range(N):
    awave = allpars[i][0] * np.sin(2*np.pi*allpars[i][1]*t + allpars[i][2])
    waves.append( awave )
    total += awave

# plot
HEIGHT = 7.5
WIDTH = 12
BG = "w"
STY = "b-"
manySTY = ["b-", "r-", "g-", "c-", "m-", "k-"]

fig = plt.figure("Adding Waves", (WIDTH, HEIGHT), facecolor = BG)
gs = gridspec.GridSpec(N, 4)
for i in range(N):
    ax = fig.add_subplot( gs[i, 0] )
    ax.plot(t, waves[i], manySTY[i])
    ax.grid(True)
ax = fig.add_subplot( gs[:, 1:] )
ax.plot(t, total, STY)
ax.grid(True)

fig.tight_layout()
plt.show()

plt.close()

del np, plt, gridspec
