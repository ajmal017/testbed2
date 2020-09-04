from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.order import Order
from ibapi.common import *
from ibapi.ticktype import *
from iexfinance.stocks import Stock
import pandas as pd
from threading import Timer
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import time
import json
import os


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


def get_Optins_Contract_Detail_bulk(aboveRdays=6, strikeSpan=0.15):
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


def pick_stricks(last: float, stricks: list, sknum=1):
    stricks = list(sorted(stricks))
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
            ps.pop(m)
        else:
            if nearup:
                ps = stricks_3[sidx - m: sidx + m + 2]
                ps.pop(m)
            else:
                ps = stricks_3[sidx - m - 1: sidx + m + 1]
                ps.pop(m + 1)
    return ps


def combo_generator_Switch(symbol: str, lessdays =120):
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
            ps = pick_stricks(last, stricks_1, 2)
            for si in ps:
                Pleg.conId = di['P'][str(si)]['conID']
                Cleg.conId = di['C'][str(si)]['conID']
                contract.comboLegs = []

                contract.comboLegs.append(underlyingleg)
                contract.comboLegs.append(Pleg)
                contract.comboLegs.append(Cleg)
                Combos.append([contract, si])

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
            time.sleep(0.02)

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
                self.orderlist.append([con, order])

    def myPlaceOrder(self, orderId, contract, order):
        self.placeOrder(orderId, contract, order)
        self.reqIds(5)



if __name__ == '__main__':
    # symbolsfile = r'E:\newdata\IB data\202006-Mergers-Adj-U50.csv'
    # sdf = pd.read_csv(symbolsfile)
    # symbols = list(sdf['Underlying Security'])
    # sylist = [i.strip() for i in symbols]
    # app = myClient_get_underlying_details(sylist)
    # app.connect('127.0.0.1', 7497, 0)
    # app.run()

    # app = myClient_get_opt_params()
    # app.connect('127.0.0.1', 7497, 0)
    # app.run()

    # update_price()

    # app = myClient_get_Options_details(aboveRdays=7, strikeSpan=0.1)
    # app.connect('127.0.0.1', 7497, 0)
    # app.run()

    # get_Optins_Contract_Detail_bulk()

    # full_contracts_generator()

    app = myClient_place_orders()
    app.connect('127.0.0.1', 7497, 0)
    app.run()