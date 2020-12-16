from IB_Utils import _myClient, make_contract
from ibapi.common import *
from ibapi.ticktype import *
import copy
import pytz
from datetime import datetime
import os
import time

columns = ['DateTime', 'Bid Size', 'Bid', 'Ask', 'Ask Size', 'Mid Point']
datapath = r'D:\IB Data\Tick Data FX'
estz = pytz.timezone('America/New_York')


class myClient_get_FX_Tickdata(_myClient):
    def __init__(self, contractlist: list):
        _myClient.__init__(self)
        self.contractlist = contractlist
        self.id_sy_tab = {}

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('API初始化完成！')
        print('nextValidId:', orderId)

        self._reqData()

    def _reqData(self):
        reqid = 0
        for ci in self.contractlist:
            self.reqTickByTickData(reqid, ci, 'BidAsk', 0, True)
            sy = ''
            if ci.secType == 'CASH':
                 sy = ci.symbol + ci.currency
            else:
                sy = ci.symbol
            self.id_sy_tab[reqid] = sy

            time.sleep(0.03)

            print(reqid, '请求{}数据'.format(sy))
            reqid += 1

    def tickByTickBidAsk(self, reqId: int, time: int, bidPrice: float, askPrice: float,
                         bidSize: int, askSize: int, tickAttribBidAsk: TickAttribBidAsk):

        strtime = datetime.fromtimestamp(time, estz).strftime("%Y-%m-%d %H:%M:%S")
        midpoint = round((bidPrice + askPrice) / 2, 5)
        symbol = self.id_sy_tab[reqId]
        print(symbol, ' 时间', strtime, ' Bid', bidPrice, 'Ask', askPrice, ' Bid Size', bidSize,
              ' Asksize', askSize, ' Mid Point', midpoint)

        filename = datapath + os.sep + symbol + '-tick.txt'
        f = open(filename, 'a+')
        pdata = strtime + ',' + str(bidSize) + ',' + str(bidPrice) + ',' + str(askPrice) + ',' + str(askSize) + ',' + str(midpoint) + '\n'
        f.write(pdata)
        f.close()


if __name__ == '__main__':

    specs = [('EUR', 12087792, 'USD'),
             ('GBP', 12087797, 'USD'),
             ('USD', 15016059, 'JPY')
            ]
             # ('CHF', 12087802, 'USD'),
             # ('AUD', 14433401, 'USD'),
             # ('NZD', 39453441, 'USD'),
             # ('USD', 113342317, 'CNH'),
             # ('USD', 15016062, 'CAD'),
             # ]
    conlist = []
    # xau = make_contract(symbol='XAUUSD', conID=69067924, currency='USD', secType='CMDTY', exchange='SMART')
    # conlist.append(xau)
    # xag = make_contract(symbol='XAGUSD', conID=77124483, currency='USD', secType='CMDTY', exchange='SMART')
    # conlist.append(xag)

    for i in specs:
        con = make_contract(symbol=i[0], conID=i[1], secType='CASH', currency=i[2], exchange='IDEALPRO')
        conlist.append(copy.deepcopy(con))

    app = myClient_get_FX_Tickdata(conlist)
    app.connect('127.0.0.1', 4003, 1)
    app.run()