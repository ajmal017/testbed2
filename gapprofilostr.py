import pandas as pd
from myfuncs import cumcovert
import os
import copy


def strrolling(symbols:list, time=2200, asrio=0.2):
    iniasset = 100000
    totalasset = iniasset
    filepath = r'E:\stockdata'
    tickerdict = {}

    for si in symbols:
        ticker = pd.read_csv(filepath + os.sep + si + '.csv')
        ticker = ticker.tail(time)
        if len(ticker) == time:
            tickerdict[si] = order(si, copy.deepcopy(ticker))

    for i in range(time):
        if i > 0:
            tm = (asrio / len(symbols)) * totalasset
            for tk, tv in tickerdict.items():
                tv.rolling(i, tm)


class order():
    def __init__(self, name, ticker, win=30, sk=0.6, gaps=(-0.05, -0.02)):
        self.name = name
        self.ticker = ticker
        self.o = list(self.ticker['Open'])
        self.c = list(self.ticker['Close'])
        self.h = list(self.ticker['High'])
        self.l = list(self.ticker['Low'])
        self.win = win
        self.sk = sk
        self.gaps = gaps
        self.orderdict = {}
        self.ordernum = -1

    def rolling(self, barnum, tm):
        gap = (self.o[barnum] - self.c[barnum - 1]) / self.c[barnum - 1]
        if self.gaps[0] < gap < self.gaps[1]:
            self.ordernum += 1
            self.orderdict[self.ordernum] = {}
            self.orderdict[self.ordernum]['Status'] = True
            self.orderdict[self.ordernum]['OpenNum'] = barnum
            self.orderdict[self.ordernum]['Win'] = -1
            self.orderdict[self.ordernum]['HP'] = -1
            self.orderdict[self.ordernum]['UP'] = self.c[barnum - 1]
            self.orderdict[self.ordernum]['DP'] = self.o[barnum]
            self.orderdict[self.ordernum]['MP'] = self.o[barnum] + (self.c[barnum - 1] - self.o[barnum]) * self.sk
            self.orderdict[self.ordernum]['MaxWin'] = (self.c[barnum - 1] - self.o[barnum]) * (1 - self.sk)
            self.orderdict[self.ordernum]['MaxLoss'] = (self.c[barnum - 1] - self.o[barnum]) * -1 * self.sk
            self.orderdict[self.ordernum]['Shares'] = int(tm / abs(self.orderdict[self.ordernum]['MaxLoss']))
            self.orderdict[self.ordernum]['inim'] = tm
            self.orderdict[self.ordernum]['PnL'] = []
            self.orderdict[self.ordernum]['CloseNum'] = None
            self.orderdict[self.ordernum]['CurrentBarNum'] = []

        for ok, ov in self.orderdict.items():
            if ov['Status']:
                self.orderdict[self.ordernum]['CurrentBarNum'].append(barnum)
                ov['Win'] += 1
                if ov['Win'] <= self.win:
                    if self.h[barnum] > ov['HP']:
                        ov['HP'] = self.h[barnum]
                    diff = self.c[barnum] - ov['MP']
                    if diff < ov['MaxLoss']:
                        diff = ov['MaxLoss']
                    if ov['HP'] > ov['UP']:
                        ov['Status'] = False
                        diff = ov['MaxWin']
                        ov['CloseNum'] = barnum
                    ov['Pnl'].append(diff)
                    if ov['Win'] == self.win:
                        ov['Status'] = False
                        ov['CloseNum'] = self.win



symbollist = ['aapl', 'amd', 'dis', 'ba', 'msft']