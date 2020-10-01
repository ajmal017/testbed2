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
from threading import Timer
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from copy import deepcopy
import time
import json
import sys
import io
import os

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

def IBdate_to_Date(ibdate: str):
    year = int(ibdate[: 4])
    month = int(ibdate[4: 6])
    day = int(ibdate[6:])
    return date(year, month, day)


def Date_to_IBdate(Ddate: date):
    return Ddate.strftime('%Y%m%d')


# def selectOptions(aboveRdays=7, strikeSpan=0.1):
#     jpath = r'E:\newdata\IB data\Option Params'
#     jfilelist = os.listdir(jpath)
#
#     file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
#     underlying = pd.read_csv(file)
#     eligibleOpt = {}
#     for ji in jfilelist:
#         symbol = ji.split('.')[0]
#         idx = list(underlying['symbol']).index(symbol)
#         last = underlying['Last'][idx]
#         jf = open(jpath + os.sep + ji)
#         jdict = json.load(jf)
#         jf.close()
#
#         for ei in jdict['expirations']:
#             ed = IBdate_to_Date(ei)
#             today = date.today()
#             if ed - today > aboveRdays:
#                 eligibleOpt[ei] = []
#                 for si in jdict['strikes']:
#                     if (1 - strikeSpan) * last < si < (1 + strikeSpan) * last:
#                         eligibleOpt[ei].append((ei, si))
#     return eligibleOpt


def make_contract(symbol='', conID=0, secType='STK', currency='USD', exchange='SMART', primaryExchange='',
               multiplier=100, tradingClass='', localSymbol='', right='', lastTradeDateOrContractMonth='',
               strike=0):
    contract = Contract()
    contract.symbol = symbol
    contract.conId = conID
    contract.secType = secType
    contract.currency = currency
    contract.exchange = exchange
    contract.primaryExchange = primaryExchange
    contract.multiplier = multiplier
    contract.tradingClass = tradingClass
    contract.localSymbol = localSymbol
    contract.right = right
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    contract.strike = strike
    return contract


def contract_to_df(con: Contract):
    condict = {'symbol': [con.symbol],
               'conID': [con.conId],
               'secType': [con.secType],
               'currency': [con.currency],
               'exchange': [con.exchange],
               'primaryExchange': [con.primaryExchange],
               'multiplier': [con.multiplier],
               'tradingClass': [con.tradingClass],
               'localSymbol': [con.localSymbol],
               'right': [con.right],
               'lastTradeDateOrContractMonth': [con.lastTradeDateOrContractMonth],
               'strike': [con.strike]}
    condf = pd.DataFrame(data=condict)
    return condf


def contract_to_dict(con: Contract):
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


def get_price_iex(symbol: str):
    try:
        ticker = Stock(symbol)
        qt = ticker.get_quote()
        price = float(qt['iexRealtimePrice'])
        print(symbol, price)
        return price
    except:
        print(symbol, '获取价格失败！')
        return float('nan')


def update_price():
    file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
    df = pd.read_csv(file)
    symbols = list(df['symbol'])
    last = []
    for si in symbols:
        price = get_price_iex(si)
        last.append(price)
    df['Last'] = last
    df.to_csv(file, index=False)


def full_contracts_generator():
    aboveRdays = 6
    strikeSpan = 0.1
    jpath = r'E:\newdata\IB data\Option Params'

    specpath = r'E:\newdata\IB data\Option Specs'
    specslist = os.listdir(specpath)

    # cons = []
    # for spei in specslist:
    #     symbol = spei.split('-')[0]
    #     jfe = open(specpath + os.sep + spei, 'r')
    #     jfdict = json.load(jfe)
    #     jfe.close()
    #     for month in jfdict.keys():
    #         for strik in jfdict[month]['C'].keys():
    #             cons.append((symbol, month, strik))

    file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
    underlying = pd.read_csv(file)
    non_cons = []
    for spi in specslist:
        symbol = spi.split('-')[0]
        jfile = symbol + '.json'
        jf = open(jpath + os.sep + jfile, 'r')
        jdict = json.load(jf)
        jf.close()
        idx = list(underlying['symbol']).index(symbol)
        last = underlying['Last'][idx]

        for ei in jdict['expirations']:
            ed = IBdate_to_Date(ei)
            today = date.today()
            if (ed - today).days > aboveRdays:
                for si in jdict['strikes']:
                    if (1 - strikeSpan) * last < si < (1 + strikeSpan) * last:
                        u = [symbol, ei, si]
                        non_cons.append(u)

    jnon = open(r'E:\newdata\IB data\Full Contracts.json', 'w')
    json.dump({'Full Contracts': non_cons}, jnon)
    jnon.close()




