# from ibapi.client import EClient
# from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.common import *
from ibapi.scanner import ScannerSubscription, ScanData
from ibapi.ticktype import *
import pandas as pd
from threading import Timer, Thread, Lock
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from IB_Utils import contract_to_df, _myClient, make_contract, print_Order_State, IBdate_to_Date
from IB_Utils_3 import Contract_to_Dict, Dict_to_Contract, Dict_to_Json, Json_to_Dict
import time
import json
import math
import sys
import os

# from IB_Utils_4_1 import check_delete_bad_specs

UDpath = r'E:\newdata\IB data\Underlying Details'
OPpath = r'E:\newdata\IB data\Option Params 2'
OSpath = r'E:\newdata\IB data\Option Specs'


class myClient_m_2(_myClient):
    def __init__(self, ProClient, UDdf: pd.DataFrame):  #: myIB_Pro_Client_2
        _myClient.__init__(self)
        self.ProClient = ProClient
        self.timegapstart = datetime.now()
        self.UDdf = UDdf
        self.dfsymbols = list(self.UDdf['金融产品'])
        self.dfIVs = list(self.UDdf['期权隐含波动率'])
        self.dfPrice = list(self.UDdf['最后价'])

        self.excludesymbols_P = ['HYLN', 'SHLL']
        self.excludesymbols_O = []

        self.reqID = 0
        self.NextValidID = 0
        self.account = ''
        self._AccontValue = {}
        self._Position = {}
        self._OrderStatus = {}
        self._OpenOrder = {}

        self.AccontValue_details = {}
        self.Position_details = {}
        self.Position_details_exc = {}
        self.OpenOrder_details = {}

        self.nextIdDone = False
        self.accountDone = False
        self.Init_Accot_Pos_OO_OS = False
        self.accountDownloadDone = False
        self.openOrderDone = False
        self.Init_Accot_Pos_OO_OS_Done = False

        self.req0 = False
        self.req1 = False
        self.req2 = False
        self.req4 = False
        self.req5 = False

        self.contractDetails_STK_batch_buff = {}
        self.contractDetails_STK_batch_ID_buff = []
        self.contractDetails_STK_batch_eorr_ID_buff = []

        self.OPT_Params_reqIDs = {}
        self.OPT_Params_recivedIDs = []
        self.OPT_Params_error_reqIDs = []
        self.OPT_Params = {}

        self.pick_OPT_strickes_paramters = {}

        self.existed_OPT_details = {}
        self.OPT_Detail_reqIDs = {}
        self.OPT_Detail_recived_IDs = {}
        self.OPT_Detail_error_IDs = {}
        self.OPT_Detail_Done = {}

        self.Scan_Timer = Timer(0.1, self.Scan)

    def control_reqtime_gap(self):
        now = datetime.now()
        timegap = (now - self.timegapstart).microseconds
        resttime = 21000 - timegap
        if resttime > 0:
            print('机器过热， 休息{}秒...'.format(resttime / 1000000))
            time.sleep(resttime / 1000000)
        self.timegapstart = datetime.now()

    def Scan(self):
        pn = 0
        while True:
            pn += 1
            if pn >= 50:
                now = datetime.now()
                print(now.__str__(), 'Scan运行中.....')
                pn = 0
            time.sleep(0.1)
            if self.nextIdDone and self.accountDone:
                if not self.Init_Accot_Pos_OO_OS:
                    self.reqAccountUpdates(True, self.account)
                    self.control_reqtime_gap()
                    self.reqOpenOrders()
                    self.control_reqtime_gap()
                    self.Init_Accot_Pos_OO_OS = True

            if self.openOrderDone and self.accountDownloadDone:
                if not self.Init_Accot_Pos_OO_OS_Done:
                    self.Init_Accot_Pos_OO_OS_Done = True

            if self.Init_Accot_Pos_OO_OS_Done:
                sposbuff = {}
                _Position_details = {}
                _Position_details_exc = {}
                for oid, pos in self._Position.items():
                    if pos['position'] != 0:
                        symbol = pos['contract'].symbol
                        if symbol not in self.excludesymbols_P:
                            if symbol not in _Position_details.keys():
                                _Position_details[symbol] = {'underlying': {}, 'option': {}}
                            if symbol not in sposbuff.keys():
                                sposbuff[symbol] = {}
                            sposbuff[symbol][oid] = pos
                            if pos['contract'].secType == 'STK':
                                _Position_details[symbol]['underlying'][oid] = pos
                            else:
                                month = pos['contract'].lastTradeDateOrContractMonth
                                strike = pos['contract'].strike
                                sorder = (month, strike)
                                if sorder not in _Position_details[symbol]['option'].keys():
                                    _Position_details[symbol]['option'][sorder] = {}
                                _Position_details[symbol]['option'][sorder][oid] = pos
                        else:
                            _Position_details_exc[oid] = pos
                self.Position_details = _Position_details
                self.Position_details_exc = _Position_details_exc
                self.ProClient.Position_details = _Position_details
                self.ProClient.Position_details_exc = _Position_details_exc

                _AccontValue_details = {}
                _AccontValue_details['API_Capital_Class'] = {}
                ttcapital = 0
                absttcapital = 0
                for symi, poi in sposbuff.items():
                    capital = 0
                    for cid, poii in poi.items():
                        capital += float(poii['position']) * float(poii['averageCost'])

                    _AccontValue_details['API_Capital_Class'][symi] = capital
                    ttcapital += capital
                    absttcapital += abs(capital)
                _AccontValue_details['ABS_API_Capital'] = absttcapital

                _AccontValue_details['exclude_Capital'] = 0
                for coi, poi in self.Position_details_exc.items():
                    _AccontValue_details['exclude_Capital'] += float(poi['position']) * float(poi['averageCost'])

                _AccontValue_details['Total_Cash'] = float(self._AccontValue[('TotalCashBalance', 'BASE')]['Value'])
                _AccontValue_details['Total_Init_Capital'] = ttcapital + _AccontValue_details['exclude_Capital'] +\
                                                                _AccontValue_details['Total_Cash']
                self.AccontValue_details = _AccontValue_details
                self.ProClient.AccontValue_details = _AccontValue_details

                _OpenOrder_details = {}
                _OpenOrder_details['rmainingOrderIDs'] = []
                _OpenOrder_details['CancelableOrderIDs'] = []
                _OpenOrder_details['CancelableOrderIDs_Class'] = {}
                _OpenOrder_details['SubmittedChildOrderIDs'] = []
                for cid, sta in self._OrderStatus.items():
                    if sta['parentId'] == 0 and sta['status'] == 'Submitted':
                        if sta['filled'] != 0:
                            if cid not in _OpenOrder_details['rmainingOrderIDs']:
                                _OpenOrder_details['rmainingOrderIDs'].append(cid)
                        else:
                            if cid not in _OpenOrder_details['CancelableOrderIDs']:
                                _OpenOrder_details['CancelableOrderIDs'].append(cid)
                            sym = self._OpenOrder[cid]['contract'].symbol
                            if sym not in _OpenOrder_details['CancelableOrderIDs_Class'].keys():
                                _OpenOrder_details['CancelableOrderIDs_Class'][sym] = {'BUY': [], 'SELL': []}
                            action = self._OpenOrder[cid]['order'].action
                            _OpenOrder_details['CancelableOrderIDs_Class'][sym][action].append(cid)
                    elif sta['parentId'] != 0 and sta['status'] == 'Submitted':
                        _OpenOrder_details['SubmittedChildOrderIDs'].append(cid)
                self.OpenOrder_details = _OpenOrder_details
                self.ProClient.OpenOrder_details = _OpenOrder_details

                if not self.ProClient.InitDone:
                    self.ProClient.dfsymbols = list(self.UDdf['金融产品'])
                    self.ProClient.dfIVs = list(self.UDdf['期权隐含波动率'])
                    self.ProClient.dfPrice = list(self.UDdf['最后价'])
                    self.extendFunc()

                    self.ProClient.InitDone = True

            if self.ProClient.InitDone:
                self.extendFunc()

            self.APIfuncs()

            if self.req0:
                if (self.contractDetails_STK_batch_ID_buff.__len__() + self.contractDetails_STK_batch_eorr_ID_buff.__len__())\
                        == self.contractDetails_STK_batch_buff.__len__():

                    rsymbols = []
                    missedsymbols = []
                    for eid in self.contractDetails_STK_batch_eorr_ID_buff:
                        missedsymbols.append(self.contractDetails_STK_batch_buff[eid])
                    for syi in self.dfsymbols:
                        if syi not in missedsymbols:
                            rsymbols.append(syi)

                    self.contractDetails_STK_batch_eorr_ID_buff = []
                    self.contractDetails_STK_batch_ID_buff = []
                    self.contractDetails_STK_batch_buff = {}
                    self.req0 = False
                    self.ProClient.APIreturnValues = rsymbols

            elif self.req1:
                if (self.OPT_Params_recivedIDs.__len__() + self.OPT_Params_error_reqIDs.__len__()) == self.OPT_Params_reqIDs.__len__():
                    self.req1 = False
                    self.OPT_Params_reqIDs = {}
                    self.OPT_Params_recivedIDs = []
                    self.OPT_Params_error_reqIDs = []
                    self.ProClient.APIfuncID = 2

            elif self.req2:
                OPT_All_Done = True
                for sym, id in self.OPT_Detail_reqIDs.items():
                    if not self.OPT_Detail_Done[sym]:
                        if (self.OPT_Detail_recived_IDs[sym].__len__() + self.OPT_Detail_error_IDs[sym].__len__()) == len(id):
                            self.OPT_Detail_Done[sym] = True
                            savefile = OSpath + os.sep + sym + '-specs.json'
                            Dict_to_Json(self.existed_OPT_details[sym], savefile)

                    OPT_All_Done = OPT_All_Done and self.OPT_Detail_Done[sym]

                if OPT_All_Done:
                    self.req2 = False
                    self.pick_OPT_strickes_paramters = {}
                    self.existed_OPT_details = {}
                    self.OPT_Detail_reqIDs = {}
                    self.OPT_Detail_recived_IDs = {}
                    self.OPT_Detail_error_IDs = {}
                    self.OPT_Detail_Done = {}
                    # check_delete_bad_specs(OSpath, OPpath)
                    self.ProClient.APIreturnValues = True

    def extendFunc(self):
        pass

    def APIfuncs(self):
        funcID = self.ProClient.APIfuncID
        parameters = self.ProClient.APIfuncParameters
        self.ProClient.APIfuncID = None
        self.ProClient.APIfuncParameters = None

        if funcID == 0:
            self.reqContract_STK_batch()

        elif funcID == 1:
            self.pick_OPT_strickes_paramters = parameters
            self.reqOPT_Params_Details_batch_1(parameters['symbols'])

        elif funcID == 2:
            self.reqOPT_Params_Details_batch_2()

        elif funcID == 3:
            self.reqCancel_Orders_batch(parameters)

        elif funcID == 4:
            self.Place_Order_batch(parameters)

        elif funcID == 5:
            self.req5 = True
            self.Place_Order_Singal(parameters['orderId'], parameters['contract'], parameters['order'])

    def reqContract_STK_batch(self):
        UDfiles = os.listdir(UDpath)
        reqCSBbuff = []
        for si in self.dfsymbols:
            if si + '-Details.json' not in UDfiles:
                con = make_contract(symbol=si, secType='STK')
                reqCSBbuff.append((self.reqID, deepcopy(con)))
                self.contractDetails_STK_batch_buff[self.reqID] = si
                self.reqID += 1
        self.req0 = True
        for ri in reqCSBbuff:
            self.reqContractDetails(ri[0], ri[1])
            self.control_reqtime_gap()

    def reqOPT_Params_Details_batch_1(self, symbols: list):
        optparamsbuff = []
        for si in symbols:
            if si not in ["DQ", "PINS", "CELH", "GOVT", "FSLY", "FUTU", "TNA", "NVTA", "HYLB", "PAR", "MRNA", "TSLA", "GSX", "RUN", "XPEV", "SWBI", "CVAC", "DKNG", "GRWG", "UVXY", "SPCE", "NIO", "BNTX", "BLI", "OTRK", "PZA", "WKHS"]:
                uddjfile = UDpath + os.sep + si + '-Details.json'
                uddetail = Json_to_Dict(uddjfile)
                conid = int(uddetail['conID'])
                optparamsbuff.append((self.reqID, si, conid))
                self.OPT_Params_reqIDs[self.reqID] = si
                self.reqID += 1
        self.req1 = True
        for oi in optparamsbuff:
            self.reqSecDefOptParams(oi[0], oi[1], '', 'STK', oi[2])
            self.control_reqtime_gap()

    def reqOPT_Params_Details_batch_2(self):
        optdelbuff = []
        for sym, param in self.OPT_Params.items():
            self.OPT_Detail_reqIDs[sym] = {}
            self.OPT_Detail_recived_IDs[sym] = []
            self.OPT_Detail_error_IDs[sym] = []
            self.OPT_Detail_Done[sym] = False

            osfile = OSpath + os.sep + sym + '-specs.json'
            existed_OPT_details_brif = []
            if os.path.exists(osfile):
                self.existed_OPT_details[sym] = Json_to_Dict(osfile)
                for month, rig in self.existed_OPT_details[sym].items():
                    for rigi, st in rig.items():
                        for sti in st.keys():
                            existed_OPT_details_brif.append((sym, month, rigi, sti))
            else:
                self.existed_OPT_details[sym] = {}

            stricklimit = 0.15
            idx = self.dfsymbols.index(sym)
            last = self.dfPrice[idx]
            pdiff = 100 - last
            if pdiff > 0:
                stricklimit = 0.15 + (pdiff / 80) * (self.pick_OPT_strickes_paramters['maxstricklimit'] - 0.15)
            exs = param['expirations']
            strs = param['strikes']

            today = date.today()
            for ei in exs:
                exdate = IBdate_to_Date(ei)
                if (exdate - today).days <= self.pick_OPT_strickes_paramters['lessthanday']:
                    for strsi in strs:
                        if last * (1 - stricklimit) <= strsi <= last * (1 + stricklimit):
                            brif_C = (sym, ei, 'C', strsi)
                            if brif_C not in existed_OPT_details_brif:
                                con_C = make_contract(symbol=sym, secType='OPT', right='C', lastTradeDateOrContractMonth=ei,
                                                      strike=strsi)
                                optdelbuff.append((self.reqID, deepcopy(con_C)))
                                self.OPT_Detail_reqIDs[sym][self.reqID] = brif_C
                                self.reqID += 1

                            brif_P = (sym, ei, 'P', strsi)
                            if brif_P not in existed_OPT_details_brif:
                                con_P = make_contract(symbol=sym, secType='OPT', right='P', lastTradeDateOrContractMonth=ei,
                                                      strike=strsi)
                                optdelbuff.append((self.reqID, deepcopy(con_P)))
                                self.OPT_Detail_reqIDs[sym][self.reqID] = brif_P
                                self.reqID += 1
        self.req2 = True
        # locker = Lock()
        # locker.acquire()
        for oi in optdelbuff:
            self.reqContractDetails(oi[0], oi[1])
            self.control_reqtime_gap()
        # locker.release()

    def reqCancel_Orders_batch(self, orderIds: list):
        for id in orderIds:
            self.cancelOrder(id)
            self.control_reqtime_gap()
        self.ProClient.APIreturnValues = True

    def Place_Order_batch(self, Contrcats_Orders: list):
        self.req4 = True
        for oii in Contrcats_Orders:
            oid = self.NextValidID
            self.placeOrder(oid, oii[0], oii[1])
            print('提交子订单--', oii[0].__str__(), '----', oii[1].__str__())
            self.control_reqtime_gap()
            self.reqIds(-1)
            self.control_reqtime_gap()
            while True:
                if oid < self.NextValidID:
                    break
        self.req4 = False
        self.req5 = False
        self.ProClient.APIreturnValues = self.NextValidID

    def Place_Order_Singal(self, orderId: int, contract: Contract, order: Order):
        self.placeOrder(orderId, contract, order)
        print('提交父订单--', contract.__str__(), '----', order.__str__())
        self.control_reqtime_gap()
        self.reqIds(-1)
        self.control_reqtime_gap()
        while True:
            if orderId < self.NextValidID:
                break
        self.ProClient.APIreturnValues = self.NextValidID

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

        if self.req0:
            if reqId in self.contractDetails_STK_batch_buff.keys():
                self.contractDetails_STK_batch_eorr_ID_buff.append(reqId)

        elif self.req1:
            if reqId in self.OPT_Params_reqIDs.keys():
                self.OPT_Params_error_reqIDs.append(reqId)

        elif self.req2:
            for sym, id in self.OPT_Detail_reqIDs.items():
                if reqId in id.keys():
                    self.OPT_Detail_error_IDs[sym].append(reqId)

    def nextValidId(self, orderId: int):
        print('nextValidId:', orderId)

        self.NextValidID = orderId
        self.ProClient.NextValidID = orderId
        if not self.nextIdDone:
            self.nextIdDone = True
            self.Scan_Timer.start()

    def managedAccounts(self, accountsList: str):
        print(accountsList)

        if not self.accountDone:
            self.accountDone = True
            self.account = accountsList

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        if not self.req4 or not self.req5:
            print('----------------账户{}信息-------------------'.format(accountName))
            print('key:', key, ' Value:', val, ' Currency:', currency, ' Account Name:', accountName)

        AccountValue = {'key': key, 'Value': val, 'Currency': currency, 'Account Name': accountName}
        self.ProClient.AccontValue[(key, currency)] = AccountValue
        self._AccontValue[(key, currency)] = AccountValue

    def updatePortfolio(self, contract: Contract, position: float, marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float, realizedPNL: float, accountName: str):
        if not self.req4 or not self.req5:
            print('-------------------------账户{}组合信息---------------------------'.format(accountName))
            print('contract:', contract, ' position:', position, ' marketPrice:', marketPrice, ' marketValue:', marketValue,
                  ' averageCost:', averageCost, ' unrealizedPNL:', unrealizedPNL, ' realizedPNL:', realizedPNL, ' accountName:', accountName)

        Portfolio = {'contract': contract, 'position': position, 'marketPrice': marketPrice,
                     'marketValue': marketValue, 'averageCost': averageCost,
                     'unrealizedPNL': unrealizedPNL, 'realizedPNL': realizedPNL, 'accountName': accountName}
        self.ProClient.Position[contract.conId] = Portfolio
        self._Position[contract.conId] = Portfolio

    def accountDownloadEnd(self, accountName: str):
        if not self.req4 or not self.req5:
            print('---------------账户{}更新完毕------------------'.format(accountName))

        if not self.accountDownloadDone:
            self.accountDownloadDone = True

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        if not self.req4 or not self.req5:
            print('-----------------openOrder-------------------')
            print('orderId', orderId, ' contract', contract, ' order', order)
            print_Order_State(orderState)

        openOrder = {'orderId': orderId, 'contract': contract, 'order': order, 'orderState': orderState}
        self.ProClient.OpenOrder[orderId] = openOrder
        self._OpenOrder[orderId] = openOrder

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float,
                    permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        if not self.req4 or not self.req5:
            print('-----------------orderStatus-------------------')
            print('orderId', orderId, ' status', status, ' filled', filled, ' remaining', remaining,
                  ' avgFillPrice', avgFillPrice, ' permId', permId, ' parentId', parentId,
                  ' lastFillPrice', lastFillPrice, ' clientId', clientId, ' whyHeld', whyHeld,
                  ' mktCapPrice', mktCapPrice)

        orderStatus = {'orderId': orderId, 'status': status, 'filled': filled, 'remaining': remaining,
                                'avgFillPrice': avgFillPrice, 'permId': permId, 'parentId': parentId,
                                'lastFillPrice': lastFillPrice, 'clientId': clientId, 'whyHeld': whyHeld,
                                'mktCapPrice': mktCapPrice}
        self.ProClient.OrderStatus[orderId] = orderStatus
        self._OrderStatus[orderId] = orderStatus

    def openOrderEnd(self):
        if not self.req4 or not self.req5:
            print('OpenOrder 完毕！')

        if not self.openOrderDone:
            self.openOrderDone = True

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str, underlyingConId: int, tradingClass: str,
                                          multiplier: str, expirations: SetOfString, strikes: SetOfFloat):

        symbol = self.OPT_Params_reqIDs[reqId]
        if symbol not in self.OPT_Params.keys():
            self.OPT_Params[symbol] = {'expirations': expirations, 'strikes': strikes}
        else:
            exs = self.OPT_Params[symbol]['expirations']
            strs = self.OPT_Params[symbol]['strikes']
            exs = exs | expirations
            strs = strs | strikes
            self.OPT_Params[symbol] = {'expirations': exs, 'strikes': strs}

    def securityDefinitionOptionParameterEnd(self, reqId: int):
        if reqId not in self.OPT_Params_recivedIDs:
            self.OPT_Params_recivedIDs.append(reqId)
            print(self.OPT_Params_reqIDs[reqId], '期权参数接收完毕！')

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.__str__())

        if self.req0:
            for id, sym in self.contractDetails_STK_batch_buff.items():
                if id == reqId:
                    savefile = UDpath + os.sep + sym + '-Details.json'
                    Dict_to_Json(Contract_to_Dict(contractDetails.contract), savefile)
                    self.contractDetails_STK_batch_ID_buff.append(reqId)

        elif self.req2:
            for sym, id in self.OPT_Detail_reqIDs.items():
                if reqId in id.keys():
                    month = id[reqId][1]
                    rig = id[reqId][2]
                    strk = id[reqId][3]
                    if month not in self.existed_OPT_details[sym].keys():
                        self.existed_OPT_details[sym][month] = {'C': {}, 'P': {}}
                    self.existed_OPT_details[sym][month][rig][strk] = Contract_to_Dict(contractDetails.contract)
                    self.OPT_Detail_recived_IDs[sym].append(reqId)
