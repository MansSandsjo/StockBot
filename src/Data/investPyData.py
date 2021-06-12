import investpy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from array import *

def import_omxs30():
    
    OMXS30 = pd.read_csv("OMXS30.txt")
    stocks = OMXS30["ticker"].tolist()
    
    dfs = list()
    
    start_date='07/01/2018'
    end_date='01/01/2020'
    
    for stock in stocks:
       df = investpy.get_stock_historical_data(stock=stock,
                                               country='Sweden',
                                               from_date=start_date,
                                               to_date=end_date)
       dfs.append(df)
    
    for i in dfs:
        i.drop(['Currency','Open','High','Low','Volume'], axis=1, inplace=True)
        i.dropna(0,inplace=True)    
        i.reset_index(inplace=True)
    # Essity was part of SCA before 2017 – no data before 2017-03
    # delete Essity col.    
    del dfs[9]
    
    # Evolution Gaming was introduced to OMXS30 in 2015-03 – no data before that
    # delete Ev. Gaming col.
    del dfs[9]
    
    # counters for missing or wrong data    
    nbrs_15 = 0
    globalZeroindex = list()

    for stock in dfs:                                                      
        # make new col for the next day closing price
        stock['Close+1day'] = stock['Close'].shift(1)
        # calculate the fraction of the next day's closing price and this day
        stock['R'] = (stock['Close+1day']-stock['Close'])/stock['Close']
        
        # Count the instances of closeChange gt or lt 15%
        nbrs_15 += stock.R[(stock.R>.15) | (stock.R<(-.15))].count()
        # see if we have any missing values
    #        isnaCount += stock['Close'].isna().sum()
        globalZeroindex = stock[stock['R']==0].index.tolist()
        
        # Drop the values that are outside the range
        stock = stock.drop(stock[(stock.R>.15) | (stock.R<(-.15))].index)
        stock.drop(['Close', 'Close+1day'], axis = 1, inplace=True)
    
    #        dates = stock['Date'].to_numpy()
    #        priceChange = stock['closeChange'].to_numpy()
    #        plt.plot(dates, priceChange)
    #        R = R.append(stock)
        
    #    Drop all indexes where there are NaN values
    #    for stock in dfs:
        
    #    Drop all zero values of the return
    for stock in dfs:
        for dropInd in globalZeroindex:
            stock.drop(stock.index[dropInd],inplace=True)   
            
    dfs = [df.set_index('Date') for df in dfs]
    dfs = [df['R'] for df in dfs]
    final = pd.concat(dfs, axis=1)
    # be careful here, we remove the day where we have NaN
    
    final.dropna('index',inplace=True)
#    final = final[(final != 0).all(1)]
    final = final.reset_index() 
    final.drop(['Date'], axis = 1, inplace=True)
    N = len(final.columns)
    #first values are NaNs drop them
    final = final.iloc[1:]

    return final, N
#final, N = import_omxs30()
#dfs = import_omxs30()