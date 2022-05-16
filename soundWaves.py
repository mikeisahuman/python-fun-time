### by Michael Phillips, 4/6/2019
### For 'listening' to and displaying sound waves.
### Sound is taken live from the microphone input.
### Waves are displayed directly (raw); also, a
### fourier transform (FFT) picks primary frequencies
### to display 'cleaner' waves, along with FFT peaks.

##import os
##import tkinter as tk
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
fft = np.fft.fft

##win1 = tk.Tk()    #(screenName="Loop Time")
##lab = Label(win1, text="\nEnter a number of 'seconds' to plot sound waves:\n\n")
##lab.pack()
##win1.mainloop()

Nfreq = 3       # number of primary frequencies to pick from FFT
fmin = 50       # minimum frequency to use/display in FFT
fmax = 45e3     # maximum frequency
famp = 3.0      # maximum amplitude on FFT output
wantLog = True  # take log of FFT output
wantAbs = True  # absolute value of FFT output
fftBins = 450   # number of ouput elements for fft

aTime = input("\nPlease enter a time (in 'seconds'):" + "\n\t")
print("\n")
aTime = float(aTime)  # custom max time to watch
processFactor = 10  # factor to convert input time to actual seconds (accounts for processing times)
aTime = aTime / processFactor

t = 0.02           # duration of each recording (seconds)
tmax = aTime    #10           # max total time to record & display live ("seconds")
imax = int(tmax/t)  # max number of record & display steps

fs = 48000      # sampling frequency (frames per second) -- 44100 or 48000
ffrac = fmax/fs     # fraction (of total points) to cut FFT spectrum [0.5 or less]
channels = 2    # number of channels
my_channel = 2  # selected channel to use
dur = int(t*fs) # duration of recording (frames)
amp = 0.20      # fixed maximum amplitude

SIZE = 7.5      # figure size
BG = 'k'        # background color code
rSTY = 'w-'     # style code for raw input
wSTY = 'b-'     # style code for clean waves
fSTY = 'g-'     # style code for fft
txtColor = 'white'
yperc = 1.08    # percentage of min/max for plotting

##sd.query_devices()          # get list of available audio devices (with channel info) 
##sd.default.device = [0,2]   # set default device(s): [input, output]
sd.default.samplerate = fs
sd.default.channels = 2

# set up figure and plots
plt.ion()
fig = plt.figure("Sound Waves", (int(SIZE*(1.5)), SIZE), facecolor = BG)
sz = "12"

# record & plot initial data
r = sd.rec(dur)
sd.wait()
r = [ dat[my_channel-1] for dat in r]
axr = fig.add_subplot(int(sz + "1"), facecolor = BG)#, aspect = "equal")
axr.set_title("raw\n", color=txtColor)
axr.set_xlim(0, dur)
##ax.set_ylim(yperc*min(r), yperc*max(r))
##ax.set_ylabel("signal", color=txtColor)
axr.set_ylim(yperc*amp, -yperc*amp)
axr.grid(True)
rLine, = axr.plot(r, rSTY)

# fourier transform
f = fft(r, n=fftBins).real
newlen = int(ffrac*len(f))
xf = np.linspace(fmin, ffrac*fs, newlen)
axf = fig.add_subplot(int(sz + "2"), facecolor = BG)#, aspect = "equal")
axf.set_title("fft\n", color=txtColor)
axf.set_xlim(min(xf), max(xf))
axf.xaxis.label.set_color(txtColor)
axf.tick_params(axis='x', colors=txtColor)
##ax.set_ylabel("signal", color=txtColor)
if wantAbs:
    axf.set_ylim(-(yperc-1)*famp, yperc*famp)
    func = np.abs
else:
    axf.set_ylim(-yperc*famp, yperc*famp)
    func = lambda x: x
axf.grid(True)
if wantLog:
    fLine, = axf.semilogx(xf, func(f[:newlen]), fSTY, basex=10)
else:
    fLine, = axf.plot(xf, func(f[:newlen]), fSTY)

##def recPlot(r, pos, sty, title="", ylbl="", grd=True, size="13"):
##    r = [ dat[my_channel-1] for dat in r]
##    ax = fig.add_subplot(int(size+str(pos)), facecolor = BG)#, aspect = "equal")
##    ax.set_title(title, color=txtColor)
####    ax.set_xlim(-0.5, len(terms)-0.5)
##    ax.set_xlim(0, len(r))
##    ax.set_ylim(yperc*min(r), yperc*max(r))
##    ax.set_ylabel(ylbl, color=txtColor)
##    ax.grid(grd)
##    ax.plot(r, sty)
##    print(max(r))
##    return

# loop and redraw
for i in range(imax):
    r = sd.rec(dur)
    sd.wait()
    r = [ dat[my_channel-1] for dat in r]
    rLine.set_ydata(r)
    f = fft(r).real
    fLine.set_ydata(func(f[:newlen]))
    fig.canvas.draw()
    fig.canvas.flush_events()

### show
##fig.tight_layout()
##plt.show()

# done
##print(i)
plt.close()

del plt, np, sd#, os
