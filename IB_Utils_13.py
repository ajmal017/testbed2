from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
import copy
import pytz
from datetime import datetime
import os
import time
import matplotlib.pyplot as plt

columns = ['DateTime', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Mid Point']
datapath = r'D:\IB Data\Future Spread Plus'
estz = pytz.timezone('America/New_York')


class myClient_get_Combos_Tickdata(_myClient):
    def __init__(self, combo: dict):
        _myClient.__init__(self)
        self.combo = combo
        fname = datapath + os.sep + combo['back'].symbol
        if not os.path.exists(fname):
            os.mkdir(fname)
        self.spreadname = '{}-{}'.format(combo['back'].localSymbol, combo['front'].localSymbol)
        self.filename = fname + os.sep + self.spreadname + '-tick.txt'
        self.id_tick_tab = {0: [None] * 5, 1: [None] * 5}
        self.spread_tab = [None] * 5
        self.spread_tab_p = [None] * 5
        self.plotstart = False
        self.plotnums = 0

        plt.ion()
        plt.figure(1)
        plt.tight_layout()
        plt.grid()
        plt.title(self.spreadname)

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('API初始化完成！')
        print('nextValidId:', orderId)

        self._reqData()

    def _reqData(self):
        self.reqTickByTickData(0, self.combo['back'], 'BidAsk', 0, False)
        print(0, '请求{}数据'.format(self.combo['back'].localSymbol))

        self.reqTickByTickData(1, self.combo['front'], 'BidAsk', 0, False)
        print(1, '请求{}数据'.format(self.combo['front'].localSymbol))

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: int, askSize: int, tickAttribBidAsk: TickAttribBidAsk):
        strtime = datetime.now(estz).strftime("%Y-%m-%d %H:%M:%S.%f")
        # strtime = datetime.fromtimestamp(time, estz).strftime("%Y-%m-%d %H:%M:%S")

        symbol = self.combo['back'].localSymbol
        if reqId == 1:
            symbol = self.combo['front'].localSymbol

        print(symbol, ' 时间', strtime, ' Bid', bidPrice, 'Ask', askPrice, ' Bid Size', bidSize, ' Asksize', askSize)

        tickdata = [time, bidPrice, askPrice, bidSize, askSize]
        self.id_tick_tab[reqId] = tickdata

        if None not in self.id_tick_tab[0] and None not in self.id_tick_tab[1]:
            self.spread_tab_p = copy.deepcopy(self.spread_tab)

            self.spread_tab[0] = strtime
            self.spread_tab[1] = self.id_tick_tab[0][1] - self.id_tick_tab[1][2]
            self.spread_tab[2] = self.id_tick_tab[0][2] - self.id_tick_tab[1][1]

            self.spread_tab[3] = self.id_tick_tab[0][3]
            if self.id_tick_tab[0][3] >= self.id_tick_tab[1][4]:
                self.spread_tab[3] = self.id_tick_tab[1][4]

            self.spread_tab[4] = self.id_tick_tab[0][4]
            if self.id_tick_tab[0][4] >= self.id_tick_tab[1][3]:
                self.spread_tab[4] = self.id_tick_tab[1][3]

            f = open(self.filename, 'a+')
            pdata = ','.join(str(i) for i in self.spread_tab) + '\n'
            f.write(pdata)
            f.close()

            self.plot_chart()

    def plot_chart(self):
        if not self.plotstart:
            if (None not in self.spread_tab) and (None not in self.spread_tab_p):
                self.plotstart = True
        else:
            x = [self.plotnums, self.plotnums + 1]
            bidy = [self.spread_tab_p[1], self.spread_tab[1]]
            asky = [self.spread_tab_p[2], self.spread_tab[2]]
            self.plotnums += 1

            plt.plot(x, bidy, color='green')
            plt.plot(x, asky, color='red')
            plt.draw()
            plt.pause(0.001)


if __name__ == '__main__':

    ES202012 = make_contract(symbol='ES', conID=383974339, secType='FUT', exchange='GLOBEX', localSymbol='ESZ0')
    ES202103 = make_contract(symbol='ES', conID=396336017, secType='FUT', exchange='GLOBEX', localSymbol='ESH1')
    ES = {'back': ES202103, 'front': ES202012}

    NQ202012 = make_contract(symbol='NQ', conID=383974419, secType='FUT', exchange='GLOBEX', localSymbol='NQZ0')
    NQ202103 = make_contract(symbol='NQ', conID=396335999, secType='FUT', exchange='GLOBEX', localSymbol='NQH1')
    NQ = {'back': NQ202103, 'front': NQ202012}

    YM202012 = make_contract(symbol='YM', conID=396335960, secType='FUT', exchange='ECBOT', localSymbol='YM DEC 20')
    YM202103 = make_contract(symbol='YM', conID=412888950, secType='FUT', exchange='ECBOT', localSymbol='YM MAR 21')
    YM = {'back': YM202103, 'front': YM202012}

    RTY202012 = make_contract(symbol='RTY', conID=383974422, secType='FUT', exchange='GLOBEX', localSymbol='RTYZ0')
    RTY202103 = make_contract(symbol='RTY', conID=396336027, secType='FUT', exchange='GLOBEX', localSymbol='RTYH1')
    RTY = {'back': RTY202103, 'front': RTY202012}

    GC202104 = make_contract(symbol='GC', conID=368776104, secType='FUT', exchange='NYMEX', localSymbol='GCJ1')
    GC202102 = make_contract(symbol='GC', conID=358917044, secType='FUT', exchange='NYMEX', localSymbol='GCG1')
    GC = {'back': GC202104, 'front': GC202102}

    SI202101 = make_contract(symbol='SI', conID=355211350, secType='FUT', exchange='NYMEX', localSymbol='SIF1')
    SI202103 = make_contract(symbol='SI', conID=362937126, secType='FUT', exchange='NYMEX', localSymbol='SIH1')
    SI = {'back': SI202103, 'front': SI202101}

    app = myClient_get_Combos_Tickdata(GC)
    app.connect('127.0.0.1', 7496, 2)
    app.run()