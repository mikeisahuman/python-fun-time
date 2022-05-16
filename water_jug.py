##  Water leaving a jug: open vs. closed
##      Michael Phillips, 8/15/2019 ; edited 6/27/2021

import numpy as np
import matplotlib.pyplot as plt

# important constants (cgs)
g = 980         # gravitational accel.
A0 = 8*16       # area of container
H = 12          # height of container
rho = 1         # density of water
R = 70          # 'resistance' ~ (length)*(viscosity)/r^4
P0 = 1e5        # 1/10 atmospheric pressure  [dyne/cm^2]

# for calculation
N = 500         # number of points to sample
tmax = 30       # maximum time
h0 = H/2        # starting height of water (h0 < H)

# no lid: pressure difference is just water's weight, rho*g*h
t = np.linspace(0, tmax, N) # linear time-space
lam = rho*g/(A0*R)          # inverse characteristic time, lam=1/tau
h_op = h0 * np.exp(-lam*t)  # height function for open jug case

# lid: pressure drops inside the closed container due to isothermal expansion, following ideal gas law
P0p = P0                    # beginning pressure in the container, at h=h0
alpha = P0 * A0 * (H - h0)  # alpha = N*k*T (constant if the container is closed, etc.)
shift = P0/(rho*g)          # variable shift

h0p = h0 - shift            # each variable shifted
Hp = H - shift              #

beta = np.sqrt( alpha/(A0*rho*g) + (Hp**2)/4 )      # useful def.

hmin = Hp/2 - beta + shift  # asymptotic value of h (the minimum value)

h = hmin + (h0 - hmin)*np.exp(-10*lam*t)   # exponential scale for height values on the interval [hmin, h0]
hp = h - shift             # shifted heights
#   two integrals
S1 = 0.5 * np.log(np.abs( ( (hp-Hp/2)**2 - beta**2 )/( (h0p-Hp/2)**2 - beta**2 ) ))
S2 = ( Hp/(4*beta) ) * ( np.log(np.abs( (hp - Hp/2 - beta)/(h0p - Hp/2 - beta) )) -
                         np.log(np.abs( (hp - Hp/2 + beta)/(h0p - Hp/2 + beta) )) )
#   #
t_cl = (-1/lam) * (S1 - S2)    # new time-points of closed case arise from the difference in integrals

print("h asymptote: %2.2f" % (hmin) )

# find time constants
#   open case
h_th = h0/np.e      # threshold value for time constant
ind = 0             # starting index value
while (h_op[ind] > h_th) and (ind < (len(h_op)-1)):
    ind += 1        # increment index, stop when threshold reached (or just passed)
tau_op = t[ind]     # characteristic time is the corresponding value
#   closed case
h_th = hmin + (h0 - hmin)/np.e
ind = 0
while (h[ind] > h_th) and (ind < (len(h)-1)):
    ind += 1
tau_cl = t_cl[ind]

# plots
title = "Comparison of Open vs. Closed Jug"
ht, wd = 6, 6
BG = "w"
openSTY = "b.-"
tColor = "darkcyan"
closeSTY = "r.-"
tclColor = "magenta"
asymCOL = "darkred"
mksize = 0
ymax = h0+1
xmax = 10

fig = plt.figure(title, (ht, wd), facecolor=BG)
ax = fig.add_subplot(111, facecolor=BG)
ax.set_title("Open vs. Closed Jug")
ax.plot(t, h_op, openSTY, markersize = mksize, label="open")
ax.plot([tau_op, tau_op], [0, H], color = tColor, linestyle = "dashed", label = r"$\tau$")
ax.plot(t_cl, h, closeSTY, markersize = mksize, label="closed")
ax.plot([tau_cl, tau_cl], [0, H], color = tclColor, linestyle = "dashed", label = r"$\tau_{eff}$")
ax.plot(t, hmin*np.ones(N), color = asymCOL, linestyle = "dotted", markersize = 0)
plt.text(-0.6, 0.99*hmin, "%2.2f" % (hmin), color = asymCOL)
plt.text(0.97*tau_op, 1.8, "%2.2f" % (tau_op), color = tColor)
plt.text(0.7*tau_cl, 1.8, "%2.2f" % (tau_cl), color = tclColor)
ax.legend(loc="upper right", edgecolor="inherit")
ax.set_xlabel("time (s)")
ax.set_ylabel("height (cm)")
ax.set_ylim(2,ymax)
ax.set_xlim(0,xmax)

ax.grid(True)
fig.tight_layout()
plt.show()

# done
plt.close()

del np, plt
