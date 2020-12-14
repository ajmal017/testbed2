from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
from threading import Timer
import pytz
from datetime import datetime
import copy
import time
import os
import matplotlib.pyplot as plt


columns = ['DateTime', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Last', 'Last Size']
datapath = r'D:\IB Data\Future Spread'
estz = pytz.timezone('America/New_York')


class myClient_get_FUT_Spread_Tickdata(_myClient):
    def __init__(self, RorS=True):
        _myClient.__init__(self)
        self.contracts = {}
        self.id_tick_tab = {}
        self.combo_tick = []
        self.combo_tick_pre = []
        self.RorS = RorS
        self.drawticktypes = [0, 1, 2, 3, 66, 67, 69, 70]
        self.plotstart = False
        self.plotnums = 0
        self.spreadname = ''
        self.filename = ''

        plt.ion()
        plt.figure(1)
        plt.tight_layout()
        plt.grid()

    def get_contracts(self, cons: dict):
        self.contracts = cons
        sym = cons['back'].symbol
        back = cons['back'].localSymbol
        front = cons['front'].localSymbol
        spath = datapath + os.sep + sym
        if not os.path.exists(spath):
            os.mkdir(spath)
        self.spreadname = '{}-{}'.format(back, front)
        self.filename = spath + os.sep + '{}-{}_spread.txt'.format(back, front)

        plt.title(self.spreadname)

    def write_data(self):
        if None not in self.combo_tick:
            f = open(self.filename, 'a+')
            txt = ','.join(str(i) for i in self.combo_tick) + '\n'
            f.write(txt)
            f.close()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('API初始化完成！')
        print('nextValidId:', orderId)

        if not self.RorS:
            self.reqMarketDataType(4)
            time.sleep(0.03)
        self._reqData()

    def _reqData(self):
        self.id_tick_tab[0] = [None] * 5
        self.id_tick_tab[1] = [None] * 5
        self.combo_tick = [None] * 5
        self.combo_tick_pre = [None] * 5
        self.reqMktData(0, self.contracts['back'], '', False, False, [])
        time.sleep(0.03)
        self.reqMktData(1, self.contracts['front'], '', False, False, [])

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):

        symbol = self.contracts['back'].localSymbol
        if reqId == 1:
            symbol = self.contracts['front'].localSymbol
        BorA = '-'
        if tickType == 66 or tickType == 1:
            BorA = 'Bid'
        elif tickType == 67 or tickType == 2:
            BorA = 'Ask'
        print(symbol, '{}价格：'.format(BorA), price)

        strnow = datetime.now(tz=estz).strftime('%Y-%m-%d %H:%M:%S:%f')
        if tickType == 66 or tickType == 1:
            self.combo_tick_pre = copy.deepcopy(self.combo_tick)
            self.id_tick_tab[reqId][1] = price
            self.id_tick_tab[reqId][0] = strnow
            self.calc_combo_tick(1, strnow)
            self.write_data()

        elif tickType == 67 or tickType == 2:
            self.combo_tick_pre = copy.deepcopy(self.combo_tick)
            self.id_tick_tab[reqId][2] = price
            self.id_tick_tab[reqId][0] = strnow
            self.calc_combo_tick(2, strnow)
            self.write_data()

        if tickType in self.drawticktypes:
            self.plot_chart()

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):

        symbol = self.contracts['back'].localSymbol
        if reqId == 1:
            symbol = self.contracts['front'].localSymbol
        BorA = '-'
        if tickType == 69 or tickType == 0:
            BorA = 'Bid'
        elif tickType == 70 or tickType == 3:
            BorA = 'Ask'
        print(symbol, '{}尺寸：'.format(BorA), size)

        strnow = datetime.now(tz=estz).strftime('%Y-%m-%d %H:%M:%S:%f')
        if tickType == 69 or tickType == 0:
            self.combo_tick_pre = copy.deepcopy(self.combo_tick)
            self.id_tick_tab[reqId][3] = size
            self.id_tick_tab[reqId][0] = strnow
            self.calc_combo_tick(3, strnow)
            self.write_data()

        elif tickType == 70 or tickType == 3:
            self.combo_tick_pre = copy.deepcopy(self.combo_tick)
            self.id_tick_tab[reqId][4] = size
            self.id_tick_tab[reqId][0] = strnow
            self.calc_combo_tick(4, strnow)
            self.write_data()

        if tickType in self.drawticktypes:
            self.plot_chart()

    def calc_combo_tick(self, tickbit: int, strnow: str):
        if (not self.id_tick_tab[0][tickbit] is None) and (not self.id_tick_tab[1][tickbit] is None):
            self.combo_tick[0] = strnow
            if tickbit in [1, 2]:
                val = self.id_tick_tab[0][tickbit] - self.id_tick_tab[1][tickbit]
                self.combo_tick[tickbit] = val

            elif tickbit in [3, 4]:
                val = self.id_tick_tab[0][tickbit]
                if self.id_tick_tab[0][tickbit] > self.id_tick_tab[1][tickbit]:
                    val = self.id_tick_tab[1][tickbit]
                self.combo_tick[tickbit] = val

    def plot_chart(self):
        if not self.plotstart:
            if (None not in self.combo_tick) and (None not in self.combo_tick_pre):
                self.plotstart = True
        else:
            x = [self.plotnums, self.plotnums + 1]
            bidy = [self.combo_tick_pre[1], self.combo_tick[1]]
            asky = [self.combo_tick_pre[2], self.combo_tick[2]]
            self.plotnums += 1

            plt.plot(x, bidy, color='green')
            plt.plot(x, asky, color='red')
            plt.draw()
            plt.pause(0.001)


if __name__ == '__main__':
    coilk1 = make_contract(symbol='COIL', conID=153452020, secType='FUT', exchange='IPE', localSymbol='COILK1')
    coilh1 = make_contract(symbol='COIL', conID=153452051, secType='FUT', exchange='IPE', localSymbol='COILH1')

    ES202012 = make_contract(symbol='ES', conID=383974339, secType='FUT', exchange='GLOBEX', localSymbol='ESZ0')
    ES202103 = make_contract(symbol='ES', conID=396336017, secType='FUT', exchange='GLOBEX', localSymbol='ESH1')
    cons = {'back': ES202103, 'front': ES202012}

    app = myClient_get_FUT_Spread_Tickdata()
    app.get_contracts(cons)
    app.connect('127.0.0.1', 7496, 1)
    app.run()