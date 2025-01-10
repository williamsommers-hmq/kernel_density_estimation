#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 16:45:50 2024

@author: williamsommers
"""


import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(444)
np.set_printoptions(precision=2)  # Output decimal fmt.
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 100)      # Set the display width


# Synthesized simulated current over the motor life
# Amplitude - 
# Frequency - hertz or cycles/s (Hz)
# Dampen = dampening facotr 
# time= linear spaced time series 
# N= standard gaussian noise
# A= nominal amperage range of mixer motor at 20 HP (sinusoidal) ~28A
#
# Components of simulated motor performance and decay:
#
#   S0= base exponential decay carrier over the simulated motor life
#   S1= base sinusoidal operating current nominal 
#   FI1= fault injection - impulse at failure time 1
#   FI2= fault injection - impulse train at failure time 2
#   TC = total current:  S0 + S1 + S2 + N

time_span = 100         # number of seconds
Amplitude = 28
Noise_scale = Amplitude / 2.1
Frequency = 60
Nyquist   = Frequency * 2
Gen_scale = Nyquist * 16
Dampen = 0.8
numsamples = time_span * Gen_scale
# time = np.linspace(1, numsamples, num=int(Frequency * time_span))
time = np.arange(0,time_span, 1/Gen_scale )


N = np.random.uniform(low=-Noise_scale, high=Noise_scale, size=(numsamples,))  # noise

#A = np.random.weibull(10., numsamples)  # amperage 

S0 = np.exp( -Dampen * time) 
#S1 = np.sin(2 * np.pi * Frequency * time)
S1 = Amplitude * np.sin(2 * np.pi * Frequency * time)
FI1 = np.zeros_like(time)
FI2 = np.zeros_like(time)
Max = np.full(numsamples, Amplitude)
Min = np.full(numsamples, -Amplitude)


print(time.shape)
print(N.shape)
#print(A.shape)
print(S0.shape)
print(S1.shape)
print(FI1.shape)
print(FI2.shape)

print(time)
print(S0)

# build the data frame
dfC = pd.DataFrame()
dfC['time'] = time
dfC['N'] = N
#dfC['A'] = A
dfC['S0'] = S0
dfC['S1'] = S1
dfC['FI1'] = FI1
dfC['FI2'] = FI2
dfC['Min'] = Min
dfC['Max'] = Max
#dfC['signal'] = Amplitude * S0 * S1 + FI1 + FI2 + N

dfC['signal'] = S1 + N

print(dfC.head(50))
print(dfC.describe(include='all'))


print('writing output motor_data.csv')

filepath = Path('motor_data.csv')  
dfC.to_csv(filepath, index=False)  

