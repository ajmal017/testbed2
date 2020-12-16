from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
import numpy as np
import pytz
from datetime import datetime
import os
import time

columns = ['DateTime', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Last', 'Last Size']
datapath = r'D:\IB Data\Tick Data'
estz = pytz.timezone('America/New_York')


class myClient_get_STK_Tickdata_2(_myClient):
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

        self._reqData()

    def _reqData(self):
        reqid = 0
        for ci in self.contractlist:
            self.reqTickByTickData(reqid, ci, 'Last', 0, False)
            reqid += 1
            self.reqTickByTickData(reqid, ci, 'AllLast', 0, False)
            reqid += 1
            self.reqTickByTickData(reqid, ci, 'BidAsk', 0, True)
            reqid += 1
            self.reqTickByTickData(reqid, ci, 'MidPoint', 0, False)

            self.id_sy_tab[reqid] = ci.symbol
            self.id_tick_tab[reqid] = [np.nan] * 7
            time.sleep(0.03)

            print(reqid, '请求{}数据'.format(ci.symbol))
            reqid += 1

    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast, exchange: str,
                          specialConditions: str):
        print(reqId, tickType, time, price, size, exchange, specialConditions)

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: int, askSize: int, tickAttribBidAsk: TickAttribBidAsk):
        print(reqId, time, bidPrice, askPrice, bidSize, askSize)

    def tickByTickMidPoint(self, reqId: int, time: int, midPoint: float):
        print(reqId, time, midPoint)

    def historicalTicks(self, reqId: int, ticks: ListOfHistoricalTick, done: bool):
        pass

    def historicalTicksBidAsk(self, reqId: int, ticks: ListOfHistoricalTickBidAsk, done: bool):
        pass

    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast, done: bool):
        pass