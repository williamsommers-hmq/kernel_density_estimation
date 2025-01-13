#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:07:03 2024

@author: william.sommers
"""

# William Sommers
# HiveMQ Technical Account Manager (TAM)

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity


pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 100)      # Set the display width


# function to calcuate Interquartile Range (IQR)

def IQR(dist):
    return np.percentile(dist, 75) - np.percentile(dist, 25)

# calcualte the Freedman-Diaconis rule for histogram nubmer of bins
def FD(dist):
    return 2 * IQR(dist) * pow(length(dist), 1/3)
    
def signal_plot(df, title, x_axis, y_axis, start, end ):
    # plot a sample
    plt.figure(figsize=(20, 6), dpi=80)
    df.loc[start:end, y_axis].plot.line(x='time', y=y_axis)
    df.loc[start:end,'Min'].plot(x=x_axis, y='Min', linestyle = ':')
    df.loc[start:end,'Max'].plot(x=x_axis, y='Max', linestyle = ':')
    plt.title(title)
    plt.show()
    
def signal_multiplot(df, title, x_axis, y_axis, start, end, *other_y ):
    # plot a sample
    plt.figure(figsize=(20, 6), dpi=80)
    df.loc[start:end, y_axis].plot.line(x='time', y=y_axis)
    df.loc[start:end,'Min'].plot(x=x_axis, y='Min', linestyle = ':')
    df.loc[start:end,'Max'].plot(x=x_axis, y='Max', linestyle = ':')
    plt.title(title)
    
    num_args = len(other_y)
    print("Number of arguments:", num_args)
    for axis in other_y:
        print(axis)
        df.loc[start:end, y_axis].plot.line(x='time', y=axis)
    plt.show()


def histogram_plot(df, title, y_axis, start, end):
    df.loc[samp_start:samp_end, y_axis].plot.hist(column=y_axis)
    plt.title(title)
    plt.show()

# Sample ranges
samp_start = 3000
samp_end = 3120

# file
data_file = 'kde_motor_data.csv'

# read the data - replace this with MQTT data
df = pd.read_csv(data_file)
print(df.describe())
length = len(df)
print('Length = {}'.format(length))

S=np.array(list(df['signal'])).reshape(-1,1)
S1=np.array(list(df['S1'])).reshape(-1, 1)

# plot the histogram of the signal
# use Freedman-Diaconis rule for number of bins
bin_edges = np.histogram_bin_edges(S, bins='fd')
print('Bin edges = {}'.format(bin_edges))
plt.hist(S, bins=bin_edges)
plt.title('Histogram of signal (with Noise)')
plt.show()


#bin_edges2 = np.histogram_bin_edges(S1, bins='fd')
#print('Bin edges = {}'.format(bin_edges2))
#df.plot.hist(column='S1', bins=bin_edges)
df.plot.hist(column='S1')
#plt.hist(S1, bins=bin_edges)
plt.title('Histogram of signal (ideal)')
plt.show()

# print('Kernel Density Estimation')
# kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(S)
# print(kde.score_samples(S))

signal_plot(df, 'Motor Current Signal (representative)', 
            'time', 'signal', 5000, 6500)

signal_plot(df, 'Motor Current Signal (with noise)', 
            'time', 'signal', samp_start, samp_end)

signal_plot(df, 'Motor Current Signal2 (dampened with noise)', 
            'time', 'signal2', samp_start, samp_end)


signal_plot(df, 'Motor Current Signal (missing data with noise)', 
            'time', 'signal3', samp_start, samp_end)

signal_plot(df, 'Motor Current Signal (degraded signal with multi-spectrum noise)', 
            'time', 'signal4', samp_start, samp_end)

signal_plot(df, 'Motor Current Signal (degraded signal multi-spectrum)', 
            'time', 'S4', samp_start, samp_end)

signal_multiplot(df, 'Motor Current Signal (degraded signal multi-spectrum)', 
            'time', 'S4', samp_start, samp_end, 'S4_0', 'S4_1', 'S4_2', 'S4_3')

histogram_plot(df, 'Histogram of Primary Noise', 'N', samp_start, samp_end)
histogram_plot(df, 'Histogram of Secondary Noise', 'N2', samp_start, samp_end)

histogram_plot(df, 'Histogram of degraded signal with multi-spectrum noise',
               'signal4', samp_start, samp_end)

histogram_plot(df, 'Histogram of degraded signal multi-spectrum',
               'S4', samp_start, samp_end)

# plot histogram of dampened, noisy signal
df.loc[samp_start:samp_end, 'signal2'].plot.hist(column='signal2')
plt.title('Histogram of signal2 (dampened with noise)')
plt.show()


# plot histogram of signal3 missing data with noise
df.loc[samp_start:samp_end, 'signal3'].plot.hist(column='signal3')
plt.title('Histogram of signal3 (missing data with noise)')
plt.show()


# plot the noise (sample)
# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[samp_start:samp_end,'N'].plot.line(x='time', y='signal')
# plt.title('Noise')
# plt.show()

signal_plot(df, 'Noise', 
            'time', 'N', samp_start, samp_end)



# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[0:10000,'S0'].plot.line(x='time', y='S0')
# plt.title('Logrithmic decay component S0')
# plt.show()

signal_plot(df, 'Logrithmic decay component S0', 
            'time', 'S0', samp_start, samp_end)


# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[samp_start:3060,'S1'].plot.line(x='time', y='S1')
# plt.title('Pure sinusoidal signal S1')
# plt.show()

signal_plot(df, 'Pure sinusoidal signal S1', 
            'time', 'S1', samp_start, samp_end)


# plot pure sine wave with actual (overlay, not combined)
plt.figure(figsize=(20, 6), dpi=80)
df.loc[samp_start:samp_end,'signal'].plot.line(x='time', y='signal', label='Actual signal')
df.loc[samp_start:samp_end,'S1'].plot.line(x='time', y='S1', label='Pure sine wave')
df.loc[samp_start:samp_end,'Min'].plot(x='time', y='Min', linestyle = ':', label='Min')
df.loc[samp_start:samp_end,'Max'].plot(x='time', y='Max', linestyle = ':', label='Max')
plt.title('Motor Current Signal Sample (with Noise)')
plt.show()



# provide an array of ones (1) for the single-dimension trasformation
# ones = []
# for i in range(len(S)):
#     ones.append(1)



#sys.exit(0)

# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[5000:6500,'signal'].plot.line(x='time', y='signal')
# plt.title('Motor Current Signal (representative)')
# plt.show()

# plot a sample of the motor current signal
# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[samp_start:samp_end,'signal'].plot.line(x='time', y='signal')
# df.loc[samp_start:samp_end,'Min'].plot(x='time', y='Min', linestyle = ':')
# df.loc[samp_start:samp_end,'Max'].plot(x='time', y='Max', linestyle = ':')
# plt.title('Motor Current Signal Sample (with noise)')
# plt.show()

# plot a sample of the motor current signal2 (dampend with noise)
# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[samp_start:samp_end,'signal2'].plot.line(x='time', y='signal')
# df.loc[samp_start:samp_end,'Min'].plot(x='time', y='Min', linestyle = ':')
# df.loc[samp_start:samp_end,'Max'].plot(x='time', y='Max', linestyle = ':')
# plt.title('Motor Current Signal2 Sample (dampened with noise)')
# plt.show()

# plot a sample of the motor current signal3 (missing data w/noise)
# plt.figure(figsize=(20, 6), dpi=80)
# df.loc[samp_start:samp_end,'signal3'].plot.line(x='time', y='signal')
# df.loc[samp_start:samp_end,'Min'].plot(x='time', y='Min', linestyle = ':')
# df.loc[samp_start:samp_end,'Max'].plot(x='time', y='Max', linestyle = ':')
# plt.title('Motor Current Signal3 Sample (missing data with noise)')
# plt.show()
