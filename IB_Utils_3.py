from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.common import *
from ibapi.scanner import ScannerSubscription, ScanData
from ibapi.ticktype import *
from iexfinance.stocks import Stock
import pandas as pd
from threading import Timer, Thread, Lock
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from IB_Utils import contract_to_df, _myClient, make_contract, print_Order_State
import time
import json
import math
import sys
import io
import os
import re


PublicInData = None
PublicOutData = None
InitDone = False
AcctDone = False
AccountsList = ''
NextValidId = 0
Error = []
MKTDataDict = {}
col = ['Last', 'Bid', 'Ask', 'Last Size', 'Bid Size', 'Ask Size', 'Vol', 'AvgVol', 'IV', 'Open', 'High', 'Low', 'Close']
for i in col:
    MKTDataDict[i] = None
UpdatePortfolio = {}
UpdateAccountValues = {}
openOrder = {}
orderStatus = {}


class myClient_m(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.lock = Lock()
        self.buff = None
        self.buff2 = None
        self.reqID = 0
        self.timegapstart = None
        self.timegapstartInit = False
        self.timestamplist = []
        self.start = False
        self.req0 = False
        self.req1 = False
        self.req2 = False
        self.req3 = False
        self.req4 = False
        self.req5 = False
        self.req7 = False
        self.req8 = False
        self.req9 = False
        self.req10 = False
        self.MKTdatabuff = None

        self.superoptdel = {}
        self.optreqidinfo = {}
        self.opthasdel = {}
        self.opthaonotdel = {}
        self.reciveoptdelstatus = {}
        self.optsupercon = []

    def control_reqtime_gap_2(self):
        now = datetime.now()
        timegap = (now - self.timegapstart).microseconds
        resttime = 20000 - timegap
        if resttime > 0:
            print('机器过热， 休息{}秒钟...'.format(resttime / 1000000))
            time.sleep(resttime / 1000000)
        self.timegapstart = datetime.now()

    def scan(self):
        timer = Timer(0.000001, self.scan)
        if not self.timegapstartInit:
            self.timegapstart = datetime.now()
            self.timegapstartInit = True

        global PublicInData
        global PublicOutData
        if not (PublicInData is None):
            Indata = PublicInData
            PublicInData = None

            if Indata['funcID'] == 0:
                self.req0 = True
                self.reqIds(-1)
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 1:
                self.req1 = True
                self.buff2 = Indata['reqId']
                self.reqID = Indata['reqId']
                self.reqContractDetails(Indata['reqId'], Indata['contract'])
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 2:
                self.req2 = True
                self.buff2 = Indata['parameters'][0]
                self.reqID = Indata['parameters'][0]
                self.reqSecDefOptParams(Indata['parameters'][0], Indata['parameters'][1], Indata['parameters'][2],
                                        Indata['parameters'][3], Indata['parameters'][4])
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 3:
                if Indata['parameters'][2].transmit:
                    self.req3 = True
                    self.buff2 = Indata['parameters'][0]
                    self.reqID = Indata['parameters'][0]
                self.placeOrder(Indata['parameters'][0], Indata['parameters'][1], Indata['parameters'][2])
                self.control_reqtime_gap_2()
                if not Indata['parameters'][2].transmit:
                    PublicOutData = False

            elif Indata['funcID'] == 4:
                self.req4 = True
                self.buff = {}
                # self.buff2 = {}
                self.buff['openOrder'] = {}
                self.buff['orderStatus'] = {}
                self.reqOpenOrders()
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 5:
                self.req5 = True
                self.buff = {}
                self.buff['AccountValue'] = {}
                self.buff['Portfolio'] = {}
                self.buff2 = Indata['parameters'][1]
                self.reqAccountUpdates(Indata['parameters'][0], Indata['parameters'][1])
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 6:
                self.cancelOrder(Indata['parameters'][0])
                self.control_reqtime_gap_2()
                PublicOutData = True

            elif Indata['funcID'] == 7:
                self.reqMarketDataType(3)
                self.req7 = True
                global MKTDataDict
                self.MKTdatabuff = MKTDataDict
                self.buff2 = Indata['parameters'][0]
                self.reqID = Indata['parameters'][0]
                self.reqMktData(Indata['parameters'][0], Indata['parameters'][1], Indata['parameters'][2],
                                Indata['parameters'][3], Indata['parameters'][4], Indata['parameters'][5])
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 8:
                self.reqOptionContractDetails_bulk(Indata['parameters'][0])

            elif Indata['funcID'] == 9:
                self.req9 = True
                self.buff = {}
                self.reqPositions()
                self.control_reqtime_gap_2()

            elif Indata['funcID'] == 10:
                self.req10 = True
                self.buff = {}
                self.reqCompletedOrders(Indata['parameters'][0])
                self.control_reqtime_gap_2()


        if self.req7:
            done = True
            for v in self.MKTdatabuff.keys():
                vd = not (v is None)
                done = done and vd
            if done:
                self.req7 = False
                PublicOutData = deepcopy(self.MKTdatabuff)
                self.MKTdatabuff = None
                self.buff2 = None
        if self.req8:
            bulkoptdone = True
            for sym, ids in self.optreqidinfo.items():
                if len(self.opthasdel[sym] + self.opthaonotdel[sym]) == len(ids) and len(ids) > 0:
                    if not self.reciveoptdelstatus[sym]:
                        optdelfile = ospath + os.sep + sym + '-specs.json'
                        Dict_to_Json(self.superoptdel[sym], optdelfile)
                        self.reciveoptdelstatus[sym] = True
                bulkoptdone = bulkoptdone and self.reciveoptdelstatus[sym]
            if bulkoptdone:
                self.req8 = False
                self.superoptdel = {}
                self.optreqidinfo = {}
                self.opthasdel = {}
                self.opthaonotdel = {}
                self.reciveoptdelstatus = {}
                print('+++++++++++++++++++++++++所有批量请求期权Contract Details 数据完成！+++++++++++++++++++++++++')
                PublicOutData = self.reqID

        timer.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)
        global Error
        Error = [reqId, errorCode, errorString]

        global PublicOutData
        if self.req3 and reqId == self.buff2:
            PublicOutData = ['error', reqId, errorCode, errorString]
            self.req3 = False
            self.buff2 = None

        elif self.req1 and reqId == self.buff2:
            PublicOutData = ['error', reqId, errorCode, errorString]
            self.req1 = False
            self.buff2 = None

        elif self.req2 and reqId == self.buff2:
            PublicOutData = ['error', reqId, errorCode, errorString]
            self.req2 = False
            self.buff2 = None

        elif self.req8:
            for susym, suid in self.optreqidinfo.items():
                if reqId in suid.keys():
                    self.opthaonotdel[susym].append(reqId)

    def nextValidId(self, orderId: int):
        print('nextValidId:', orderId)


        global NextValidId
        NextValidId = orderId

        global InitDone
        if not InitDone:
            InitDone = True

        if not self.start:
            self.start = True
            self.scan()

        if self.req0:
            global PublicOutData
            PublicOutData = orderId
            self.req0 = False

    def managedAccounts(self, accountsList: str):
        print(accountsList)
        global AccountsList
        AccountsList = accountsList

        global AcctDone
        if not AcctDone:
            AcctDone = True

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        print('----------------账户{}信息-------------------'.format(accountName))
        print('key:', key, ' Value:', val, ' Currency:', currency, ' Account Name:', accountName)

        AccountValue = {'key': key, 'Value': val, 'Currency': currency, 'Account Name': accountName}
        global UpdateAccountValues
        UpdateAccountValues[(key, currency)] = AccountValue

        if self.req5:
            kid = len(self.buff['AccountValue'])
            self.buff['AccountValue'][kid] = AccountValue

    def updateAccountTime(self, timeStamp: str):
        print('-----------------时间戳---------------------')
        print(timeStamp)

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        print('-------------------------账户{}组合信息---------------------------'.format(accountName))
        print('contract:', contract, ' position:', position, ' marketPrice:', marketPrice, ' marketValue:', marketValue,
              ' averageCost:', averageCost, ' unrealizedPNL:', unrealizedPNL, ' realizedPNL:', realizedPNL, ' accountName:', accountName)

        Portfolio = {'contract': contract, 'position': position, 'marketPrice': marketPrice,
                                           'marketValue': marketValue, 'averageCost': averageCost,
                                           'unrealizedPNL': unrealizedPNL, 'realizedPNL': realizedPNL, 'accountName': accountName}
        global UpdatePortfolio
        UpdatePortfolio[contract.conId] = Portfolio
        if self.req5:
            kid = len(self.buff['Portfolio'])
            self.buff['Portfolio'][kid] = Portfolio

    def accountDownloadEnd(self, accountName: str):
        print('---------------账户{}更新完毕------------------'.format(accountName))
        if self.req5:
            # self.reqAccountUpdates(False, self.buff2)
            global PublicOutData
            PublicOutData = deepcopy(self.buff)
            self.buff = None
            self.buff2 = None
            self.req5 = False

    def position(self, account:str, contract:Contract, position:float, avgCost:float):
        print('---------------账户{}头寸------------------'.format(account))
        print('contract:', contract, ' position:', position, ' avgCost:', avgCost)

        if self.req9:
            if account not in self.buff.keys():
                self.buff[account] = {}
            kid = len(self.buff[account])
            self.buff[account][kid] = {'contract': contract, 'position': position, 'avgCost': avgCost}

    def positionEnd(self):
        print('---------------头寸下载完毕------------------')
        if self.req9:
            global PublicOutData
            self.req9 = False
            self.cancelPositions()
            self.control_reqtime_gap_2()
            PublicOutData = self.buff
            self.buff = None

    def reqOptionContractDetails_bulk(self, params: dict):
        for sym, para in params.items():

            self.optreqidinfo[sym] = {}
            optdelfile = ospath + os.sep + sym + '-specs.json'
            if os.path.exists(optdelfile):
                self.superoptdel[sym] = Json_to_Dict(optdelfile)
            else:
                self.superoptdel[sym] = {}
            self.opthasdel[sym] = []
            self.opthaonotdel[sym] = []
            self.reciveoptdelstatus[sym] = False

            for parai in para:
                exs = parai[0]
                strs = parai[1]
                if len(exs) != 0 and len(strs) != 0:
                    for ei in exs:
                        for si in strs:
                            self.reqID += 1
                            con_C = make_contract(symbol=sym, secType='OPT', right='C', lastTradeDateOrContractMonth=ei, strike=si)
                            self.optsupercon.append((self.reqID, deepcopy(con_C)))
                            self.optreqidinfo[sym][self.reqID] = [sym, ei, si, 'C']

                            self.reqID += 1
                            con_P = make_contract(symbol=sym, secType='OPT', right='P', lastTradeDateOrContractMonth=ei, strike=si)
                            self.optsupercon.append((self.reqID, deepcopy(con_P)))
                            self.optreqidinfo[sym][self.reqID] = [sym, ei, si, 'P']

        self.req8 = True
        for coi in self.optsupercon:
            self.reqContractDetails(coi[0], coi[1])
            print(coi[0], '批量请求期权Contract Details 数据：', coi[1].__str__())
            self.control_reqtime_gap_2()

        self.optsupercon = []

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.__str__())

        if self.req1 and reqId == self.buff2:
            global PublicOutData
            PublicOutData = deepcopy(['contractDetails', reqId, contractDetails])
            self.req1 = False
            self.buff2 = None
        elif self.req8:
            for susym, suid in self.optreqidinfo.items():
                if reqId in suid.keys():
                    info = suid[reqId]
                    if info[1] not in self.superoptdel[susym]:
                        self.superoptdel[susym][info[1]] = {}
                        self.superoptdel[susym][info[1]]['C'] = {}
                        self.superoptdel[susym][info[1]]['P'] = {}
                    self.superoptdel[susym][info[1]][info[3]][info[2]] = Contract_to_Dict(deepcopy(contractDetails.contract))
                    self.opthasdel[susym].append(reqId)

    def contractDetailsEnd(self, reqId: int):
        pass

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        global openOrder
        openOrder[orderId] = {'orderId': orderId, 'contract': contract, 'order': order, 'orderState': orderState}
        if self.req4:
            kid = len(self.buff['openOrder'])
            self.buff['openOrder'][kid] = {'orderId': orderId, 'contract': contract, 'order': order, 'orderState': orderState}

        elif self.req3 and orderId == self.buff2:
            global PublicOutData
            PublicOutData = {'openOrderType': 'Place Order', 'orderId': orderId, 'contract': contract, 'order': order, 'orderState': orderState}
            self.req3 = False
            self.buff2 = None

        print('-----------------openOrder-------------------')
        print('orderId', orderId, ' contract', contract, ' order', order)
        print_Order_State(orderState)

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        global orderStatus
        orderStatus[orderId] = {'orderId': orderId, 'status': status, 'filled': filled, 'remaining': remaining,
                                              'avgFillPrice': avgFillPrice, 'permId': permId, 'parentId': parentId,
                                              'lastFillPrice': lastFillPrice, 'clientId': clientId, 'whyHeld': whyHeld,
                                              'mktCapPrice': mktCapPrice}

        print('-----------------orderStatus-------------------')
        print('orderId', orderId, ' status', status, ' filled', filled, ' remaining', remaining,
                                              ' avgFillPrice', avgFillPrice, ' permId', permId, ' parentId', parentId,
                                              ' lastFillPrice', lastFillPrice, ' clientId', clientId, ' whyHeld', whyHeld,
                                              ' mktCapPrice', mktCapPrice)

        if self.req4:
            kid = len(self.buff['orderStatus'])
            self.buff['orderStatus'][kid] = {'orderId': orderId, 'status': status, 'filled': filled, 'remaining': remaining,
                                              'avgFillPrice': avgFillPrice, 'permId': permId, 'parentId': parentId,
                                              'lastFillPrice': lastFillPrice, 'clientId': clientId, 'whyHeld': whyHeld,
                                              'mktCapPrice': mktCapPrice}

    def openOrderEnd(self):
        print('OpenOrder 完毕！')
        if self.req4:
            global PublicOutData
            self.req4 = False
            PublicOutData = self.buff
            self.buff = None

    def orderBound(self, reqId: int, apiClientId: int, apiOrderId: int):
        print('OrderBound 被激活++++++++++++++++++++++++')

    def completedOrder(self, contract:Contract, order:Order, orderState:OrderState):
        print('---------------已完成的订单------------------')
        print('contract:', contract, 'order:', order)
        print_Order_State(orderState)

        if self.req10:
            kid = len(self.buff)
            self.buff[kid] = {'contract': contract, 'order': order, 'orderState': orderState}

    def completedOrdersEnd(self):
        print('---------------已完成的订单下载完毕------------------')
        if self.req10:
            self.req10 = False
            global PublicOutData
            PublicOutData = self.buff
            self.buff = None

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str,
                                          multiplier: str, expirations: SetOfString, strikes: SetOfFloat):
        if self.req2 and reqId == self.buff2:
            if exchange == 'SMART':
                print('获取{}期权参数'.format(underlyingConId))
                global PublicOutData
                PublicOutData = ['securityDefinitionOptionParameter', reqId, exchange, underlyingConId, tradingClass,
                                 multiplier, expirations, strikes]
                self.req2 = False
                self.buff2 = None

    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print('期权Params获取结束！')

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if self.req7 and self.buff2 == reqId:
            if tickType == 66:
                self.MKTdatabuff['Bid'] = price
            elif tickType == 67:
                self.MKTdatabuff['Ask'] = price
            elif tickType == 68:
                self.MKTdatabuff['Last'] = price
            elif tickType == 72:
                self.MKTdatabuff['High'] = price
            elif tickType == 73:
                self.MKTdatabuff['Low'] = price
            elif tickType == 75:
                self.MKTdatabuff['Close'] = price
            elif tickType == 76:
                self.MKTdatabuff['Open'] = price

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        if self.req7 and self.buff2 == reqId:
            if tickType == 69:
                self.MKTdatabuff['Bid Size'] = size
            elif tickType == 70:
                self.MKTdatabuff['Ask Size'] = size
            elif tickType == 71:
                self.MKTdatabuff['Last Size'] = size
            elif tickType == 74:
                self.MKTdatabuff['Vol'] = size
            elif tickType == 21:
                self.MKTdatabuff['AvgVol'] = size

    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        if self.req7 and self.buff2 == reqId:
            if tickType == 24:
                self.MKTdatabuff['IV'] = value


