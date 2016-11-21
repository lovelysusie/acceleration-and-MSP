# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 23:26:56 2016

@author: Susie
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import pandas as pd
from scipy.signal import butter,lfilter
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np



def butterBandPass(lowcut,highcut,fs,order=5):
    nyq = fs*0.5
    low = lowcut/nyq
    high = highcut/nyq
    b,a = butter(order,[low,high],btype='bandpass')
    return b,a

def butterBandPassFilter(data,lowcut,highcut,fs,order=5):
    b,a = butterBandPass(lowcut,highcut,fs,order=order)
    y = lfilter(b,a,data)
    return y


lowcut = 0.2
highcut = 4

Fs = 67*2

y = np.array([0.0888672,0.0961914,0.122314,0.134033,0.14502,0.14502,0.140137,0.134033,0.118408,0.105469,0.0905762,0.0947266,0.0986328,0.118896,0.136963,0.14209,0.140381,0.122559,0.119629,0.111328,0.100342,0.0908203,0.0922852,0.111084,0.139648,0.148193,0.151611,0.141113,0.131836,0.12207,0.107666,0.104004,0.0998535,0.10083,0.104248,0.116943,0.124756,0.125244,0.123779,0.120605,0.118652,0.111572,0.117676,0.121094,0.134766,0.145264,0.139893,0.128174,0.112305,0.11084,0.107666,0.104492,0.102051,0.0939941,0.101074,0.107422,0.131104,0.156006,0.161133,0.158691,0.145508,0.137695,0.117188,0.0974121,0.088623,0.0856934])

f1,accx = signal.periodogram(y,fs=Fs,scaling='density',return_onesided=True)

ax = butterBandPassFilter(y,lowcut,highcut,Fs,order=6)

# drawing the periodogram
f,gyX = signal.periodogram(ax,fs=Fs,scaling='density',return_onesided=True)
plt.subplot(211)
plt.plot(f1,accx)
plt.subplot(212)
plt.plot(f,gyX)
plt.show()