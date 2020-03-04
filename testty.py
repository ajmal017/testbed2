import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from myfuncs import cumcovert
import os

path = 'E:\stockdata'
ticker = 'uvxy'
vix = pd.read_csv(path + os.sep + '^VIX.csv')
stock = pd.read_csv(path + os.sep + ticker + '.csv')
c = list(stock['Close'])
vix = vix.tail(len(c))
vixc = list(vix['Close'])
startnumlist = []
win = 120
lil = 20
adjclist = []
for i in range(len(vixc)):
    if vixc[i] > lil:
        startnumlist.append(i)

for iv in startnumlist:
    if iv < len(c) - win:
        adjc = (c[iv + win] - c[iv]) / c[iv]
        adjclist.append(adjc)
binnum = len(adjclist)
# hist, bins = np.histogram(adjclist, bins=200, density=False)
# hist = list(hist)
# bins = bins[1:]
# bins = list(bins)
# ctotal = sum(hist)
# chist = [sum(hist[:ic + 1]) / ctotal for ic in range(len(hist))]
#
# plt.plot(bins, chist)
# plt.show()

# plt.hist(adjclist, bins=binnum, density=True, cumulative=True)
# plt.tight_layout()
# plt.grid()
# plt.title('Value  ' + ticker.upper() + ': WIN = ' + str(win) + ', VIX > ' + str(lil) + ', Bins = ' + str(binnum))
# plt.show()

hist, bins = cumcovert(adjclist)
plt.plot(bins, hist)
plt.tight_layout()
plt.grid()
plt.show()