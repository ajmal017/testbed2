import sys

sys.path.append("..")
import matplotlib.pyplot as plt
from myfuncs import cumcovert
from random import randint
import pandas as pd
import numpy as np
import os


def vrlmvfunc(ticker='uvxy', win=90, lils=[15, 20], lwin=22):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])
    c = list(stock['Close'])

    vix = vix.tail(len(h))
    vixl = list(vix['Low'])
    vixh = list(vix['High'])
    startnumlist = []
    riolist = []
    adjclist = []
    for i in range(len(vixl)):
        if vixh[i] > lils[1] > vixl[i]:
            startnumlist.append(i)
            if vixl[i] < lils[0]:
                randrio = randint(0, 100) / 100
                vixp = lils[0] + (lils[1] - lils[0]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                riolist.append(eprio)
            else:
                randrio = randint(0, 100) / 100
                vixp = vixl[i] + (lils[1] - vixl[i]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                riolist.append(eprio)
        elif vixl[i] < lils[0] < vixh[i]:
            startnumlist.append(i)
            if vixh[i] > lils[1]:
                randrio = randint(0, 100) / 100
                vixp = lils[0] + (lils[1] - lils[0]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                riolist.append(eprio)
            else:
                randrio = randint(0, 100) / 100
                vixp = lils[0] + (vixh[i] - lils[0]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                riolist.append(eprio)
        elif vixl[i] >= lils[0] and vixh[i] <= lils[1]:
            startnumlist.append(i)
            randrio = randint(0, 100) / 100
            vixp = vixl[i] + (vixh[i] - vixl[i]) * randrio
            eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
            riolist.append(eprio)
    n = -1
    for iv in startnumlist:
        if iv < len(h) - win:
            n += 1
            subclistl = c[iv + win - lwin: iv + win]
            lmc = min(subclistl)
            # randrio = randint(0, 100) / 100
            sp = l[iv] + (h[iv] - l[iv]) * riolist[n]
            adjc = (lmc - sp) / sp
            adjclist.append(adjc)

    return adjclist


ticker = 'uvxy'
win = 46
lwin = 22
lils = [15, 20, 25, 30, 35, 40, 50]
lillist = []
for li in range(len(lils)):
    if li == 0:
        lily = [0, lils[0]]
        lillist.append(lily)
        lily = [lils[li], lils[li + 1]]
        lillist.append(lily)
    elif li == len(lils) - 1:
        lily = [lils[li], 1000]
        lillist.append(lily)
    else:
        lily = [lils[li], lils[li + 1]]
        lillist.append(lily)

plotdict = {}
for lli in lillist:
    adjlist = vrlmvfunc(ticker, win=win, lils=lli, lwin=lwin)
    if adjlist != []:
        chist, cbins = cumcovert(adjlist)
        plotdict[tuple(lli)] = (chist, cbins)

II = []
for k, v in plotdict.items():
    Ii = ''
    II.append(Ii)
    label = str(k[0]) + ' < VIX < ' + str(k[1])
    II[-1], = plt.plot(v[1], v[0], label=label)

title = ticker.upper() + ', Win = ' + str(win) + ', Limit Win = ' + str(lwin)
xticks = np.arange(-0.9, 0.025, 0.025)
yticks = np.arange(0, 1.025, 0.025)
# plt.xticks(xticks)
plt.yticks(yticks)
plt.title(title)
plt.grid()
plt.tight_layout()
plt.legend()
plt.show()
