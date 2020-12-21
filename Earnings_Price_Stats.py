import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
import numpy as np
import pandas as pd
import json
import os

epath = r'E:\Yahoo data\Earnings 2'
ppath = r'E:\Yahoo data\Hist Price'
dateformat = '%Y-%m-%d'

fn = 5

files = os.listdir(epath)
for fi in files:
    symbol = fi.split('.')[0]

    edf = pd.read_csv(epath + os.sep + fi)
    esdates = []
    essps = []
    fl = len(edf)
    for esi in range(fl):
        ess = edf['epssurprisepct'][esi]
        esd = edf['startdatetime'][esi].split('T')[0]

        if not np.isnan(ess) and edf['gmtOffsetMilliSeconds'][esi] == 0:
            esdates.append(esd)
            essps.append(ess)

    pdf = pd.read_csv(ppath + os.sep + fi)
    dates = pdf['Date'].to_list()
    close = pdf['Close'].to_list()
    high = pdf['High'].to_list()
    low = pdf['Low'].to_list()

    chg = []
    abschg = []

    for di in esdates:

        weekday = datetime.strptime(di, dateformat).weekday()
        isweekend = False
        rdi = di
        if weekday in [5, 6]:
            isweekend = True
            rdi = (datetime.strptime(di, dateformat) - timedelta(days=(weekday - 4))).strftime(dateformat)

        if rdi in dates:
            idx = dates.index(rdi)
            csidx = idx - 1
            subidxs = idx
            subidxe = idx + fn
            if isweekend:
                csidx = idx
                subidxs = idx + 1
                subidxe = idx + fn + 1

            cs = close[csidx]
            subh = high[subidxs: subidxe]
            subl = low[subidxs: subidxe]
            maxh = max(subh)
            minl = min(subl)
            maxhch = (maxh - cs) / cs
            minlch = (minl - cs) / cs

            if abs(minlch) >= abs(maxhch):
                chg.append(minlch)
                abschg.append(abs(minlch))
            else:
                chg.append(maxhch)
                abschg.append(abs(maxhch))
        else:
            chg.append(np.nan)
            abschg.append(np.nan)

        delnums = []
        for ni in range(len(chg)):
            if np.isnan(chg[ni]):
                delnums.append(ni)
        delnums = reversed(delnums)

        for dli in delnums:
            essps.pop(dli)
            chg.pop(dli)
            abschg.pop(dli)

    print(len(chg))
    if len(chg) > 10:
        plt.figure(symbol + ':' + str(len(chg)))

        plt.subplot(1, 2, 1)
        plt.scatter(essps, chg)
        plt.title('Scatter')
        plt.tight_layout()
        plt.grid()

        plt.subplot(1, 2, 2)
        plt.hist(abschg, bins=len(abschg), density=True, cumulative=True)
        plt.title('Cumulative Density')
        plt.tight_layout()
        plt.grid()

        plt.show()
    pass
