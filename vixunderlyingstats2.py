import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
ticker = 'VIXM'
vix = pd.read_csv(path + os.sep + '^VIX.csv')
stock = pd.read_csv(path + os.sep + ticker + '.csv')
slen = len(stock)
vix = vix.tail(slen)
vixc = list(vix['Close'])
vixh = list(vix['High'])
vixo = list(vix['Open'])
vixl = list(vix['Low'])
stockc = list(stock['Close'])
stockh = list(stock['High'])
stocko = list(stock['Open'])
stockl = list(stock['Low'])

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
for ic in vixhupnum:
    tailstockh = stockh[ic + 1:]
    adjsp = 0
    if vixo[ic] < lil:
        rio = lil / (vixh[ic] - vixl[ic])
        adjsp = stockl[ic] + (stockh[ic] - stockl[ic]) * rio
    else:
        adjsp = stocko[ic]
    maxth = max(tailstockh)
    adjc = (maxth - adjsp) / adjsp
    adjclist.append(adjc)

plt.hist(adjclist, bins=200, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.title(ticker.upper())
plt.show()