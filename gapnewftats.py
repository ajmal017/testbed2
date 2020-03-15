import matplotlib.pyplot as plt
import pandas as pd
from myfuncs import cumcovert
import os

def GapNewStats(symbol, gaps=(-0.05, -0.02)):
    path = r'E:\stockdata'
    ticker = pd.read_csv(path + os.sep + symbol + '.csv')
    c = list(ticker['Close'])
    o = list(ticker['Open'])
    h = list(ticker['High'])
    l = list(ticker['Low'])
    slen = len(c)
    gapslist = []

    for i in range(slen):
        if i > 0:
            gap = (o[i] - c[i - 1]) / c[i - 1]
            if gaps[0] < gap < gaps[1]:
                gapslist.append(gap)
    win = len(gapslist)
    chist, cbins= cumcovert(gapslist, win)

    return cbins, chist, slen


def GapNewWinStatsP(symbol, gaps=(-0.05, -0.02)):
    path = r'E:\stockdata'
    ticker = pd.read_csv(path + os.sep + symbol + '.csv')
    c = list(ticker['Close'])
    o = list(ticker['Open'])
    h = list(ticker['High'])
    l = list(ticker['Low'])

    slen = len(c)
    gapsnumlist = []
    idxes = range(slen)
    for i in idxes:
        if i > 0:
            gap = (o[i] - c[i - 1]) / c[i - 1]
            if gaps[0] < gap < gaps[1]:
                gapsnumlist.append(i)
    days = []
    nondays = 0
    for gi in gapsnumlist:
        subidxes = list(range(gi, slen))
        bp = c[gi - 1]
        hp = -1
        for si in subidxes:
            if hp < h[si]:
                hp = h[si]
            if hp > bp:
                days.append(si - gi)
                break
            else:
                if si == subidxes[-1]:
                    nondays += 1
    maxdays = max(days)
    if nondays != 0:
        days = days + [maxdays + 10] * nondays

    dayslen = len(days)
    chist, cbins= cumcovert(days, dayslen)

    return cbins, chist, slen


if __name__ == '__main__':
    symbol = 'amzn'
    gaps = (-0.05, -0.02)
    bins, hists, slen = GapNewWinStatsP(symbol, gaps)
    totalgaps = len(bins)
    plt.plot(bins, hists)
    plt.tight_layout()
    plt.grid()
    rio = totalgaps / slen
    title = symbol.upper() + ', TotalLenth = ' + str(slen) +', TotalGaps = ' + str(totalgaps) + ', Rate = ' + str(rio)
    plt.title(title)
    monlx = [30] * 100
    minmonly = min(hists)
    monly = [(mi / 100) * (1 - minmonly) + minmonly for mi in range(100)]
    plt.plot(monlx, monly)
    plt.show()