class _iclient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class _myClient(EWrapper, _iclient):
    def __init__(self):
        EWrapper.__init__(self)
        _iclient.__init__(self, wrapper=self)


class myClient_get_underlying_details(_myClient):
    def __init__(self, symbolslist: list):
        _myClient.__init__(self)
        self.reqConsdict = {}
        self.initdf = True
        self.superdf = ''
        self.recivedreqid = []
        self.non_recivedreqid = []
        self.symbolslist = symbolslist

    def scan(self):
        print('----------------------------')
        timer = Timer(0.2, self.scan)
        reqidnums = list(self.reqConsdict.keys())
        if len(reqidnums) == len(self.recivedreqid + self.non_recivedreqid) and len(reqidnums) > 0:
            if len(self.non_recivedreqid) > 0:
                nonr = [self.reqConsdict[i] for i in self.non_recivedreqid]
                nondf = pd.DataFrame(data={'Missed Symbol': nonr})
                nonsavename = r'E:\newdata\IB data\Missed Symbols.csv'
                nondf.to_csv(nonsavename, index=False)

            savename = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
            self.superdf.reset_index(drop=True)
            self.superdf.to_csv(savename, index=False)
            print('Underlying Contract Details 文件已生成！')
            timer.cancel()
            self.disconnect()
        timer.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)
        reqidnums = list(self.reqConsdict.keys())
        if reqId in reqidnums and reqId not in self.non_recivedreqid:
            self.non_recivedreqid.append(reqId)

    def nextValidId(self, orderId: int):
        self.ReqContractsDetail(self.symbolslist)

    def ReqContractsDetail(self, symbols: list):
        reqn = 0
        for si in symbols:
            self.reqConsdict[reqn] = si
            reqCon = make_contract(symbol=si)
            print('请求合约详情：', si)
            self.reqContractDetails(reqn, reqCon)
            reqn += 1
        self.scan()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.__str__())
        con = contract_to_df(contractDetails.contract)
        if self.initdf:
            self.superdf = con
            self.initdf = False
        else:
            self.superdf = self.superdf.append(con)

    def contractDetailsEnd(self, reqId: int):
        if reqId not in self.recivedreqid:
            self.recivedreqid.append(reqId)


class myClient_get_opt_params(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.reqConsdict = {}
        self.recivedreqid = []
        self.non_recivedreqid = []

    def scan(self):
        # print('----------------------------')
        timer = Timer(0.2, self.scan)
        reqidnums = list(self.reqConsdict.keys())
        if len(reqidnums) == len(self.recivedreqid + self.non_recivedreqid) and len(reqidnums) > 0:
            if len(self.non_recivedreqid) > 0:
                nonr = [self.reqConsdict[i] for i in self.non_recivedreqid]
                nondf = pd.DataFrame(data={'Symbol': nonr})
                nonsavename = r'E:\newdata\IB data\Missed Symbols-Opt Params.csv'
                nondf.to_csv(nonsavename, index=False)
            self.disconnect()
        timer.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)
        reqidnums = list(self.reqConsdict.keys())
        if reqId in reqidnums and reqId not in self.non_recivedreqid:
            self.non_recivedreqid.append(reqId)

    def nextValidId(self, orderId: int):
        self.ReqOPTparams()

    def ReqOPTparams(self):
        file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
        sdf = pd.read_csv(file)
        dflen = len(sdf)
        for di in range(dflen):
            symbol = sdf['symbol'][di]
            secType = sdf['secType'][di]
            conID = sdf['conID'][di]
            self.reqSecDefOptParams(di, symbol, '', secType, conID)
            self.reqConsdict[di] = symbol
            print('请求期权参数：', symbol)

        self.scan()

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
                                          underlyingConId: int, tradingClass: str, multiplier: str,
                                          expirations: SetOfString, strikes: SetOfFloat):
        if exchange == 'SMART':
            if reqId not in self.recivedreqid:
                self.recivedreqid.append(reqId)
                jdict = {}
                jdict['expirations'] = list(sorted(list(expirations)))
                jdict['strikes'] = list(sorted(list(strikes)))
                savename = r'E:\newdata\IB data\Option Params' + os.sep + self.reqConsdict[reqId] + '.json'
                jf = open(savename, 'w')
                json.dump(jdict, jf)
                jf.close()
                print('写入json文件：', self.reqConsdict[reqId])

    def securityDefinitionOptionParameterEnd(self, reqId: int):
        pass


