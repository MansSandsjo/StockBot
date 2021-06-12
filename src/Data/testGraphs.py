#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 14:10:45 2021

@author: manssandsjo
"""
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

lstm_lw = pd.read_pickle('./pickle_graphs/totValueLSTM_LW.pkl') #.to_numpy()
lstm_scm = pd.read_pickle('./pickle_graphs/totValueLSTM_SCM.pkl') #.to_numpy()
sma_scm = pd.read_pickle('./pickle_graphs/totValueSMA_SCM.pkl') #.to_numpy()

df = pd.DataFrame(columns=['SMA_SCM','LSTM_LW','LSTM_SCM'])

df['LSTM_LW'] = lstm_lw.iloc[:,0]
df['LSTM_SCM'] = lstm_scm.iloc[:,0]
df['SMA_SCM'] = sma_scm.iloc[:,0]


color = ['red', 'green', 'blue']
fig = plt.figure()
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Total value of portfolio, SEK')
plt.xlabel('Year')

def buildmebarchart(i=int):
    plt.legend(df.columns)
    p = plt.plot(df[:i].index, df[:i].values) #note it only returns the dataset, up to the point i
    for i in range(0,3):
        p[i].set_color(color[i]) #set the colour of each curve

        

anim = ani.FuncAnimation(fig, buildmebarchart, interval = 100)

from matplotlib import rc

# equivalent to rcParams['animation.html'] = 'html5'
rc('animation', html='html5')
anim