import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
ticker = 'vxx'
vix = pd.read_csv(path + os.sep + '^VIX.csv')
stock = pd.read_csv(path + os.sep + ticker + '.csv')
c = list(stock['Close'])
vix = vix.tail(len(c))
vixc = list(vix['Close'])
startnumlist = []
win = 30
lil = 14
adjclist = []
for i in range(len(vixc)):
    if vixc[i] < lil:
        startnumlist.append(i)

for iv in startnumlist:
    if iv < len(c) - win:
        adjc = (c[iv + win] - c[iv]) / c[iv]
        adjclist.append(adjc)
binnum = len(adjclist)
plt.hist(adjclist, bins=binnum, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.title(ticker.upper() + ', WIN = ' + str(win) + ', Bins = ' + str(binnum))
plt.show()