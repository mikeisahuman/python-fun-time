##  Mike Phillips, 07/03/2021
##  Work to emulate results of: Ben-Naim & Redner, "Dynamics of Social Diversity"
##  Master Equation framework, using discrete 'fitness' k and time t (both bounded at 0)
##  Main equations: f(k)=F(k)-F(k-1) , dF(k)/dt = r*(F(k+1)-F(k)) - s*F(k)*(F(k)-F(k-1))
##  Initial condition used in paper: f(k)=delta(k,0) , F(k)=1 for all k>=0


import numpy as np
##import random as rn
import matplotlib.pyplot as plt
##from matplotlib import cm
from matplotlib.widgets import Slider, Button


def exactf(Del=1,k=1,t=0,s=1,r=1/2,pm=-1,fvt0=0):
    if t==0:
        return fvt0[k]
    kmin = - r*t - Del
    kmax = (s - r)*t + Del
    ks = (s/2 - r)*t
    def sqt(eta=1):
        sq = (Del**4)*(s*t)**2 + 2*(Del*s*t)**3 + (1-eta)*(Del**2)*(s*t)**4
        sq += 2*eta*(k+r*t)*(Del**2)*(s*t)**3
        return sq
    if k <= kmin or k > kmax:
        return 0
    elif k > kmin and k <= ks:
        return ( 1/(s*t) + pm * (Del**2)/((sqt(1))**(0.5)) )
    elif k > ks and k <= kmax:
        return ( 1/(s*t) + pm * (Del**2)/((sqt(-1))**(0.5)) )
    else:
        print("\n\t*** What just happened? ***\n\n")
        return -1
     

def evaluate(Kmax=100, Tmax=100, s=1, r=1/2, deltat=0.5,
             lottery=False, u=1/4, p=1/10, sf=False, ds=0.5, lam=1, ksat=False, avKmax_frac=0.50):
    # model parameters - rate of decline, r; rate of competition, s
##    s = 1
##    r = s/2
##    print("(s=%2.1f, r=%2.1f)" % (s, r))
    avKmax = avKmax_frac * Kmax   # saturation of fitness: some fraction of maximum in list
    def sfunc(k,t):   # if competition rate is a function of fitness and/or time
        if sf:
            return ( (s-ds) + ds * np.tanh(lam*k) )     # arbitary function of fitness
        elif ksat:
            return ( s * (1 - avK(t)/avKmax) )  # fitness saturation model: avg. k, fcn. of t, reaches max.
        else:
            return s

##    Kmax = 100      # maximum fitness in list
    klist = np.array(range(0, Kmax+1))         # fitness list
##    Tmax = 100      # maximum time
    time = np.linspace(0, Tmax, Tmax/deltat+1)      # time list

    # initial vectors: f, F, dF ;  indexed directly by fitness k
    dF = np.zeros(Kmax+1)
    f = dF.copy()
    f[0] = 1
##    f[10:20] = 1/10
    F = np.ones(Kmax+1)
##    F[0:10] = 0
##    F[10:20] = (1/10)*np.array(range(1,11))

    # initialize arrays for time steps ;  indexed directly by time t
    fvt = [f.copy()]
    Fvt = [F.copy()]

    def avK(t):     # calculate average fitness, for saturation model, or just additional info
        this_f = fvt[list(time).index(t)-1]
        avg = sum( [k*this_f[k] for k in klist] )
##        print("\n\t\tAVG K = %i \n" % avg)
        return avg

    # build vectors for k space, repeat for time space (t > 0)
    for t in time[1:]:
        if ksat:
            s_eff = sfunc(0,t)
        elif (not ksat) and (not sf):
            s_eff = sfunc(0,0)
        for k in range(Kmax+1):
            if sf and (not ksat):
                s_eff = sfunc(k,0)
            if k == 0:
                Fneg = 0
            else:
                Fneg = F[k-1]
            if k < 2:
                Flneg = F[0]
            else:
                Flneg = F[k-2]
            if k == Kmax:
                Fbig = F[k]
            else:
                Fbig = F[k+1]
            dF[k] = ( r*( Fbig - F[k] ) - s_eff*F[k]*( F[k] - Fneg ) ) * deltat
            if lottery:
                dF[k] += ( u*( (Fbig - F[k]) - p*(Fbig - Flneg) ) ) * deltat
            F[k] += dF[k]
            if k == 0:
                f[k] = F[k]
            else:
                f[k] = F[k] - F[k-1]
        fvt += [f.copy()]
        Fvt += [F.copy()]
    return (klist, fvt, Fvt, time, sfunc)


