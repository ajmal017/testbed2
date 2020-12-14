from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
import copy
import pytz
from datetime import datetime
import os
import time


histpath = r'D:\IB Data\History Data'


class myClient_get_Hist_data(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.bars = []

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('API初始化完成！')
        print('nextValidId:', orderId)

        zs = make_contract(symbol='ZS', conID=341629352, secType='FUT', exchange='ECBOT')
        le = make_contract(symbol='LE', conID=373227052, secType='FUT', exchange='GLOBEX')
        now = datetime.now().strftime("%Y%m%d %H:%M:%S")
        self.reqHistoricalData(0, zs, now, '2 Y', '1 hour', 'BID_ASK', 0, 1, False, [])

    def historicalData(self, reqId: int, bar: BarData):
        print(bar)
        self.bars.append(bar)


if __name__ == '__main__':

    app = myClient_get_Hist_data()
    app.connect('127.0.0.1', 7496, 3)
    app.run()





