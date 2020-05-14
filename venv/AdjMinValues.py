import matplotlib.pyplot as plt
import pandas as pd
import os

def adjminvalues(ticker='uvxy', win=90, lil=19):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])

    vix = vix.tail(len(h))
    vixl = list(vix['Low'])
    vixh = list(vix['High'])
    startnumlist = []
    adjclist = []
    for i in range(len(vixl)):
        if lil < vixh[i]:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(h) - win:
            subclisth = h[iv: iv + win]
            subclistl = l[iv: iv + win]
            sp = 0
            if lil < vixl[iv]:
                sp = l[iv]
            else:
               sp = ((vixh[iv] - lil) / (vixh[iv] - vixl[iv])) * (h[iv] - l[iv]) + l[iv]
            minl = min(subclistl)
            adjc = (minl - sp) / sp
            adjclist.append(adjc)

    return adjclist


def vixrangeminvalues(ticker='uvxy', win=90, lils=[12, 15, 20, 25, 30, 40, 50, 70]):
    lillist = []
    for li in range(len(lils)):
        if li == 0:
            lily = [0, lils[0]]
            lillist.append(lily)
        elif li == len(lils) - 1:
            lily = [lils[li], 1000]
            lillist.append(lily)
        else:
            lily = [lils[li], lils[li + 1]]
            lillist.append(lily)
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])

    vix = vix.tail(len(h))
    vixl = list(vix['Low'])
    vixh = list(vix['High'])

    adjclist = []
    numslist = []
    for li2 in lillist:
        startnumlist = []
        for i in range(len(vixl)):
            if vixh[i] >= li2[1] and vixl[i] < li2[1]:
                startnumlist.append(i)
            elif vixl[i] < li2[0] and vixh[i] >= li2[0]:
                startnumlist.append(i)
            elif vixl[i] >= li2[0] and vixh[i] < li2[1]:
                startnumlist.append(i)
        numslist.append(startnumlist)

    for ivi in numslist:
        for iv in ivi:
            if iv < len(h) - win:
                subclisth = h[iv: iv + win]
                subclistl = l[iv: iv + win]
                sp = 0
                if lil < vixl[iv]:
                    sp = l[iv]
                else:
                   sp = ((vixh[iv] - lil) / (vixh[iv] - vixl[iv])) * (h[iv] - l[iv]) + l[iv]
                minl = min(subclistl)
                adjc = (minl - sp) / sp
                adjclist.append(adjc) 

    return adjclist