class myClient_get_Options_details(_myClient):
    missedsymbols = []

    def __init__(self, symbol: str, jdict: dict, last: float, aboveRdays=7, strikeSpan=0.1):
        _myClient.__init__(self)
        self.symbol = symbol
        self.last = last
        self.jdict = jdict
        self.recivedreqid = []
        self.non_recivedreqid = []
        self.aboveRdays = aboveRdays
        self.strikeSpan = strikeSpan
        self.eligibleOptreqIDs = []
        self.eligibleOpts = []
        self.recivedata = {}
        self.done = False
        self.timeout = 0
        self.fullcons = []
        self.efullcons = []

    def scan(self):
        print(self.symbol, '----------------------------', self.timeout)
        timer = Timer(0.2, self.scan)
        if len(self.recivedreqid + self.non_recivedreqid) == len(self.eligibleOptreqIDs) and len(self.eligibleOptreqIDs) > 0:
            jfpath = r'E:\newdata\IB data\Option Specs' + os.sep + self.symbol + '-specs.json'
            jf = open(jfpath, 'w')
            json.dump(self.recivedata, jf)
            jf.close()

            jnon = open(r'E:\newdata\IB data\Full Contracts.json', 'w')
            json.dump({'Full Contracts': self.efullcons + self.fullcons}, jnon)
            jnon.close()

            print('写入', self.symbol + '-specs.json')
            self.done = True
            timer.cancel()
            self.disconnect()
        self.timeout += 1

        if self.timeout >= 900:
            print('请求超时！', self.symbol)
            myClient_get_Options_details.missedsymbols.append(self.symbol)
            timer.cancel()
            self.disconnect()

        if not self.done:
            timer.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)
        if reqId in self.eligibleOptreqIDs and reqId not in self.non_recivedreqid:
            self.non_recivedreqid.append(reqId)

    def nextValidId(self, orderId: int):
        self.ReqContractsDetail()

    def ReqContractsDetail(self):
        reqn = 0
        sleepnum = 7000
        jnon = open(r'E:\newdata\IB data\Full Contracts.json', 'r')
        self.efullcons = json.load(jnon)['Full Contracts']
        jnon.close()

        for ei in self.jdict['expirations']:
            ed = IBdate_to_Date(ei)
            today = date.today()
            if (ed - today).days > self.aboveRdays:
                for si in self.jdict['strikes']:
                    if (1 - self.strikeSpan) * self.last < si < (1 + self.strikeSpan) * self.last:
                        u = [self.symbol, ei, si]

                        if u not in self.efullcons:
                            self.fullcons.append(u)
                            reqCon_C = make_contract(self.symbol, secType='OPT', right='C', lastTradeDateOrContractMonth=ei, strike=si)
                            self.reqContractDetails(reqn, reqCon_C)
                            self.eligibleOptreqIDs.append(reqn)
                            self.eligibleOpts.append((ei, si, 'C', reqn))
                            print('请求：', (ei, si, 'C', reqn))
                            time.sleep(0.021)
                            reqn += 1
                            sleepnum -= 1
                            reqCon_P = make_contract(self.symbol, secType='OPT', right='P', lastTradeDateOrContractMonth=ei, strike=si)
                            self.reqContractDetails(reqn, reqCon_P)
                            self.eligibleOptreqIDs.append(reqn)
                            self.eligibleOpts.append((ei, si, 'P', reqn))
                            print('请求：', (ei, si, 'P', reqn))
                            time.sleep(0.021)
                            reqn += 1
                            sleepnum -= 1
                            if sleepnum <= 0:
                                print('睡眠中！+++++++++++')
                                time.sleep(30)
                                sleepnum = 7000

        if len(self.eligibleOptreqIDs) == 0:
            print('所有期权已存在：', self.symbol)
            self.disconnect()
        else:
            jfpath = r'E:\newdata\IB data\Option Specs'
            jffiles = os.listdir(jfpath)
            file = self.symbol + '-specs.json'
            if file in jffiles:
                jh = open(jfpath + os.sep + file, 'r')
                self.recivedata = json.load(jh)

            self.scan()

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract.__str__())
        if reqId in self.eligibleOptreqIDs:
            idx = self.eligibleOptreqIDs.index(reqId)
            spc = self.eligibleOpts[idx]
            if spc[0] not in self.recivedata.keys():
                self.recivedata[spc[0]] = {}
                self.recivedata[spc[0]]['C'] = {}
                self.recivedata[spc[0]]['P'] = {}
            self.recivedata[spc[0]][spc[2]][spc[1]] = contract_to_dict(contractDetails.contract)
            self.recivedreqid.append(reqId)

    def contractDetailsEnd(self, reqId: int):
        pass


