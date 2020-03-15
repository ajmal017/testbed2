import pandas as pd
import random
import os


def strFunc(symbol, win=30, gap=0.1, fd=True, sk=0.6, asrio=None, bars=1000):
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

    winidxes = list(range(win))
    PnL = []
    PnLNum = []
    asset = 100000
    assetstart = asset
    if fd:
        while(rnum < len(c)):
            startp = o[rnum]
            prio = 1
            hp = -1
            tspu = startp * (1 + gap)
            tspm = startp * (1 + gap * sk)
            tspd = startp
            maxwin = tspu - tspm
            maxloss = tspd - tspm
            if asrio is not None:
                prio = (asset * asrio) / abs(maxloss)
            for i in winidxes:
                print(rnum, i)
                if rnum + i >= len(c) - 1:
                    pft = c[rnum + i] - tspm
                    if pft < maxloss:
                        pft = maxloss
                    elif pft > maxwin:
                        pft = maxwin
                    PnL.append(pft * prio)
                    PnLNum.append(rnum + i)
                    asset += pft * prio
                    rnum = rnum + i + 1
                    break
                if hp < h[rnum + i]:
                    hp = h[rnum + i]

                if hp > tspu:
                    pft = maxwin
                    PnL.append(pft * prio)
                    asset += pft * prio
                    PnLNum.append(rnum + i)
                    rnum = rnum + i + 1
                    break
                else:
                    if i == win - 1:
                        pft = c[rnum + i] - tspm
                        if pft < maxloss:
                            pft = maxloss
                        elif pft > maxwin:
                            pft = maxwin
                        PnL.append(pft * prio)
                        asset += pft * prio
                        PnLNum.append(rnum + i)
                        rnum = rnum + i + 1
    else:
        while (rnum < len(c)):
            startp = o[rnum]
            prio = 1
            lp = 10000000000000
            tspu = startp
            tspm = startp * (1 - gap * sk)
            tspd = startp * (1 - gap)
            maxwin = tspm - tspd
            maxloss = tspm - tspu
            if asrio is not None:
                prio = (asset * asrio) / abs(maxloss)
            for i in winidxes:
                print(rnum, i)
                if rnum + i >= len(c) - 1:
                    pft = tspm - c[rnum + i]
                    if pft < maxloss:
                        pft = maxloss
                    PnL.append(pft * prio)
                    PnLNum.append(rnum + i)
                    asset += pft * prio
                    rnum = rnum + i + 1
                    break
                if lp > l[rnum + i]:
                    lp = l[rnum + i]

                if lp < tspd:
                    pft = maxwin
                    PnL.append(pft * prio)
                    PnLNum.append(rnum + i)
                    asset += pft * prio
                    rnum = rnum + i + 1
                    break
                else:
                    if i == win - 1:
                        pft = tspm - c[rnum + i]
                        if pft < maxloss:
                            pft = maxloss
                        PnL.append(pft * prio)
                        PnLNum.append(rnum + i)
                        asset += pft * prio
                        rnum = rnum + i + 1

    PnLLine = [assetstart]
    for pi in PnL:
        tp = PnLLine[-1]
        PnLLine.append(pi + tp)
    PnLNum = [0] + PnLNum
    rPnLLine = [ri / assetstart for ri in PnLLine]

    return PnLLine, rPnLLine, PnLNum


class Order:
    ticker = None
    def __init__(self, Nos:list, prices:list, fd:bool):
        self.openprice = prices[0]
        self.closeprice = prices[1]
        self.fd = fd
        self.openNo = Nos[0]
        self.closeNo = Nos[1]
        self.PnL = []
        self.barNum = []
        if Order.ticker is None:
            print('未设置ticker！')
        else:
            subticker = Order.ticker[self.openNo: self.closeNo + 1]
            self.barNum = list(subticker.index)
            o = subticker['Open']
            h = subticker['High']
            l = subticker['Low']
            c = subticker['Close']
            self.PnL.append(0)
            if self.fd:
                for i in range(len(c)):
                    if i > 0:
                        self.PnL.append(self.openprice - c[i])
                    if i == len(c) - 1:
                        self.PnL[-1] = self.closeprice - self.openprice
            else:
                for i in range(len(c)):
                    if i > 0:
                        self.PnL.append(c[i] - self.openprice)
                    if i == len(c) - 1:
                        self.PnL[-1] = self.openprice - self.closeprice