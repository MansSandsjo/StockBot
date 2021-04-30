import investpy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from array import *

OMXS30 = pd.read_csv("OMXS30.txt")
stocks = OMXS30["ticker"].tolist()

dfs = list()

start_date='01/01/2001'
end_date='01/01/2021'

for stock in stocks:
   df = investpy.get_stock_historical_data(stock=stock,
                                           country='Sweden',
                                           from_date=start_date,
                                           to_date=end_date)
   dfs.append(df)

for i in dfs:
    i.drop(['Currency','Open','High','Low','Volume'], axis=1, inplace=True)

#k= 2
#for i in dfs:
#    plt.plot(i, label = k)
#    k=k+1

#plt.legend()
#plt.show()

#plt.plot(dfs[12],label = 'hm')
#plt.show()

# H & M Hennes & Mauritz AB B
hm = dfs[12]
hm.reset_index(inplace=True)

hm_temp = hm.head(5)

print(hm)


#Skapar en tom array med floats för at
arr = array('f',[])

#procentuell avvikelse
fh = 1.15
fl = 0.85
i = 0
ip=0
ep=0
#for i in range(len(hm)-100):
while i<(len(hm)-1):
   pt_1 = hm.iloc[i+1,1]
   pt_0 = hm.iloc[i, 1]
   hh = (pt_1/pt_0)
   if hh>fh or hh<fl:
       hm.drop(index=(i + 1), inplace=True)
       ip = ip + 1
   i = i+1

i=0
while i<(len(hm)-1):
   #print(len(hm))
   #print("i ", i)
   pt_1 = hm.iloc[i+1,1]
   pt_0 = hm.iloc[i, 1]
   hh = (pt_1/pt_0)
   arr.append(hh)
   i = i+1

#plt.plot(hm.Date[0:len(hm)-1],arr[0:len(arr)])
plt.plot(hm.Date[0:len(hm)-1],arr[0:len(arr)])