def get_Optins_Contract_Detail_bulk(aboveRdays=7, strikeSpan=0.15):
    jpath = r'E:\newdata\IB data\Option Params'
    jfilelist = os.listdir(jpath)

    specpath = r'E:\newdata\IB data\Option Specs'
    specslist = os.listdir(specpath)

    file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
    underlying = pd.read_csv(file)

    for ji in jfilelist:
        symbol = ji.split('.')[0]
        specfile = symbol + '-specs.json'
        # if specfile not in specslist:
        idx = list(underlying['symbol']).index(symbol)
        last = underlying['Last'][idx]
        jf = open(jpath + os.sep + ji)
        jdict = json.load(jf)
        jf.close()
        print('请求', symbol)
        app = myClient_get_Options_details(symbol, jdict, last, aboveRdays, strikeSpan)
        app.connect('127.0.0.1', 7497, 0)
        app.run()
        time.sleep(3)
    print('超时丢失的symbols:', myClient_get_Options_details.missedsymbols)


def pick_stricks_2(last: float, stricks: list, sknum=1):
    buffdict = {}
    for i in stricks:
        buffdict[i - last] = i
    gaps = list(sorted(list(buffdict.keys()), reverse=True))
    absgaps = [abs(gi) for gi in gaps]
    absgaps = list(sorted(list(set(absgaps))))
    rv = []
    n = 0
    for agi in absgaps:
        for gii in gaps:
            if abs(gii) == agi:
                rv.append(buffdict[gii])
                n += 1
                if n == sknum:
                    break
        if n == sknum:
            break
    return rv


def pick_stricks(last: float, stricks: list, sknum=1):
    stricks = list(sorted(stricks))
    # print(stricks)
    ps = []
    if last in stricks:
        sidx = stricks.index(last)
        m = sknum // 2
        y = sknum % 2
        if y != 0:
            ps = stricks[sidx - m: sidx + m + 1]
        else:
            ps = stricks[sidx - m + 1: sidx + m + 1]

    else:
        stricks_2 = stricks
        stricks_2.append(last)
        stricks_3 = list(sorted(stricks_2))
        sidx = stricks_3.index(last)
        ds = stricks_3[sidx - 1]
        us = stricks_3[sidx + 1]
        nearup = False
        if us - last <= last - ds:
            nearup = True
        m = sknum // 2
        y = sknum % 2
        if y == 0:
            ps = stricks_3[sidx - m: sidx + m + 1]
            print(last)
            print(sidx)
            print(stricks_3)
            ps.pop(m)
        else:
            if nearup:
                ps = stricks_3[sidx - m: sidx + m + 2]
                ps.pop(m)
            else:
                ps = stricks_3[sidx - m - 1: sidx + m + 1]
                ps.pop(m + 1)
    return ps


def combo_generator_Switch(symbol: str, abovedays=7, lessdays =120):
    specpath = r'E:\newdata\IB data\Option Specs'
    file = specpath + os.sep + symbol + '-specs.json'
    jf = open(file, 'r')
    jdict = json.load(jf)
    jf.close()

    underlyingfile = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
    underlying = pd.read_csv(underlyingfile)
    syms = list(underlying['symbol'])
    idx = syms.index(symbol)
    last = underlying['Last'][idx]


    underlyingleg = ComboLeg()
    underlyingleg.conId = underlying['conID'][idx]
    underlyingleg.ratio = 100
    underlyingleg.action = 'BUY'
    underlyingleg.exchange = 'SMART'

    Pleg = ComboLeg()
    Pleg.ratio = 1
    Pleg.action = 'BUY'
    Pleg.exchange = 'SMART'

    Cleg = ComboLeg()
    Cleg.ratio = 1
    Cleg.action = 'SELL'
    Cleg.exchange = 'SMART'

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'BAG'
    contract.currency = 'USD'
    contract.exchange = 'SMART'

    Combos = []

    for mi, di in jdict.items():
        jm = IBdate_to_Date(mi)
        today = date.today()
        if abovedays < (jm - today).days <= lessdays:
            stricks = list(di['C'].keys())
            stricks_1 = [float(i) for i in stricks]
            print(symbol)
            ps = pick_stricks_2(last, stricks_1, 2)
            for si in ps:
                Pleg.conId = di['P'][str(si)]['conID']
                Cleg.conId = di['C'][str(si)]['conID']
                contract.comboLegs = []

                contract.comboLegs.append(underlyingleg)
                contract.comboLegs.append(Pleg)
                contract.comboLegs.append(Cleg)
                Combos.append([deepcopy(contract), si])

    return Combos