class myIB_Thread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        app = myClient_m()
        app.connect('127.0.0.1', 7497, 1)
        app.run()


class myIB_Pro_Client():
    def __init__(self):
        self.IbThread = myIB_Thread()
        self.IbThread.start()
        self.sacnThread = Update_Values_Thread(Pclient=self)
        self.lock = Lock()
        self.Account = ''
        self.dyInitMoney = 0
        self.AccountValues = {}
        self.Positions = {}
        self.nextValidId = 0
        self.TWSsymbols = ['QO', 'IAU', 'GC']
        self.APIcapitalover = False
        self.InitMoney = 0
        self.TWScapital = 0
        self.APIcapital = 0
        self.API_singleSymbolPos = {}
        self.API_singleSymbolPosStat = {}

    def updateAcct_Pos_2(self):
        self.lock.acquire()
        global UpdatePortfolio, UpdateAccountValues
        TWScapital = 0
        cash = float(UpdateAccountValues[('TotalCashValue', 'USD')]['Value'])
        noncash = 0
        longlist = []
        shortlist = []
        for v in UpdatePortfolio.values():
            if v['position'] != 0:
                if v['contract'].symbol in self.TWSsymbols:
                    TWScapital += (int(v['position']) * float(v['averageCost']))
                else:
                    longcondition = (v['contract'].secType == 'STK' and v['position'] > 0) or (v['contract'].secType == 'OPT' and v['contract'].right == 'C' and v['position'] < 0) or (v['contract'].secType == 'OPT' and v['contract'].right == 'P' and v['position'] > 0)
                    if longcondition:
                        longlist.append(v)
                    else:
                        shortlist.append(v)

            symbol = v['contract'].symbol
            if symbol not in self.API_singleSymbolPos.keys():
                self.API_singleSymbolPos[symbol] = {}
                self.API_singleSymbolPosStat[symbol] = {}
                self.API_singleSymbolPosStat[symbol]['CurrentCapital'] = 0
                self.API_singleSymbolPosStat[symbol]['MaxCapital'] = 0
                self.API_singleSymbolPosStat[symbol]['CapitalRatio'] = 0

            self.API_singleSymbolPos[symbol][v['contract'].conId] = v

            noncash += (int(v['position']) * float(v['averageCost']))
        dyInitMoney = cash + noncash

        longvalue = 0
        shortvalue = 0
        for li in longlist:
            longvalue += (int(li['position']) * float(li['averageCost']))
        for si in shortlist:
            shortvalue += (int(si['position']) * float(si['averageCost']))
        APIcapital = longvalue + abs(shortvalue)

        self.TWScapital = TWScapital
        self.APIcapital = APIcapital
        self.dyInitMoney = dyInitMoney

        self.lock.release()
        if APIcapital >= dyInitMoney * 2.5 * 0.8 and not self.APIcapitalover:
            self.APIcapitalover = True
        if APIcapital <= dyInitMoney * 2 * 0.8 and self.APIcapitalover:
            self.APIcapitalover = False

        if self.APIcapitalover:
            self.CancelAllOrders()

    def CancelAllOrders(self):
        self.lock.acquire()
        global orderStatus
        willcancelIds = []
        for v in orderStatus.values():
            if v['parentId'] != 0 and v['status'] == 'Submitted':
                pass
            elif v['parentId'] == 0 and v['filled'] != 0:
                pass
            elif v['status'] == 'Cancelled':
                pass
            else:
                willcancelIds.append(v['orderId'])
        self.lock.release()
        if len(willcancelIds) > 0:
            print('资金使用已达上限！暂停，并撤销未成交订单.....')
            for i in willcancelIds:
                self.cancelOrder(i)

    def updateAcct_Pos(self):
        data = self.reqAccountUpdates(True, self.Account)
        self.AccountValues = data['AccountValue']
        self.Positions = data['Portfolio']
        cash = 0
        for v in self.AccountValues.values():
            if v['key'] == 'TotalCashValue' and v['Currency'] == 'USD':
                cash = float(v['Value'])
                break
        noncash = 0
        for v in self.Positions.values():
            if v['position'] != 0:
                noncash += (int(v['position']) * float(v['averageCost']))

        self.InitMoney = cash + noncash

        return self.InitMoney

    def update_dyInitMoney(self):
        global UpdateAccountValues, UpdatePortfolio
        cash = float(UpdateAccountValues[('TotalCashValue', 'USD')]['Value'])
        noncash = 0
        for v in UpdatePortfolio.values():
            noncash += int(v['position']) * float(v['averageCost'])
        dyInitMoney = cash + noncash
        return dyInitMoney

    def waitapidone(self):
        global InitDone
        global AcctDone
        global AccountsList
        global NextValidId
        while not (InitDone and AcctDone):
            time.sleep(0.05)
        self.Account = AccountsList
        self.nextValidId = NextValidId
        self.updateAcct_Pos()
        self.reqOpenOrders()
        self.sacnThread.start()
        print('API初始化完成！')

    def reqIds(self):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 0
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = PublicOutData
                self.nextValidId = PublicOutData
                PublicOutData = None
                return rdata

    def reqContractDetails(self, reqId: int, contract: Contract):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 1
        rd['reqId'] = reqId
        rd['contract'] = contract
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqSecDefOptParams(self, reqId: int, underlyingSymbol: str, futFopExchange: str, underlyingSecType: str,
                           underlyingConId: int):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 2
        rd['parameters'] = [reqId, underlyingSymbol, futFopExchange, underlyingSecType, underlyingConId]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def placeOrder(self, orderId: OrderId, contract: Contract, order: Order):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 3
        rd['parameters'] = [orderId, contract, order]

        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqOpenOrders(self):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 4
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqAccountUpdates(self, subscribe: bool, acctCode: str):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 5
        rd['parameters'] = [subscribe, acctCode]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def cancelOrder(self, orderId: OrderId):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 6
        rd['parameters'] = [orderId]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqMktData(self, reqId: TickerId, contract: Contract, genericTickList: str, snapshot: bool,
                   regulatorySnapshot: bool, mktDataOptions: TagValueList):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 7
        rd['parameters'] = [reqId, contract, genericTickList, snapshot, regulatorySnapshot, mktDataOptions]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqOptionContractDetails_bulk(self, params: dict):
        global PublicInData
        global PublicOutData
        st = datetime.now()
        rd = {}
        rd['funcID'] = 8
        rd['parameters'] = [params]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                diff = (datetime.now() - st).seconds
                print('共耗时{}秒！'.format(diff))
                return rdata

    def reqPositions(self):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 9
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata

    def reqCompletedOrders(self, apiOnly: bool):
        global PublicInData
        global PublicOutData
        rd = {}
        rd['funcID'] = 10
        rd['parameters'] = [apiOnly]
        PublicInData = rd
        while True:
            if not (PublicOutData is None):
                rdata = deepcopy(PublicOutData)
                PublicOutData = None
                return rdata