def plot(klist=[], fvt=[[]], Fvt=[[]], s=1, r=1, tlist=[], C=100, Del=1):
##    print("(s=%2.1f, r=%2.1f)" % (s, r))
##    (klist, fvt, Fvt) = evaluate(Kmax, Tsteps, s, r)
    size = 7.5
    bg = "w"
    fsize = 14
    axcolor = 'lightgoldenrodyellow'
    Tsteps = len(fvt) - 1
    atime = 0
    logymin = 1e-8

    def avK(t):     # calculate average fitness, for saturation model, or just additional info
        this_f = fvt[list(tlist).index(t)]
        avg = sum( [k*this_f[k] for k in klist] )
##        print("\n\t\tAVG K = %i \n" % avg)
        return avg


##    C = 200
    kones = np.ones(len(klist))
    def plateau(t):
        if C == 0 and t == 0:
            return kones
        else:
            return ( (1/(C+s*t)) * kones )
    def Fline(t):
        if C == 0 and t == 0:
            return ( (r/s) + klist )
        else:
            return ( (r/s) + klist/(C+s*t) )

##    def myf(time):
##        return ([exactf(k=ka,t=time,Del=Del,fvt0=fvt[0],s=s,r=r,pm=1) for ka in list(klist)])

    fig = plt.figure("Social Heirarchy", figsize=(size,size))
    ax1 = fig.add_subplot(211, facecolor=bg)
    line1,line1c,line1avg, = ax1.semilogy(klist, fvt[atime], "b+-", klist, plateau(atime), "g--",
                                [avK(atime), avK(atime)], [0, 2], "c:")
                                # ,line1ex  <...>  klist, myf(0), "k:")
##     = ax1.semilogy([avK(atime), avK(atime)], [0, 2], "c:")
    ax1.set_title("distribution : t = %i (s=%2.2f, r=%2.2f)" % (atime, s, r), fontsize=fsize)
    ax1.set_xlabel("k")
    ax1.set_ylabel(r"$f_k$")
    ax1.set_ylim(logymin,1.1)
    ax1.grid(True)

    ax2 = fig.add_subplot(212, facecolor=bg)
    line2, line2c = ax2.plot(klist, Fvt[atime], "r+-", klist, Fline(0), "m--")
    ax2.set_title("cumulative : t = %i (s=%2.2f, r=%2.2f)" % (atime, s, r), fontsize=fsize)
    ax2.set_xlabel("k")
    ax2.set_ylabel(r"$F_k$")
    ax2.set_ylim(-0.1,1.1)
    ax2.grid(True)

    fig.tight_layout()

    ax_time = plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor)
    stime = Slider(ax_time, 'time', 0, max(tlist), valinit=atime, valstep=max(tlist)/Tsteps)

    def update(val):
        time = stime.val
        ind = list(tlist).index(round(time,1))
        line1.set_ydata(fvt[ind])
        line2.set_ydata(Fvt[ind])
        line1c.set_ydata(plateau(time))
##        line1ex.set_ydata(myf(time))
        line1avg.set_xdata([avK(time), avK(time)])
        line2c.set_ydata(Fline(time))
        ax1.set_ylim(logymin, max(fvt[ind])*1.1)
        fig.canvas.draw_idle()
    stime.on_changed(update)

    ax_reset = plt.axes([0.85, 0.01, 0.1, 0.04])
    button = Button(ax_reset, 'Reset', color=axcolor, hovercolor='0.975')

    def reset(event):
        stime.reset()
    button.on_clicked(reset)

    plt.show()
    plt.close()
    return

#del np, plt     #, rn, cm, Button