def combo_generator_Box(symbol: str, lessdays =120):
    specpath = r'E:\newdata\IB data\Option Specs'
    file = specpath + os.sep + symbol + '-specs.json'
    jf = open(file, 'r')
    jdict = json.load(jf)
    jf.close()

    underlyingfile = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
    underlying = pd.read_csv(underlyingfile)
    syms = list(underlying['symbol'])
    idx = syms.index(symbol)
    last = underlying['Last'][idx]

    underlyingleg = ComboLeg()
    underlyingleg.conId = underlying['conID'][idx]
    underlyingleg.ratio = 100
    underlyingleg.action = 'BUY'
    underlyingleg.exchange = 'SMART'

    Pleg = ComboLeg()
    Pleg.ratio = 1
    Pleg.action = 'BUY'
    Pleg.exchange = 'SMART'

    Cleg = ComboLeg()
    Cleg.ratio = 1
    Cleg.action = 'SELL'
    Cleg.exchange = 'SMART'

    contract = Contract()
    contract.symbol = symbol
    contract.secType = 'BAG'
    contract.currency = 'USD'
    contract.exchange = 'SMART'

    Combos = []

    for mi, di in jdict.items():
        jm = IBdate_to_Date(mi)
        today = date.today()
        if (jm - today).days <= lessdays:
            stricks = list(di['C'].keys())
            stricks_1 = [float(i) for i in stricks]
            ps = pick_stricks_2(last, stricks_1, 2)
            for si in ps:
                Pleg.conId = di['P'][str(si)]['conID']
                Cleg.conId = di['C'][str(si)]['conID']
                contract.comboLegs = []

                contract.comboLegs.append(underlyingleg)
                contract.comboLegs.append(Pleg)
                contract.comboLegs.append(Cleg)
                Combos.append([deepcopy(contract), si])

    return Combos


class myClient_place_orders(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.orderId = ''
        self.start = False
        self.orderlist = []
        self.pid = 0

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        print('Order ID:', orderId)

        if not self.start:
            self.myOrders_generator()
            self.start = True

        if self.pid < len(self.orderlist) - 1:
            self.myPlaceOrder(orderId, self.orderlist[self.pid][0], self.orderlist[self.pid][1])
            print('PID:', self.pid, '+++++++++++++++++')
            self.pid += 1
            time.sleep(0.1)

    def myOrders_generator(self):
        file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
        underlying = pd.read_csv(file)
        symbols = list(underlying['symbol'])
        for syi in symbols:
            Combos = combo_generator_Switch(syi, 120)
            for coi in Combos:
                con = coi[0]
                sk = coi[1]
                limitPrice = sk * 0.9
                quantity = 1
                action = 'BUY'

                order = Order()
                order.action = action
                order.orderType = "LMT"
                order.totalQuantity = quantity
                order.lmtPrice = limitPrice
                self.orderlist.append([deepcopy(con), deepcopy(order)])

    def myPlaceOrder(self, orderId, contract, order):
        self.placeOrder(orderId, contract, order)
        self.reqIds(5)


class myClient_get_acccount_position_infos(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.Account = ''
        self.placedorders = []
        self.remainingcash = 0
        self.get_placedorders_done = False
        self.get_remainingcash_done = False

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        pass

    def reqAccount_Position_infos(self, sp: bool, acct: str):
        self.reqAccountUpdates(sp, acct)
        # self.reqPositions()
        self.reqAllOpenOrders()

    def managedAccounts(self, accountsList:str):
        print(accountsList)
        self.Account = accountsList.split(',')[0]
        self.reqAccount_Position_infos(True, self.Account)

    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):
        print('-----------------账户信息-----------------------')
        print('key:', key, ' Value:', val, ' Currency:', currency, ' Account Name:', accountName)
        if key == 'FullAvailableFunds' and currency == 'USD':
            self.remainingcash = val
            self.get_remainingcash_done = True

    def updatePortfolio(self, contract: Contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):
        print('-----------------Portfolio信息-----------------------')
        print('Contract:', contract.__str__())
        print('Position:', position, ' Market Price:', marketPrice, ' MarketValue:', marketPrice, ' Average Cost:',
              averageCost, ' unRealized PNL:', unrealizedPNL, ' Realized PNL:', realizedPNL, ' Account Name:',
              accountName)


    def updateAccountTime(self, timeStamp: str):
        print('-----------------时间戳-----------------------')
        print(timeStamp)

    def accountDownloadEnd(self, accountName: str):
        print('-----------------账户更新完毕-----------------------')
        print(accountName)

    def position(self, account:str, contract:Contract, position:float,
                 avgCost:float):
        print('-----------------Position信息-----------------------')
        print('Account:', account, ' Position:', position, ' avgCost:', avgCost)
        print('Contract:', contract.__str__())

    def positionEnd(self):
        print('-----------------Position信息完毕-----------------------')

    def accountSummary(self, reqId:int, account:str, tag:str, value:str,
                       currency:str):
        pass

    def accountSummaryEnd(self, reqId:int):
        pass

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order,
                  orderState: OrderState):
        print(orderId)
        self.placedorders.append(
         deepcopy([contract.comboLegs[0].conId, contract.comboLegs[0].action, contract.comboLegs[0].ratio,
         contract.comboLegs[1].conId, contract.comboLegs[1].action, contract.comboLegs[1].ratio,
         contract.comboLegs[2].conId, contract.comboLegs[2].action, contract.comboLegs[2].ratio,
         order.action, order.totalQuantity, order.lmtPrice]))

    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def openOrderEnd(self):
        print('OpenOrder 完毕！')
        self.get_placedorders_done = True

    def orderBound(self, reqId: int, apiClientId: int, apiOrderId: int):
        print('OrderBound 被激活++++++++++++++++++++++++')


