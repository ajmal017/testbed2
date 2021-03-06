from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
import numpy as np
import pytz
from datetime import datetime
import os
import time
import copy

columns = ['DateTime', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Last', 'Last Size']
datapath = r'D:\IB Data\Tick Data'
estz = pytz.timezone('America/New_York')


class myClient_get_FUT_Tickdata(_myClient):
    def __init__(self, contractlist: list):
        _myClient.__init__(self)
        self.contractlist = contractlist
        self.id_sy_tab = {}
        self.id_tick_tab = {}

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('API初始化完成！')
        print('nextValidId:', orderId)

        self.reqMarketDataType(4)
        self._reqData()

    def _reqData(self):
        reqid = 0
        for ci in self.contractlist:
            self.reqMktData(reqid, ci, '', False, False, [])
            self.id_sy_tab[reqid] = ci.symbol
            self.id_tick_tab[reqid] = [np.nan] * 7
            time.sleep(0.03)

            print(reqid, '请求{}数据'.format(ci.symbol))

            reqid += 1

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        symbol = self.id_sy_tab[reqId]
        print('价格：', symbol, price)

        if tickType == 66:
            self.id_tick_tab[reqId][2] = price
        elif tickType == 67:
            self.id_tick_tab[reqId][3] = price
        elif tickType == 68:
            self.id_tick_tab[reqId][5] = price

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        symbol = self.id_sy_tab[reqId]
        print('尺寸：', symbol, size)

        if tickType == 69:
            self.id_tick_tab[reqId][1] = size
        elif tickType == 70:
            self.id_tick_tab[reqId][4] = size
        elif tickType == 71:
            self.id_tick_tab[reqId][6] = size

    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        if tickType == 88:
            sdatetime = datetime.fromtimestamp(int(value), estz).strftime("%Y-%m-%d %H:%M:%S")
            self.id_tick_tab[reqId][0] = sdatetime
            symbol = self.id_sy_tab[reqId]

            print('时间：', symbol, sdatetime)

            # filename = datapath + os.sep + symbol + '-tick.txt'
            # f = open(filename, 'a+')
            # pdata = ','.join([str(i) for i in self.id_tick_tab[reqId]]) + '\n'
            # f.write(pdata)
            # f.close()


if __name__ == '__main__':

    conlist = []
    sb = make_contract(symbol='SB', conID=320220010, secType='FUT', exchange='NYBOT')
    cc = make_contract(symbol='CC', conID=348296999, secType='FUT', exchange='NYBOT')
    gc = make_contract(symbol='GC', conID=442474779, secType='FUT', exchange='NYMEX')
    zs = make_contract(symbol='ZS', conID=341629352, secType='FUT', exchange='ECBOT')
    le = make_contract(symbol='LE', conID=373227052, secType='FUT', exchange='GLOBEX')
    vix = make_contract(symbol='VIX', conID=394987017, secType='FUT', exchange='CFE')
    zg = make_contract(symbol='ZG', conID=217704900, secType='FUT', exchange='NYSELIFFE')
    coil = make_contract(symbol='COIL', conID=153452027, secType='FUT', exchange='IPE')
    w = make_contract(symbol='W', conID=374752952, secType='FUT', exchange='ICEEUSOFT')
    conlist.append(copy.deepcopy(w))

    app = myClient_get_FUT_Tickdata(conlist)
    app.connect('127.0.0.1', 4003, 1)
    app.run()