### by Michael Phillips, 1/12/2019
### "Coin-Tossing" simulation for distribution of number of successes,
### given uniform distribution at each opportunity for success.

import numpy as np
import matplotlib.pyplot as plt

p = 1/6         # define probability for success (between 0 and 1)
p0 = 1 - p      # probability for failure is: 1-(success)
N = 100          # number of trials/opportunities (or participants in a single trial)
Nsets = 1000       # number of sets of trials (or participants in multiple trials)

# define random attempt ("flip" or "roll") function
attempt = np.random.rand

# generate list of N random outcomes, count number of successes (n), repeat for Nsets "seasons"/sets of trials
outcomes = []
for s in range(Nsets):
    trials = [0] * N
    for j in range(N):
        if attempt() < p:
            trials[j] = 1
    outcomes.append(trials.count(1))     # record number of successes for this set of trials, then repeat

# theoretical prediction: probability to see n successes out of N trials, for any set of Nsets trials
#   generic probability for two outcomes in n trials
def P(n):
    return ( A(n) * (p**n) * (p0**(N-n)) )
#   factorial function for multiplicity calculation
def fac(x, x0=1):
##    if type(x) != int or type(x0) != int:
##        print("\n\tERROR: must use integer values in factorials.\n")
##        return
    x, x0 = int(x), int(x0)
    if x == x0 or x == x0-1:
        return x0
    elif x < x0:
        print("\n\tERROR: starting value x should be larger than x0.\t" +
              "(given: x=%i, x0=%i\n" % (x, x0))
        return
    else:
        return ( x * fac(x-1, x0) )
#   multiplicity function for counting number of arrangements for each number of successes
def A(n):
    return ( fac(N, N-n+1) / fac(n) )

# analyze results: theoretical plot vs. observed distribution (histrogram)
SIZE = 7            # figure size
BG = 'w'            # background color code
STY = 'b-'          # theoretical line color code
hist_STY = 'g'      # histogram style color code
mn_STY = 'g-.'       # style code for mean lines
std_STY = 'r--'     # style code for std. dev. lines
##bins = "auto"
bins = N
##bins = 6

nlist = np.array(range(N+1))
plist = np.array([ Nsets*P(n) for n in nlist ])
fig = plt.figure("%i 'Coin Tosses', with heads occurring at probability %1.2f" % (N,p),
                 (int(SIZE*1.2), SIZE), facecolor = BG)
ax = fig.add_subplot(111, facecolor=BG)
ax.set_title("Simulation vs. Theoretical distribution (max successes in sim: %i)" % max(outcomes))
(counts, bins, patches) = ax.hist(outcomes, bins, color=hist_STY, label="simulation")
ax.plot(nlist, plist, STY, label="theory")
ax.set_xlabel("n: number of successes")
ax.set_ylabel("N P(n): number of occurrences after N attempts")
xstep = 1 + (N // 20)
plt.xticks(range(0, N+1, xstep))
ymax = int(np.amax([np.amax(counts), Nsets*P(int(p*N))]))+1
ymax = int(1.1*ymax)
ax.set_ylim(0, ymax)
ystep = 1 + (ymax // 20)
plt.yticks(range(0, ymax, ystep))
ax.grid(True)
ax.legend(loc="upper left", edgecolor="inherit")
#ax.legend((line, hist), ("theory", "simulation"), loc="upper left", edgecolor="inherit")
fig.tight_layout()
plt.show()

# end
plt.close()

del np, plt