class Update_Values_Thread(Thread):
    def __init__(self, Pclient: myIB_Pro_Client):
        Thread.__init__(self)
        self.client = Pclient

    def run(self):
        while True:
            self.client.updateAcct_Pos_2()
            time.sleep(0.5)


def Dict_to_Json(data: dict, jfile: str):
    jf = open(jfile, 'w')
    json.dump(data, jf)
    jf.close()
    print('写入json文件：', jfile)


def Json_to_Dict(jfile: str):
    jf = open(jfile, 'r')
    data = json.load(jf)
    jf.close()
    print('读取json文件：', jfile)
    return data


def Dict_to_Contract(data: dict):
    con = Contract()
    con.symbol = data['symbol']
    con.conId = data['conID']
    con.secType = data['secType']
    con.currency = data['currency']
    con.exchange = data['exchange']
    con.primaryExchange = data['primaryExchange']
    con.multiplier = data['multiplier']
    con.tradingClass = data['tradingClass']
    con.localSymbol = data['localSymbol']
    con.right = data['right']
    con.lastTradeDateOrContractMonth = data['lastTradeDateOrContractMonth']
    con.strike = data['strike']
    return con


def Contract_to_Dict(con: Contract):
    condict = {'symbol': con.symbol,
               'conID': con.conId,
               'secType': con.secType,
               'currency': con.currency,
               'exchange': con.exchange,
               'primaryExchange': con.primaryExchange,
               'multiplier': con.multiplier,
               'tradingClass': con.tradingClass,
               'localSymbol': con.localSymbol,
               'right': con.right,
               'lastTradeDateOrContractMonth': con.lastTradeDateOrContractMonth,
               'strike': con.strike}
    return condict


