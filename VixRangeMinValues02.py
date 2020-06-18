import sys
sys.path.append("..")
import matplotlib.pyplot as plt
from myfuncs import cumcovert
from random import randint
import pandas as pd
import numpy as np
import os


def vixrangeminvalues02(ticker='uvxy', win=66, lils=[15, 20], lr=-0.1):
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
    i = 0
    ps = False
    p2llist = []

    while i < len(vixh) - win:
        print(i, ps)
        ustrp = None
        if not ps:
            T1 = False
            T2 = False
            T3 = False
            T4 = False
            if vixl[i] < lils[0] < vixh[i] < lils[1]:
                randrio = randint(0, 100) / 100
                vixp = lils[0] + (vixh[i] - lils[0]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                ustrp = l[i] + (h[i] - l[i]) * eprio
                T1 = True
            elif vixl[i] < lils[0] and vixh[i] > lils[1]:
                randrio = randint(0, 100) / 100
                vixp = lils[0] + (lils[1] - lils[0]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                ustrp = l[i] + (h[i] - l[i]) * eprio
                T2 = True
            elif lils[0] < vixl[i] < lils[1] < vixh[i]:
                randrio = randint(0, 100) / 100
                vixp = vixl[i] + (lils[1] - vixl[i]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                ustrp = l[i] + (h[i] - l[i]) * eprio
                T3 = True
            elif lils[0] < vixl[i] and vixh[i] < lils[1]:
                randrio = randint(0, 100) / 100
                vixp = vixl[i] + (vixh[i] - vixl[i]) * randrio
                eprio = (vixp - vixl[i]) / (vixh[i] - vixl[i])
                ustrp = l[i] + (h[i] - l[i]) * eprio
                T4 = True
            ps = T1 or T2 or T3 or T4
            print(i, ps)
            if not ps:
                i += 1
        if ps:
            for si in range(win):
                sublist = l[i: i + si + 1]
                minl = min(sublist)
                rio = (minl - ustrp) / ustrp
                if rio <= lr:
                    p2llist.append(True)
                    i += si + 1
                    ps = False
                    break
                if si == win - 1:
                    fp = (c[i + si] - ustrp) / ustrp
                    p2llist.append(fp)
                    i += si + 1
                    ps = False

    return p2llist


ticker = 'uvxy'
win = 66
lils = [12, 17]
lr = -0.1
p2l = vixrangeminvalues02(ticker, win, lils, lr)
print(p2l)