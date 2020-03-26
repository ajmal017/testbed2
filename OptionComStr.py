import pandas as pd
from random import randint
import matplotlib.pyplot as plt
import os


def stockcomstrategyNew(stock, iniasset=100000, win=45, bias=0.01, closerio=0.03, sk=0.65, asrio=0.2, marg=0.01):
    o = list(stock['Open'])
    c = list(stock['Close'])
    h = list(stock['High'])
    l = list(stock['Low'])

    slen = len(c)
    Num = randint(0, 200)
    totalasset = iniasset
    PnL = []
    PnLNum = []
    fullwin = 0
    while(Num < slen):
        overlimit = False
        lm = Num + win
        if lm > slen:
            lm = slen
            overlimit = True
        print(Num)
        bp = o[Num]
        bis = bp * bias
        bissk = (randint(-5, 10) / 10) * bis
        up = bp * (1 + closerio) + bissk
        dp = bp * (1 - closerio) + bissk
        diff = up - dp
        mp = dp + sk * diff
        maxwin = up - mp
        maxloss = dp - mp
        if totalasset <= 0:
            totalasset = 0
        shares = int((totalasset * asrio) / abs(maxloss))
        subidxes = list(range(Num, lm))
        hp = -1
        for bi in subidxes:
            if hp < h[bi]:
                hp = h[bi]
            if hp > up:
                pft = (maxwin - marg) * shares
                totalasset += pft
                PnL.append(pft)
                PnLNum.append(bi)
                Num = bi + 1
                fullwin += 1
                break
            else:
                if bi == subidxes[-1]:
                    pft = c[bi] - mp
                    if pft < maxloss:
                        pft = (maxloss - marg) * shares
                    totalasset += pft
                    PnL.append(pft)
                    PnLNum.append(bi)
                    Num = bi + 1
        if overlimit:
            break

    return PnL, PnLNum, fullwin


symbol = 'v'
path = 'E:\stockdata'
stock = pd.read_csv(path + os.sep + symbol + '.csv')
stock = stock.tail(2200)

PnL, PnLNum, fullwin = stockcomstrategyNew(stock, iniasset=100000, win=45, bias=0.005, closerio=0.025, sk=0.65, asrio=0.15, marg=0.01)
PnLNum = [0] + PnLNum
adjPnL = [1]
for i in PnL:
    la = adjPnL[-1]
    adjp = la + i / 100000
    adjPnL.append(adjp)

fullwinrio = fullwin / len(PnLNum)
c = list(stock['Close'])
crio = 1 / c[0]
clist = [ci * crio for ci in c]
xlist = list(range(len(c)))

I1, = plt.plot(PnLNum, adjPnL, label='P / L')
I2, = plt.plot(xlist, clist, label=symbol.upper())
plt.title(symbol.upper() + ', FullWinRio=' + str(fullwinrio))
plt.legend()
plt.grid()
plt.show()
