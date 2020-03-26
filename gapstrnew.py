import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import random
import os


def dictsort(datas:dict):
    keys = list(datas.keys())
    keys = sorted(keys)
    values = [datas[ki] for ki in keys]
    return keys, values


def GapStrNew(tdata, gaps=(-0.05, -0.02), win=30, asario=0.2, sk=0.65, bias=0.01):
    c = list(tdata['Close'])
    o = list(tdata['Open'])
    h = list(tdata['High'])
    l = list(tdata['Low'])
    iniasset = 100000
    totalasset = [iniasset]

    slen = len(c)
    gapsnumlist = []
    idxes = range(slen)
    for i in idxes:
        if i > 0:
            gap = (o[i] - c[i - 1]) / c[i - 1]
            if gaps[0] < gap < gaps[1]:
               gapsnumlist.append(i)
    fullwin = 0
    PnL = [0]
    PnLNum = [0]
    for gi in gapsnumlist:
        rd = random.randint(-5, 10)
        bup = c[gi - 1]
        bdp = o[gi]
        diff = bup - bdp
        biasp = (bias * (rd / 10)) * bdp
        up = bup + biasp
        dp = bdp - diff + biasp
        mp = dp + 2 * diff * sk
        maxwin = up - mp
        maxloss = dp - mp
        shares = int((totalasset[-1] * asario) / abs(maxloss))
        if shares <= 0:
            shares = 0
        adjwin = gi + win
        if adjwin > slen:
            adjwin = slen
        subidxes = list(range(gi, adjwin))
        hp = -1
        for si in subidxes:
            if hp < h[si]:
                hp = h[si]
            if hp > up:
                pft = (maxwin - 0.01) * shares
                PnL.append(pft)
                la = totalasset[-1]
                totalasset.append(la + pft)
                PnLNum.append(gi)
                fullwin += 1
                break
            else:
                if si == subidxes[-1]:
                    pft = c[gi] - mp
                    if pft < maxloss:
                        pft = (maxloss - 0.01) * shares
                    PnL.append(pft)
                    la = totalasset[-1]
                    totalasset.append(la + pft)
                    PnLNum.append(gi)

    return PnLNum, PnL, totalasset, fullwin


path = r'E:\stockdata'
symbollist = ['msft', 'aapl', 'goog', 'bac', 'ba', 'amd', 'dis', 'nvda', 'amzn', 'fb', 'ge', 'pcg', 'v']
twin = 220 * 10
Datalist = []
FullWin = 0
for si in symbollist:
    ticker = pd.read_csv(path + os.sep + si + '.csv')
    ticker = ticker.tail(twin)
    PnLNum, PnL, totalasset, fullwin = GapStrNew(ticker, win=45, asario=0.2, sk=0.65, bias=0.05)
    PnLNum.pop(0)
    PnL.pop(0)
    FullWin += fullwin

    for pni in range(len(PnLNum)):
        ys = (PnLNum[pni], PnL[pni])
        Datalist.append(ys)

Tnumlist = [0]
for di in Datalist:
    Tnumlist.append(di[0])
xlist = sorted(Tnumlist)
result = Counter(xlist)
xxlist = list(range(min(xlist), max(xlist) + 1))
yxlist = []
for xxi in xxlist:
    if xxi not in result.keys():
        yxlist.append(0)
    else:
        yxlist.append(result[xxi])

Tnumlist = set(Tnumlist)
Tnumlist = list(Tnumlist)
Tnumlist = sorted(Tnumlist)

sl = len(symbollist)
Tdatalist = [sl * 100000]
for ui in Tnumlist:
    for ai in Datalist:
        if ui == ai[0]:
            tla = Tdatalist[-1]
            Tdatalist.append(ai[1] + tla)

adjTdatalist = [tti / (sl * 100000) for tti in Tdatalist]
fullwinrio = FullWin/ len(xlist)

plt.plot(xlist, adjTdatalist)
plt.grid()
plt.title('Fill Gap Strategy, FullWinRio=' + str(fullwinrio))
plt.show()







