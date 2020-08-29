from Quandl_Utils import myFilenameSort_Month, myStrDateSort, QuandlDfCleaner
import matplotlib.pyplot as plt
import pandas as pd
import functools
import os

spotpath = r'E:\newdata\LBMA-GOLD.csv'
spot = pd.read_csv(spotpath)
# spot['Date'] = pd.to_datetime(spot.Date)
# spot['Date'] = spot['Date'].dt.strftime('%Y-%m-%d')
spotdate = list(spot['Date'])
adjspotdate = [di.replace('/', '-') for di in spotdate]
spot['Date'] = adjspotdate

futurespath = r'E:\newdata\quandl data\CHRIS-CME_GC\Singular Contracts'

fflist = os.listdir(futurespath)
fflist = sorted(fflist, key=functools.cmp_to_key(myFilenameSort_Month))[-39: -20]
ylabels = []
yticks = []
n = 0
ygap = 0.1
for fi in fflist:
    ylabels.append(fi.split('.')[0])
    yticks.append(n * ygap + 1)
    futureb = pd.read_csv(futurespath + os.sep + fi)
    future = futureb.iloc[::-1].reset_index(drop=True)
    rdfs = QuandlDfCleaner([spot, future])
    spotc = list(rdfs[0]['Last'])
    futurec = list(rdfs[1]['Last'])

    mins = [futurec[i] / spotc[i] + n * ygap for i in range(len(spotc))]
    plt.plot(mins)
    print(fi)
    n += 1

plt.yticks(yticks, ylabels)
plt.tight_layout()
plt.grid()
plt.show()