class myTimer():
    def __init__(self, func, timegap=1):
        self.func = func
        self.timegap = timegap

    def start(self):
        timer = Timer(self.timegap, self.func)
        timer.start()


def print_Order_State(o_s: OrderState):
    print('订单状态：', o_s.status, '手续费：', o_s.commission, '警告：', o_s.warningText, '统计：', o_s.completedStatus)
    print('初始保证金前：', o_s.initMarginBefore, '初始保证金后：', o_s.initMarginAfter, '初始保证金变化：', o_s.initMarginChange)
    print('维持保证金前：', o_s.maintMarginBefore, '维持保证金后：', o_s.maintMarginAfter, '维持保证金变化：', o_s.maintMarginChange)
    print('含贷款证券价值前：', o_s.equityWithLoanBefore, '含贷款证券价值后：', o_s.equityWithLoanAfter, '含贷款证券价值变化：', o_s.equityWithLoanChange)


def order_contract_idfy_genarator(order: Order, contract: Contract):
    idfy = {}
    idfy['orderaction'] = order.action
    # idfy['orderQuantity'] = order.totalQuantity
    idfy['orderlmtPrice'] = order.lmtPrice
    idfy['parentId'] = order.parentId
    idfy['comboLegs'] = {}
    if len(contract.comboLegs) > 0:
        for ci in contract.comboLegs:
            idfy['comboLegs'][ci.conId] = {}
            idfy['comboLegs'][ci.conId]['action'] = ci.action
            idfy['comboLegs'][ci.conId]['ratio'] = ci.ratio
    return idfy