def make_combo_Switch(underlying: Contract, call: Contract, put: Contract):

    underlyingleg = ComboLeg()
    underlyingleg.conId = underlying.conId
    underlyingleg.ratio = 100
    underlyingleg.action = 'BUY'
    underlyingleg.exchange = 'SMART'

    Pleg = ComboLeg()
    Pleg.ratio = 1
    Pleg.action = 'BUY'
    Pleg.exchange = 'SMART'
    Pleg.conId = put.conId

    Cleg = ComboLeg()
    Cleg.ratio = 1
    Cleg.action = 'SELL'
    Cleg.exchange = 'SMART'
    Cleg.conId = call.conId

    contract = Contract()
    contract.symbol = underlying.symbol
    contract.secType = 'BAG'
    contract.currency = 'USD'
    contract.exchange = 'SMART'
    contract.comboLegs = []
    contract.comboLegs.append(underlyingleg)
    contract.comboLegs.append(Pleg)
    contract.comboLegs.append(Cleg)

    return contract


def make_combo_Box(call_H: Contract, put_H: Contract, call_L: Contract, put_L: Contract):

    Pleg_H = ComboLeg()
    Pleg_H.ratio = 1
    Pleg_H.action = 'SELL'
    Pleg_H.exchange = 'SMART'
    Pleg_H.conId = put_H.conId

    Cleg_H = ComboLeg()
    Cleg_H.ratio = 1
    Cleg_H.action = 'BUY'
    Cleg_H.exchange = 'SMART'
    Cleg_H.conId = call_H.conId

    Pleg_L = ComboLeg()
    Pleg_L.ratio = 1
    Pleg_L.action = 'BUY'
    Pleg_L.exchange = 'SMART'
    Pleg_L.conId = put_L.conId

    Cleg_L = ComboLeg()
    Cleg_L.ratio = 1
    Cleg_L.action = 'SELL'
    Cleg_L.exchange = 'SMART'
    Cleg_L.conId = call_L.conId

    contract = Contract()
    contract.symbol = call_H.symbol
    contract.secType = 'BAG'
    contract.currency = 'USD'
    contract.exchange = 'SMART'
    contract.comboLegs = []
    contract.comboLegs.append(Cleg_H)
    contract.comboLegs.append(Pleg_H)
    contract.comboLegs.append(Cleg_L)
    contract.comboLegs.append(Pleg_L)

    return contract


