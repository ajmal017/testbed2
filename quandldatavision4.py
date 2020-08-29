import matplotlib.pyplot as plt
from datetime import date, timedelta
import functools
import json
import numpy as np
import pandas as pd
import os

spath = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data Json'

fc = open(spath + os.sep + 'Close.json', 'r')
c = json.load(fc)
fc.close()

c1 = c['2']
c2 = c['3']



adjmdata = {}
for k in c1.keys():
    m = int(k.split('-')[1])
    clen = len(c1[k])
    cdiff = [(c2[k][i] / c1[k][i]) + m for i in range(clen)]
    if m not in adjmdata.keys():
        adjmdata[m] = []
    adjmdata[m].append(cdiff)

span = 5

for v in adjmdata.values():
    n = 0
    for y in v:
        ylen = len(y)
        x = list(range(n, ylen + n))
        n = x[-1] + span
        plt.plot(x, y)

plt.tight_layout()
plt.grid()
plt.show()