class myClient_Place_Order_beta(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.Account = ''
        self.placedorders = []
        self.placedorderIDs = []
        self.placedorderTotalQty = []
        self.remainingcash = 0
        self.get_placedorders_done = False
        self.get_remainingcash_done = False
        self.filledordersdict = {}

        self.orderId = 0
        self.start = False
        self.orderlist = []


    def scan(self):
        print('-----')
        timer = Timer(0.2, self.scan)
        if self.get_placedorders_done and self.get_remainingcash_done:
            timer.cancel()
            self.start = True
            self.reqAccountUpdates(False, self.Account)
            self.myOrders_generator()
            self.myPlaceOrder()

        if not self.start:
            timer.start()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def reqAccount_Position_infos(self, sp: bool, acct: str):
        self.reqAccountUpdates(sp, acct)
        self.reqOpenOrders()

    def managedAccounts(self, accountsList:str):
        print(accountsList)
        self.Account = accountsList.split(',')[0]
        self.reqAccount_Position_infos(True, self.Account)

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        if key == 'FullAvailableFunds' and currency == 'USD':
            self.remainingcash = float(val)
            self.get_remainingcash_done = True
            print('可用资金已获取：', val)
            self.scan()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print('OpenOrders信息：')
        print(orderId)
        print(order.__str__())
        print(contract.__str__())
        # print_Order_State(orderState)

        self.placedorders.append(order_contract_idfy_genarator(order, contract))
        self.placedorderIDs.append(orderId)
        self.placedorderTotalQty.append(order.totalQuantity)

    def openOrderEnd(self):
        if not self.start:
            print('OpenOrder 完毕！')
            self.get_placedorders_done = True

    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        if status == 'Filled':
            self.filledordersdict[orderId] = [remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId,
                                              whyHeld, mktCapPrice]

        print('订单状态：')
        print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def nextValidId(self, orderId: int):
        print('The next Valid Order ID:', orderId)
        self.orderId = orderId

    def myOrders_generator(self):
        file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
        underlying = pd.read_csv(file)
        symbols = list(underlying['symbol'])
        for syi in symbols:
            Combos = combo_generator_Switch(syi, 7, 120)
            for coi in Combos:
                con = coi[0]
                sk = coi[1]
                quantity = int(((self.remainingcash / 30) * 2) / (sk * 100))
                if quantity > 0:
                    limitPrice = round(sk * 0.95, 2)
                    action = 'BUY'

                    order = Order()
                    order.transmit = False
                    order.action = action
                    order.orderType = "LMT"
                    order.totalQuantity = quantity
                    order.lmtPrice = limitPrice
                    self.orderlist.append([deepcopy(con), deepcopy(order)])

    def myPlaceOrder(self):
        n = 0
        for oi in self.orderlist:
            n += 1
            contract = oi[0]
            order = oi[1]
            conidfy = order_contract_idfy_genarator(order, contract)
            if conidfy not in self.placedorders:
                nagorder = deepcopy(order)
                if order.action == 'BUY':
                    nagorder.action = 'SELL'
                elif order.action == 'SELL':
                    nagorder.action = 'BUY'
                nagorder.lmtPrice = round(order.lmtPrice / 0.95, 2)
                nagorder.transmit = True
                nagorder.parentId = self.orderId

                self.placeOrder(self.orderId, contract, order)
                self.placeOrder(self.orderId + 1, contract, nagorder)
                self.reqIds(-1)
                print(n, '提交原始订单！')
                time.sleep(0.1)
            else:
                idx = self.placedorders.index(conidfy)
                if order.totalQuantity != self.placedorderTotalQty[idx]:
                    self.cancelOrder(self.placedorderIDs[idx])
                    self.placedorders.pop(idx)
                    self.placedorderIDs.pop(idx)
                    self.placedorderTotalQty.pop(idx)
                    time.sleep(0.05)

                    nagorder = deepcopy(order)
                    if order.action == 'BUY':
                        nagorder.action = 'SELL'
                    elif order.action == 'SELL':
                        nagorder.action = 'BUY'
                    nagorder.lmtPrice = round(order.lmtPrice / 0.95, 2)
                    nagorder.transmit = True
                    nagorder.parentId = self.orderId

                    self.placeOrder(self.orderId, contract, order)
                    self.placeOrder(self.orderId + 1, contract, nagorder)
                    self.reqIds(-1)
                    print(n, '提交修改订单！')
                    time.sleep(0.1)
                else:
                    print('该订单已存在！')

        print('订单发送完毕！&&&&&&&&&&&&&')


class myClient_Place_Order_beta_Box(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.Account = ''
        self.placedorders = {}
        self.remainingcash = 0
        self.get_placedorders_done = False
        self.get_remainingcash_done = False
        self.get_stop = False

        self.orderId = ''
        self.start = False
        self.orderlist = []
        self.pid = 0

    def scan(self):
        timer = Timer(0.2, self.scan)
        if self.get_placedorders_done and self.get_remainingcash_done:
            if not self.get_stop:
                self.reqAccountUpdates(False, self.Account)
                self.get_stop = True

            if not self.start:
                self.myOrders_generator()
                self.start = True
                self.reqIds(5)
        if self.start:
            timer.cancel()
        timer.start()

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def reqAccount_Position_infos(self, sp: bool, acct: str):
        self.reqAccountUpdates(sp, acct)
        self.reqOpenOrders()

    def managedAccounts(self, accountsList:str):
        print(accountsList)
        self.Account = accountsList.split(',')[0]
        self.reqAccount_Position_infos(True, self.Account)

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        if key == 'FullAvailableFunds' and currency == 'USD':
            self.remainingcash = float(val)
            self.get_remainingcash_done = True
            print('可用资金已获取：', val)
            self.scan()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(orderId)
        print_Order_State(orderState)

        key = str(contract.comboLegs[0].conId) + contract.comboLegs[0].action + str(contract.comboLegs[0].ratio) + \
                  str(contract.comboLegs[1].conId) + contract.comboLegs[1].action + str(contract.comboLegs[1].ratio) + \
                  str(contract.comboLegs[2].conId) + contract.comboLegs[2].action + str(contract.comboLegs[2].ratio) + \
                  order.action + str(order.lmtPrice)
        self.placedorders[key] = {}
        self.placedorders[key]['Quantity'] = order.totalQuantity
        # self.placedorders[key]['Action'] = order.action
        self.placedorders[key]['OrderID'] = orderId

    def openOrderEnd(self):
        print('OpenOrder 完毕！')
        self.get_placedorders_done = True

    def nextValidId(self, orderId: int):
        print('Order ID:', orderId)
        self.orderId = orderId

        if self.start:
            if self.pid < len(self.orderlist) - 1:
                contract = self.orderlist[self.pid][0]
                order = self.orderlist[self.pid][1]
                conidfy = str(contract.comboLegs[0].conId) + contract.comboLegs[0].action + str(contract.comboLegs[0].ratio) + \
                  str(contract.comboLegs[2].conId) + contract.comboLegs[2].action + str(contract.comboLegs[1].ratio) + \
                  str(contract.comboLegs[1].conId) + contract.comboLegs[1].action + str(contract.comboLegs[2].ratio) + \
                  order.action + str(order.lmtPrice)

                if conidfy not in self.placedorders.keys():
                    self.myPlaceOrder(orderId, contract, order)
                    print('PID:', self.pid, '提交原始订单！')
                else:
                    if order.totalQuantity != self.placedorders[conidfy]['Quantity']:
                        self.cancelOrder(self.placedorders[conidfy]['OrderID'])
                        self.myPlaceOrder(orderId, contract, order)
                        print('PID:', self.pid, '提交修改订单！')
                    else:
                        self.reqIds(5)
                        time.sleep(0.1)
                        print('该合约已存在！')
                self.pid += 1
            if self.pid == len(self.orderlist) - 1:
                print('订单发送完毕！&&&&&&&&&&&&&')

    def myOrders_generator(self):
        file = r'E:\newdata\IB data\Underlying_Contract_Details.csv'
        underlying = pd.read_csv(file)
        symbols = list(underlying['symbol'])
        for syi in symbols:
            Combos = combo_generator_Switch(syi, 120)
            for coi in Combos:
                con = coi[0]
                sk = coi[1]
                quantity = int(((self.remainingcash / 30) * 2) / (sk * 100))
                if quantity > 0:
                    limitPrice = round(sk * 0.95, 2)
                    action = 'BUY'

                    order = Order()
                    order.whatIf = False
                    order.action = action
                    order.orderType = "LMT"
                    order.totalQuantity = quantity
                    order.lmtPrice = limitPrice
                    self.orderlist.append([deepcopy(con), deepcopy(order)])

    def myPlaceOrder(self, orderId, contract, order):
        self.placeOrder(orderId, contract, order)
        time.sleep(0.1)
        self.reqIds(5)


class myClient_get_scaner_params(_myClient):
    def __init__(self):
        _myClient.__init__(self)

    def nextValidId(self, orderId: int):
        self.reqScannerParameters()

    def scannerParameters(self, xml: str):
        print(xml)
        f = open(r'E:\newdata\IB data\Scaner Parameters.xml', 'w', encoding='utf-8')
        f.write(xml)
        f.close()


class myClient_myScaner(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.snum = 1

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        scanSub = ScannerSubscription()
        scanSub.instrument = 'STK'
        scanSub.locationCode = 'STK.US'
        scanSub.scanCode = 'HIGH_OPT_IMP_VOLAT'
        scanSub.abovePrice = 100
        scanSub.numberOfRows = 1000
        scanSub.scannerSettingPairs = 'Annual, true'
        self.reqScannerSubscription(1, scanSub, [], [])

    def scannerData(self, reqId:int, rank:int, contractDetails:ContractDetails,
                     distance:str, benchmark:str, projection:str, legsStr:str):
        print('第{}个标的：'.format(self.snum))
        print('reqId:', reqId, ' rank:', rank, ' distance:', distance, ' benchmark:', benchmark, ' projection:', projection, ' legsStr:', legsStr)
        print('contractDetails:', contractDetails.__str__())
        self.snum += 1

    def scannerDataEnd(self, reqId:int):
        print('ScanData 结束！')


if __name__ == '__main__':

    # app = myClient_get_opt_params()
    # app.connect('127.0.0.1', 7497, 0)
    # app.run()

    # update_price()

    # get_Optins_Contract_Detail_bulk()

    # app = myClient_Place_Order_beta()
    # app.connect('127.0.0.1', 7497, 1)
    # app.run()

    app = myClient_myScaner()
    app.connect('127.0.0.1', 7497, 1)
    app.run()