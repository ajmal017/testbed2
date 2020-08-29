import matplotlib.pyplot as plt
from datetime import date, timedelta
import functools
import json
import numpy as np
import pandas as pd
import copy
import os


def myfilenamesort_month(x, y):
    xstr = x.split('.')[0].split('-')
    xdate = date(int(xstr[0]), int(xstr[1]), 1)

    ystr = y.split('.')[0].split('-')
    ydate = date(int(ystr[0]), int(ystr[1]), 1)

    if xdate < ydate:
        return -1
    elif xdate > ydate:
        return 1
    else:
        return 0


path = r'E:\newdata\quandl data\CHRIS-CME_ED\Singular Contracts'
filelist = os.listdir(path)
filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort_month))
superdata = {}
monthnum = {}
xticks = []
xlabels = []
mn = 0
for fi in filelist:
    sdata = pd.read_csv(path + os.sep + fi)
    last = list(sdata['Settle'])
    NO = list(sdata['Date No.'])
    xticks.append(mn)
    xlabels.append(fi.split('.')[0])

    rlen = len(NO)
    for ri in range(rlen):
        if NO[ri] not in superdata.keys():
            superdata[NO[ri]] = {}
        superdata[NO[ri]][mn] = last[ri]

    mn += 1

cnrio = 0.05
cn = 0
for k, v in superdata.items():
    km = list(sorted(list(v.keys())))
    columon = []
    cx = []
    bp = v[km[0]]
    plotw = True
    for ki in km:
        if bp != 0:
            columon.append(copy.deepcopy(v[ki] / bp + cn * cnrio))
            cx.append(copy.deepcopy(ki))
        else:
            plotw = False
            break
    if plotw:
        plt.plot(copy.deepcopy(cx), copy.deepcopy(columon))
        cn += 1
plt.xticks(xticks, xlabels)
plt.tight_layout()
plt.grid()
plt.show()