import matplotlib.pyplot as plt
import pandas as pd
import os

def adjminvalues(ticker='uvxy', win=90, lil=19):
    path = 'E:\stockdata'
    # ticker = 'vxx'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])

    vix = vix.tail(len(h))
    vixl = list(vix['Low'])
    vixh = list(vix['High'])
    startnumlist = []
    # win = 30
    # lil = 14
    adjclist = []
    for i in range(len(vixl)):
        if lil < vixh[i]:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(h) - win:
            subclisth = h[iv: iv + win + 1]
            subclistl = l[iv: iv + win + 1]
            sp = 0
            if lil < vixl[iv]:
                sp = l[iv]
            else:
               sp = ((vixh[iv] - lil) / (vixh[iv] - vixl[iv])) * (h[iv] - l[iv])  + l[iv]
            minl = min(subclistl)
            adjc = (minl - sp) / sp
            adjclist.append(adjc)

    return adjclist