def make_order(action='BUY', quantity=1, limitPrice=0, orderType='LMT', parentId=0, transmit=False):
    order = Order()
    order.action = action
    order.totalQuantity = quantity
    order.lmtPrice = limitPrice
    order.orderType = orderType
    order.parentId = parentId
    order.transmit = transmit

    return order


def Check_Fix_Order(app: myIB_Pro_Client):
    oOs = app.reqOpenOrders()
    adjoOs = {}
    unkownIDs = []
    checkedIDs = []
    for v in oOs[['openOrder']].values():
        adjoOs[v['orderId']] = v
        if v['order'].parentId != 0:
            checkedIDs.append(v['order'].parentId)
        else:
            unkownIDs.append(v['orderId'])
    uncompIDs = []
    for i in unkownIDs:
        if i not in checkedIDs:
            uncompIDs.append(i)

    if len(uncompIDs) > 0:
        for uni in uncompIDs:
            combo = adjoOs[uni]['contract']
            order = adjoOs[uni]['order']
            strconId = 0
            symbol = combo.symbol
            for cl in combo.comboLegs:
                if cl.ratio == 1 or cl.ratio == 1:
                    strconId = cl.conId
                    break


def check_delete_bad_specs():
    specsfilelist = os.listdir(ospath)
    deletedsymbols = []
    for si in specsfilelist:
        symbol = si.split('-')[0]
        filename = ospath + os.sep + si
        paramsfilename = oppath + os.sep + symbol + '-params.json'
        try:
            jd = Json_to_Dict(filename)
            for month, mv in jd.items():
                sc = list(sorted(list(mv['C'].keys())))
                sp = list(sorted(list(mv['P'].keys())))
                if sc != sp:
                    os.remove(filename)
                    os.remove(paramsfilename)
                    print('删除残缺文件：', filename)
                    deletedsymbols.append(symbol)
                    break
        except:
            os.remove(filename)
            os.remove(paramsfilename)
            print('删除残缺文件：', filename)
            deletedsymbols.append(symbol)
    return deletedsymbols



