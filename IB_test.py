from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.common import *
from ibapi.ticktype import *
from iexfinance.stocks import Stock
import pandas as pd
from threading import Timer
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from IB_Utils import _myClient, make_contract
import time
import json
import os


class myClient_get_Options_details(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.result = []
        self.timrstart = None

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        con = make_contract(symbol='AMZN', secType='OPT')
        self.timrstart = datetime.now()
        self.reqContractDetails(1, con)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.__str__())
        self.result.append(contractDetails)

    def contractDetailsEnd(self, reqId: int):
        now = datetime.now()
        gap = (now - self.timrstart).microseconds / 1000000
        print('耗时{}秒！！！'.format(gap))
        print('结束！')


from IB_Utils_3 import myIB_Pro_Client

if __name__ == '__main__':
    app = myIB_Pro_Client()
    app.waitapidone()
    # op = app.reqOpenOrders()
    while True:
        # app.updateAcct_Pos_2()
        print(app.dyInitMoney, app.dyInitMoney, app.TWScapital, app.APIcapital)
        time.sleep(3)
    pass
