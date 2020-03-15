import pandas as pd
import random
import os


def gapFunc(symbol, win=30, gaps=(-0.05, -0.02), sk=0.6, asrio=0.1, bars=1100):
    filepath = r'E:\stockdata'
    ticker = pd.read_csv(filepath + os.sep + symbol + '.csv')
    ticker = ticker.tail(bars)
    ticker.reset_index(drop=True, inplace=True)
    if len(ticker) < bars:
        return None, None, None
    o = ticker['Open']
    h = ticker['High']
    l = ticker['Low']
    c = ticker['Close']
    rnum = random.randint(0, 100)
    biscp = o[rnum]
    rio = 100 / biscp
    o = list(o * rio)
    h = list(h * rio)
    l = list(l * rio)
    c = list(c * rio)

    PnL = []
    PnLNum = [rnum]
    asset = 100000
    assetstart = asset

    while(rnum < bars - 1):
        subidxes = list(range(rnum, bars))
        for i in subidxes:
            gap = (o[i] - c[i - 1]) / c[i - 1]
            if gaps[0] < gap < gaps[1]:
                if i + win <= bars:
                    winidxes = list(range(i, i + win))
                else:
                    winidxes = list(range(i, bars))
                tspu = c[i - 1]
                tspd = o[i]
                diff = tspu - tspd
                tspm = tspd + diff * sk
                maxwin = diff * (1 - sk)
                maxloss = diff * -1 * sk
                snum = int((asset * asrio) / abs(maxloss))
                hp = -1
                for wi in winidxes:
                    if hp < h[wi]:
                        hp = h[wi]

                    if hp > tspu:
                        pft = maxwin * snum
                        PnL.append(pft)
                        asset += pft
                        PnLNum.append(wi)
                        rnum = rnum + wi + 1
                        break
                    else:
                        if wi == winidxes[-1]:
                            pft = c[wi] - tspm
                            if pft < maxloss:
                                pft = maxloss
                            pft *= snum
                            PnL.append(pft)
                            asset += pft
                            PnLNum.append(wi)
                            rnum = rnum + wi + 1
                break

    sumPnL = [assetstart]
    for pi in PnL:
        sp = sumPnL[-1] + pi
        sumPnL.append(sp)
    rltPnL = [ri / assetstart for ri in sumPnL]

    return sumPnL, rltPnL, PnLNum