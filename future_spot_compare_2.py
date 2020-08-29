from Quandl_Utils import myFilenameSort_Month, myStrDateSort, QuandlDfCleaner
import matplotlib.pyplot as plt
import pandas as pd
import functools
import os

spotpath = r'E:\newdata\LBMA-GOLD.csv'
spot = pd.read_csv(spotpath)
spotdate = list(spot['Date'])
adjspotdate = [di.replace('/', '-') for di in spotdate]
spot['Date'] = adjspotdate

futurespath = r'E:\newdata\quandl data\CHRIS-CME_GC\CHRIS-CME_GC-2.csv'
future = pd.read_csv(futurespath)

rdfs = QuandlDfCleaner([spot, future])
spotc = list(rdfs[0]['Last'])
futurec = list(rdfs[1]['Last'])

mins = [futurec[i] / spotc[i] for i in range(len(spotc))]
plt.plot(mins)
plt.tight_layout()
plt.grid()
plt.show()