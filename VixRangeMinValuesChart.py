import sys
sys.path.append("..")
import matplotlib.pyplot as plt
from myfuncs import cumcovert
from random import randint
import pandas as pd
import numpy as np
import os


def vixrangeminvaluesch(ticker='uvxy', win=90, lils=[15, 20]):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])

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
    coordlist = []
    for iv in startnumlist:
        if iv < len(h) - win:
            n += 1
            subclistl = l[iv: iv + win]
            minl = min(subclistl)
            endnum = subclistl.index(minl) + iv
            # randrio = randint(0, 100) / 100
            sp = l[iv] + (h[iv] - l[iv]) * riolist[n]
            adjc = (minl - sp) / sp
            coord = [[iv, endnum], [sp, minl]]
            coordlist.append(coord)
            adjclist.append(adjc)

    return coordlist, adjclist


ticker = 'UVXY'
win = 44
lils = [15, 20]
fl = -0.1
coordlist, adjclist = vixrangeminvaluesch(ticker, win, lils)
path = 'E:\stockdata'
stock = pd.read_csv(path + os.sep + ticker + '.csv')
h = list(stock['High'])
l = list(stock['Low'])

for si in range(len(h)):
    plt.plot([si, si], [h[si], l[si]], color='b')

n = -1
for ci in coordlist:
    n += 1
    cl = ''
    if adjclist[n] > fl:
        cl = 'r'
    else:
        cl = 'g'
    plt.plot(ci[0], ci[1], color=cl)

plt.tight_layout()
plt.grid()
plt.show()