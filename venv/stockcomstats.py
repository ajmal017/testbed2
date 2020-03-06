from myfuncs import cumcovert
import pandas as pd
import copy
import os

def stockstats(symbol, win=30):
    path = 'E:\stockdata'
    # ticker = 'aapl'
    stock = pd.read_csv(path + os.sep + symbol + '.csv')
    c = list(stock['Close'])
    h = list(stock['High'])
    l = list(stock['Low'])
    # win = 30
    adjclistCom = []
    adjclistMin = []
    adjclistMax = []
    for i in range(len(c)):
        if i >= win:
            subclistl = l[i - win + 1: i + 1]
            mincl = min(subclistl)
            adjcMin = (mincl - c[i - win]) / c[i - win]
            adjclistMin.append(adjcMin)

            subclisth = h[i - win + 1: i + 1]
            minch = max(subclisth)
            adjcMax = (minch - c[i - win]) / c[i - win]
            adjclistMax.append(adjcMax)

            adjc = (c[i] - c[i - win]) / c[i - win]
            adjclistCom.append(adjc)
    datadict = {}
    hist, bins = cumcovert(adjclistCom)
    datadict['Com'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMax)
    datadict['Max'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMin)
    datadict['Min'] = (copy.deepcopy(hist), copy.deepcopy(bins))

    return datadict

