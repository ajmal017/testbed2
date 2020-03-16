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


def GapStrNew(tdata, gaps=(-0.05, -0.02), win=30, asario=0.2, sk=0.6, bias=0.01):
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

    PnL = [0]
    PnLNum = [0]
    for gi in gapsnumlist:
        rd = random.randint(-5, 10)
        up = c[gi - 1]
        biasp = (bias * (rd / 10)) * up
        up += biasp
        dp = o[gi] + biasp
        diff = up - dp
        mp = dp + diff * sk
        maxwin = diff * (1 - sk)
        maxloss = diff * -1 * sk
        shares = int((totalasset[-1] * asario) / abs(maxloss))

        adjwin = gi + win
        if adjwin > slen:
            adjwin = slen
        subidxes = list(range(gi, adjwin))
        hp = -1
        for si in subidxes:
            if hp < h[si]:
                hp = h[si]
            if hp > up:
                pft = maxwin * shares
                PnL.append(pft)
                la = totalasset[-1]
                totalasset.append(la + pft)
                PnLNum.append(gi)
                break
            else:
                if si == subidxes[-1]:
                    pft = c[gi] - mp
                    if pft < maxloss:
                        pft = maxloss * shares
                    PnL.append(pft)
                    la = totalasset[-1]
                    totalasset.append(la + pft)
                    PnLNum.append(gi)

    return PnLNum, PnL, totalasset


path = r'E:\stockdata'
symbollist = ['msft', 'aapl', 'goog', 'ibm', 'bac', 'ba', 'amd', 'dis', 'nvda', 'amzn', 'fb', 'ge', 'pcg', 'v']
twin = 220 * 10
Datalist = []
for si in symbollist:
    ticker = pd.read_csv(path + os.sep + si + '.csv')
    ticker = ticker.tail(twin)
    PnLNum, PnL, totalasset = GapStrNew(ticker, win=45, asario=0.2, sk=0.65, bias=0.01)
    PnLNum.pop(0)
    PnL.pop(0)

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

plt.plot(xlist, adjTdatalist)
plt.grid()
plt.title('Fill Gap Strategy')
plt.show()







