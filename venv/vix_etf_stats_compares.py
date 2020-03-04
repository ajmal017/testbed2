import matplotlib.pyplot as plt
import pandas as pd
from myfuncs import cumcovert
import numpy as np
import os

def funcMin(ticker='vixy', win=90, lil=20):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    c = list(stock['Close'])
    vix = vix.tail(len(c))
    vixc = list(vix['Close'])
    startnumlist = []
    adjclist = []
    for i in range(len(vixc)):
        if vixc[i] > lil:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(c) - win:
            subclist = c[iv: iv + win + 1]
            minc = min(subclist)
            adjc = (minc - c[iv]) / c[iv]
            adjclist.append(adjc)

    return adjclist

def funcNormal(ticker='vixy', win=90, lil=20):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    c = list(stock['Close'])
    vix = vix.tail(len(c))
    vixc = list(vix['Close'])
    startnumlist = []
    adjclist = []
    for i in range(len(vixc)):
        if vixc[i] > lil:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(c) - win:
            adjc = (c[iv + win] - c[iv]) / c[iv]
            adjclist.append(adjc)

    return adjclist

def rangefuncMin(ticker='vixy', win=90, lmin=0, lmax=500):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    c = list(stock['Close'])
    vix = vix.tail(len(c))
    vixc = list(vix['Close'])
    startnumlist = []
    adjclist = []
    for i in range(len(vixc)):
        if vixc[i] > lmin and vixc[i] <= lmax:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(c) - win:
            subclist = c[iv: iv + win + 1]
            minc = min(subclist)
            adjc = (minc - c[iv]) / c[iv]
            adjclist.append(adjc)

    return adjclist

def rangefuncNormal(ticker='vixy', win=90, lmin=0, lmax=500):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    c = list(stock['Close'])
    vix = vix.tail(len(c))
    vixc = list(vix['Close'])
    startnumlist = []
    adjclist = []
    for i in range(len(vixc)):
        if vixc[i] > lmin and vixc[i] <= lmax:
            startnumlist.append(i)

    for iv in startnumlist:
        if iv < len(c) - win:
            adjc = (c[iv + win] - c[iv]) / c[iv]
            adjclist.append(adjc)

    return adjclist



