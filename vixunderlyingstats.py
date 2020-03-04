import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
ticker = 'vixy'
vix = pd.read_csv(path + os.sep + '^VIX.csv')
stock = pd.read_csv(path + os.sep + ticker + '.csv')
slen = len(stock)
vix = vix.tail(slen)
vixc = list(vix['Close'])
vixh = list(vix['High'])
stockc = list(stock['Close'])
stockh = list(stock['High'])

lil = 20
vixcupnum = []
vixhupnum = []
for i in range(slen):
    if vixc[i] > lil:
        vixcupnum.append(i)
    if vixh[i] > lil:
        vixhupnum.append(i)

adjclist = []
adjhlist = []
for ic in vixcupnum:
    tailstockh = stockh[ic + 1:]
    maxth = max(tailstockh)
    adjc = (maxth - stockc[ic]) / stockc[ic]
    adjclist.append(adjc)

plt.hist(adjclist, bins=200, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.title(ticker.upper())
plt.show()
