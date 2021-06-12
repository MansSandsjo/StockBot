#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 13:37:35 2021

@author: manssandsjo
"""
import os
import numpy as np
import pandas as pd
import pickle

os.chdir(os.path.pardir)
#import sys
## insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '/Data')
os.chdir('Data')
import investPyData as omxs30
Rpd, N = omxs30.import_omxs30() # N number of stocks, R return between two days

T = len(Rpd)
R=Rpd.to_numpy()
print(T/252)


## Train LSTM-model
from keras.models import Sequential # init neural netW
from keras.layers import Dense # adding densly connected neural network
from keras.layers import LSTM # Long short term memory
from keras.layers import Dropout # prevent overfitting with dropout layers
from keras import backend as back

from sklearn.preprocessing import MinMaxScaler

def teachLSTM(stock):
    R1 = Rpd.iloc[:,stock]
    predDays = 1
    #clear old session to avoid clutter from old models/layers
    back.clear_session()
    #train model from 2010-01-07 – 2016-01-01
    #validate model from 2016-01-01 – 2018-01-01
    #test model from 2018-01-01 – 2021-01-01
    
    #investpy bug, will not give us data to 2016 so deleting 2 years from the 2018 data here
    trYrs = len(R1)-2*252;
    df_train = R1[0:trYrs].to_numpy()
    df_train = df_train.reshape(-1,1)
    #scale data for performance

    sc = MinMaxScaler(feature_range = (0, 1))
    df_train_scaled = sc.fit_transform(df_train)
    
    #creating 3D array
    x_train, y_train = [], []

    # prepare the dataset with predDay timesteps:
    for i in range(predDays, trYrs): 
        x_train.append(df_train_scaled[i-predDays:i, 0])
        y_train.append(df_train_scaled[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # built model
    # create and fit the LSTM network
    # Sequential– a plain stack of layers where each layer has exactly one input tensor and one output tensor
    model = Sequential()
    # units = 50 – dimensionality of output space

    #adding 2 hidden layers 50,50 and 25 neurons 
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.5))
    model.add(LSTM(units = 50, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(units = 25))
    
    model.add(Dense(units = 1))
#    The output layer consists of one single neuron, because only one output 
#   value at each time is used to forecast in time series problems such as this one.

    model.compile(loss='mean_squared_error', optimizer='adam')
    # slice data into batch size 32 for training
    # iterate over 20 periods 
    model.fit(x_train, y_train, epochs=100)
    
    return model, sc


    
#save all models in keras_models and differentiate them with number 0-29
i=0
for stock in range(N):
    model, sc = teachLSTM(stock)
    model.save('keras_models/model_2010_2016_'+str(i))
#    save min max scaler to be able to transform the data for prediction
    with open("scaler.pkl"+str(i), "wb") as outfile:
        pickle.dump(sc, outfile)
    del sc
    i=i+1