# from IB_Utils_2 import Pick_Underlyings
# from IB_Utils import pick_stricks_2, IBdate_to_Date

if __name__ == '__main__':

    udpath = r'E:\newdata\IB data\Underlying Details'
    oppath = r'E:\newdata\IB data\Option Params 2'
    ospath = r'E:\newdata\IB data\Option Specs'

    udfilelist = os.listdir(udpath)
    osfilelist = os.listdir(ospath)

    app = myIB_Pro_Client()
    app.waitapidone()

    underlyingsdf = Pick_Underlyings(picknum=100, greatVOL=100000)
    usymbols = list(underlyingsdf['金融产品'])
    uIVs = list(underlyingsdf['期权隐含波动率'])
    uLastes = list(underlyingsdf['最后价'])

    underliysDetails = {}
    optionParams = {}
    missedusymbols = []
    #
    # reqId = 0
    # for si in usymbols:
    #     sifile = si + '-Details.json'
    #     if sifile not in udfilelist:
    #         con = make_contract(si)
    #         condel = app.reqContractDetails(reqId, con)
    #         reqId += 1
    #         if condel[0] == 'contractDetails':
    #             ucon = deepcopy(condel[2].contract)
    #             savefile = udpath + os.sep + sifile
    #             Dict_to_Json(Contract_to_Dict(ucon), savefile)
    #         else:
    #             missedusymbols.append(si)
    #
    lessdays = 120
    today = date.today()
    # for si in usymbols:
    #     if si not in missedusymbols:
    #         udfile = udpath + os.sep + si + '-Details.json'
    #         ucon = Dict_to_Contract(Json_to_Dict(udfile))
    #         optparam = app.reqSecDefOptParams(reqId, si, '', 'STK', ucon.conId)
    #         reqId += 1
    #         if optparam[0] == 'securityDefinitionOptionParameter':
    #             # optionParams[si] = {}
    #             exs = deepcopy(optparam[-2])
    #             strs = deepcopy(optparam[-1])
    #             idx = usymbols.index(si)
    #             last = uLastes[idx]
    #             saveexs = []
    #             for exi in exs:
    #                 exid = IBdate_to_Date(exi)
    #                 if (exid - today).days <= lessdays:
    #                     saveexs.append(exi)
    #             savestrs = []
    #             rio = 0.1
    #             lastdiff = last - 100
    #             if lastdiff < 0:
    #                 rio = (abs(lastdiff) / 80 + 1) * 0.1
    #             for stri in strs:
    #                 if (1 - rio) * last <= stri <= (1 + rio) * last:
    #                     savestrs.append(stri)
    #             saveexs = list(sorted(saveexs))
    #             savestrs = list(sorted(savestrs))
    #             saveParams = {'strikes': savestrs, 'expirations': saveexs}
    #             opfile = oppath + os.sep + si + '-params.json'
    #
    #             pickedparams = []
    #             if os.path.exists(opfile):
    #                 lastopfile = Json_to_Dict(opfile)
    #                 inexs = []
    #                 outexs = []
    #                 instrs = []
    #                 outstrs = []
    #
    #                 lexs = []
    #                 for i in lastopfile['expirations']:
    #                     if i >= saveexs[0]:
    #                         lexs.append(i)
    #
    #                 for exi2 in saveexs:
    #                     if exi2 not in lexs:
    #                         outexs.append(exi2)
    #                     else:
    #                         inexs.append(exi2)
    #                 for stri2 in savestrs:
    #                     if stri2 not in lastopfile['strikes']:
    #                         outstrs.append(stri2)
    #                     else:
    #                         instrs.append(stri2)
    #                 pickedparams = [(outexs, instrs), (inexs, outstrs), (outexs, outstrs)]
    #             else:
    #                 pickedparams = [(saveexs, savestrs)]
    #             optionParams[si] = pickedparams
    #
    #             Dict_to_Json(saveParams, opfile)
    #
    #         else:
    #             missedusymbols.append(si)
    # #
    # # # testfile = r'E:\newdata\IB data\test1.json'
    # # # Dict_to_Json(optionParams, testfile)
    # #
    # reqId = app.reqOptionContractDetails_bulk(optionParams)

    # oOs = app.reqOpenOrders()['openOrder']
    deletedsymbols = check_delete_bad_specs()
    missedusymbols += deletedsymbols
    ChrOrders = []
    for si in usymbols:
        if si not in missedusymbols:
            if app.APIcapitalover:
                break
            try:
                udfile = udpath + os.sep + si + '-Details.json'
                uddict = Json_to_Dict(udfile)
                udc = Dict_to_Contract(uddict)
                osfile = ospath + os.sep + si + '-specs.json'
                osdict = Json_to_Dict(osfile)
            except:
                print('读取{}失败！'.format(si))
                continue

            # cancelIds = []
            # for oi in oOs.values():
            #     if oi['contract'].symbol == si and oi['order'].parentId == 0:
            #         cancelIds.append(oi['orderId'])

            app.lock.acquire()
            # global orderStatus, openOrder
            willcancelIds = []
            for k, v in orderStatus.items():
                if openOrder[k]['contract'].symbol == si:
                    if v['parentId'] != 0 and v['status'] == 'Submitted':
                        pass
                    elif v['parentId'] == 0 and v['filled'] != 0:
                        pass
                    elif v['status'] == 'Cancelled':
                        pass
                    else:
                        willcancelIds.append(v['orderId'])
            app.lock.release()

            for oid in willcancelIds:
                app.cancelOrder(oid)

            idx = usymbols.index(si)
            last = uLastes[idx]
            IV = uIVs[idx]
            strsnum = 2
            if IV >= 0.6:
                strsnum = round(IV / 0.6) + 2

            for month, osdata in osdict.items():
                if app.APIcapitalover:
                    break
                if IBdate_to_Date(month) > today:
                    osstrs = list(osdata['C'].keys())
                    osstrs_2 = [float(i) for i in osstrs]
                    pickedstrs = pick_stricks_2(last, osstrs_2, strsnum)

                    for psi in pickedstrs:
                        if app.APIcapitalover:
                            break
                        call = Dict_to_Contract(osdict[month]['C'][str(psi)])
                        put = Dict_to_Contract(osdict[month]['P'][str(psi)])
                        combo = make_combo_Switch(udc, call, put)

                        discountPrice = psi * 0.05
                        idiff = IV / 0.8
                        if idiff > 1:
                            discountPrice = idiff * 0.05 * psi
                        if discountPrice > 0.1 * psi:
                            discountPrice = 0.1 * psi
                        if discountPrice < 0.5:
                            discountPrice = 0.5

                        limitPrice = 0
                        if psi >= last:
                            limitPrice = round(psi - discountPrice, 2)
                        else:
                            limitPrice = round(psi + discountPrice, 2)

                        quantity = round(app.dyInitMoney * 0.8 * 2.5 / (50 * limitPrice * 100))

                        if quantity > 0:
                            action = 'BUY'
                            if psi < last:
                                action = 'SELL'
                            Parorder = make_order(action=action, quantity=quantity, limitPrice=limitPrice)
                            porderId = app.reqIds()
                            ops = app.placeOrder(porderId, combo, Parorder)
                            print(porderId, '发送父订单：{}, 组合： {}'.format(Parorder, combo))
                            if action == 'BUY':
                                action = 'SELL'
                            else:
                                action = 'BUY'
                            Chrorder = make_order(action=action, quantity=quantity, limitPrice=psi, transmit=True)
                            Chrorder.parentId = porderId
                            ChrOrders.append((deepcopy(Chrorder), deepcopy(combo)))

    for ci in ChrOrders:
        if app.APIcapitalover:
            break
        chrId = app.reqIds()
        app.placeOrder(chrId, ci[1], ci[0])
        print(chrId, '发送子订单：{}, 组合： {}'.format(ci[1], ci[0]))



    pass























































