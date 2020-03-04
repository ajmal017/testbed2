from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
from ibapi.ticktype import *
import pandas as pd
import os, threading, time, copy


def dataframeinsertrow(df:pd.DataFrame, n, row:list):
    columns = list(df.columns)
    insertrow = pd.DataFrame([row], columns=columns)
    if n <= 0:
        return insertrow.append(df, ignore_index=True)
    elif n >= df.__len__():
        return df.append(insertrow, ignore_index=True)
    else:
        above = df[:n]
        below = df[n:]
        newdf = pd.concat([above, insertrow, below], ignore_index=True)
        return newdf


def make_contract(symbol='', conID=0, secType='STK', currency='USD', exchange='', primaryExchange='',
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
    if tradingClass == '':
        contract.tradingClass = symbol
    contract.localSymbol = localSymbol
    contract.right = right
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    contract.strike = strike
    return contract


class optionsdatefram():
    def __init__(self, symbol, month):
        self.symbol = symbol
        self.month = month
        self.quote = pd.DataFrame(columns=['bid C', 'ask C', 'last C', 'bidSize C', 'askSize C', 'lastSize C',
                                                  'updateTime C', 'open C', 'high C', 'low C', 'close C', 'vol C', 'IV C',
                                                  'delta C', 'theta C', 'vega C', 'gamma C', 'strike', 'bid P', 'ask P', 'last P',
                                                  'bidSize P', 'askSize P', 'lastSize P','updateTime P', 'open P', 'high P', 'low P',
                                                  'close P', 'vol P', 'IV P', 'delta P', 'theta P', 'vega P', 'gamma P'])

optionnullrow = [None] * 35

class iclient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)


class myClient3(EWrapper, iclient):
    def __init__(self, underlyingContract, Instricklist, filepath):
        EWrapper.__init__(self)
        iclient.__init__(self, wrapper=self)
        self.filepath = filepath
        self.quotedatadict = {}
        self.reqID_contract_dict = {}
        self.underlyingContract = underlyingContract
        self.refresher = threading.Timer(10, self.refreshfun)
        self.expirations = ''
        self.Instricklist = Instricklist


    def refreshfun(self):
        for k, v in self.quotedatadict.items():
            stickerpath = self.filepath + os.sep + k
            if not os.path.exists(stickerpath):
                os.makedirs(stickerpath)
            for mk, mv in v.items():
                fulloptcsvpath = self.filepath + os.sep + k + os.sep + mk + '.csv'
                if not os.path.exists(fulloptcsvpath):
                    mv.quote.to_csv(fulloptcsvpath, index=False)
                else:
                     try:
                         mv.quote.to_csv(fulloptcsvpath, index=False)
                     except Exception as oe:
                         repr(oe)
                         continue
        self.refresher = threading.Timer(2, self.refreshfun)
        self.refresher.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId:int):
        self.reqSecDefOptParams(0, self.underlyingContract.symbol, '',
                                self.underlyingContract.secType, self.underlyingContract.conId)

    def securityDefinitionOptionParameter(self, reqId: int, exchange: str,
                                          underlyingConId: int, tradingClass: str, multiplier: str,
                                          expirations: SetOfString, strikes: SetOfFloat):
        print('reqID:', reqId, ' exchange:', exchange, ' underlyingConID:', underlyingConId, ' tradindClass:',
              tradingClass, ' multiplier:', multiplier, ' expirations:', expirations, ' strikes:', strikes)
        if exchange == 'SMART':
            self.expirations = expirations

    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print('options done: ', reqId)
        n = 0
        for i in self.Instricklist:
            conP = make_contract(self.underlyingContract.symbol, secType='OPT', exchange='SMART', right='P', strike=i)
            conC = make_contract(self.underlyingContract.symbol, secType='OPT', exchange='SMART', right='C', strike=i)
            for m in self.expirations:
                conC.lastTradeDateOrContractMonth = m
                conP.lastTradeDateOrContractMonth = m
                n += 1
                self.reqID_contract_dict[n] = copy.deepcopy(conC)
                n += 1
                self.reqID_contract_dict[n] = copy.deepcopy(conP)
        self.reqMarketDataType(3)

        for k, v in self.reqID_contract_dict.items():
            self.reqMktData(k, v, '106', False, False, [])
            time.sleep(0.025)
            if v.symbol not in self.quotedatadict.keys():
                self.quotedatadict[v.symbol] = {}
                self.quotedatadict[v.symbol][v.lastTradeDateOrContractMonth] = optionsdatefram(v.symbol, v.lastTradeDateOrContractMonth)
            else:
                if v.lastTradeDateOrContractMonth not in self.quotedatadict[v.symbol].keys():
                    self.quotedatadict[v.symbol][v.lastTradeDateOrContractMonth] = optionsdatefram(v.symbol, v.lastTradeDateOrContractMonth)
        self.refresher.start()


    def marketDataType(self, reqId:TickerId, marketDataType:int):
        print('reqID:', reqId, ' marketDataType:', marketDataType)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        print('reqID:', reqId, ' tickType:', tickType, ' price:', price)

        symbol = self.reqID_contract_dict[reqId].symbol
        month = self.reqID_contract_dict[reqId].lastTradeDateOrContractMonth
        strike = self.reqID_contract_dict[reqId].strike
        right = self.reqID_contract_dict[reqId].right
        if self.quotedatadict[symbol][month].quote.empty:
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, 0, optionnullrow)
            self.quotedatadict[symbol][month].quote.at[0, 'strike'] = strike
        strickelist = list(self.quotedatadict[symbol][month].quote['strike'])
        srown = None
        if strike not in strickelist:
            strickelist.append(strike)
            strickelist = sorted(strickelist)
            #global srown
            srown = strickelist.index(strike)
            #srown = srownx
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, srown,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[srown, 'strike'] = strike
        else:
            srown = strickelist.index(strike)
        if tickType == 66:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'bid P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'bid C'] = price
        elif tickType == 67:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'ask P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'ask C'] = price
        elif tickType == 68:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'last P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'last C'] = price
        elif tickType == 72:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'high P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'high C'] = price
        elif tickType == 73:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'low P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'low C'] = price
        elif tickType == 75:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'close P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'close C'] = price
        elif tickType == 76:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'open P'] = price
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'open C'] = price

    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        print('reqID:', reqId, ' tickType:', tickType, ' size:', size)

        symbol = self.reqID_contract_dict[reqId].symbol
        month = self.reqID_contract_dict[reqId].lastTradeDateOrContractMonth
        strike = self.reqID_contract_dict[reqId].strike
        right = self.reqID_contract_dict[reqId].right
        if self.quotedatadict[symbol][month].quote.empty:
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, 0,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[0, 'strike'] = strike
        strickelist = list(self.quotedatadict[symbol][month].quote['strike'])
        srown = None
        if strike not in strickelist:
            strickelist.append(strike)
            strickelist = sorted(strickelist)
            #global srown
            srown = strickelist.index(strike)
            #srown = srown
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, srown,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[srown, 'strike'] = strike
        else:
            srown = strickelist.index(strike)
        if tickType == 69:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'bidSize P'] = size
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'bidSize C'] = size
        elif tickType == 70:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'askSize P'] = size
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'askSize C'] = size
        elif tickType == 71:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'lastSize P'] = size
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'lastSize C'] = size
        elif tickType == 74:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'vol P'] = size
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'vol C'] = size

    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):
        print('reqID:', reqId, ' tickType:', tickType, ' value:', value)

    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        print('reqID:', reqId, ' tickType:', tickType, ' value:', value)

        symbol = self.reqID_contract_dict[reqId].symbol
        month = self.reqID_contract_dict[reqId].lastTradeDateOrContractMonth
        strike = self.reqID_contract_dict[reqId].strike
        right = self.reqID_contract_dict[reqId].right
        if self.quotedatadict[symbol][month].quote.empty:
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, 0,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[0, 'strike'] = strike
        strickelist = list(self.quotedatadict[symbol][month].quote['strike'])
        srown = None
        if strike not in strickelist:
            strickelist.append(strike)
            strickelist = sorted(strickelist)
            #global srown
            srown = strickelist.index(strike)
            #srown = srownx
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, srown,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[srown, 'strike'] = strike
        else:
            srown = strickelist.index(strike)
        if tickType == 88:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'updateTime P'] = value
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'updateTime C'] = value



    def tickOptionComputation(self, reqId: TickerId, tickType: TickType,
                              impliedVol: float, delta: float, optPrice: float, pvDividend: float,
                              gamma: float, vega: float, theta: float, undPrice: float):
        print('reqID:', reqId, ' tickType:', tickType,  ' OptPrice:', optPrice, ' undPrice:', undPrice, ' IV:',
              impliedVol, ' delta:', delta, ' gamma:', gamma, ' vega:', vega, ' theta:', theta)

        symbol = self.reqID_contract_dict[reqId].symbol
        month = self.reqID_contract_dict[reqId].lastTradeDateOrContractMonth
        strike = self.reqID_contract_dict[reqId].strike
        right = self.reqID_contract_dict[reqId].right
        if self.quotedatadict[symbol][month].quote.empty:
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, 0,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[0, 'strike'] = strike
        strickelist = list(self.quotedatadict[symbol][month].quote['strike'])
        srown = None
        if strike not in strickelist:
            strickelist.append(strike)
            strickelist = sorted(strickelist)
            #global srown
            srown = strickelist.index(strike)
            #srown = srownx
            self.quotedatadict[symbol][month].quote = dataframeinsertrow(self.quotedatadict[symbol][month].quote, srown,
                                                                         optionnullrow)
            self.quotedatadict[symbol][month].quote.at[srown, 'strike'] = strike
        else:
            srown = strickelist.index(strike)
        if tickType == 83:
            if right == 'P':
                self.quotedatadict[symbol][month].quote.at[srown, 'IV P'] = impliedVol
                self.quotedatadict[symbol][month].quote.at[srown, 'delta P'] = delta
                self.quotedatadict[symbol][month].quote.at[srown, 'theta P'] = theta
                self.quotedatadict[symbol][month].quote.at[srown, 'gamma P'] = gamma
                self.quotedatadict[symbol][month].quote.at[srown, 'vega P'] = vega
            elif right == 'C':
                self.quotedatadict[symbol][month].quote.at[srown, 'IV C'] = impliedVol
                self.quotedatadict[symbol][month].quote.at[srown, 'delta C'] = delta
                self.quotedatadict[symbol][month].quote.at[srown, 'theta C'] = theta
                self.quotedatadict[symbol][month].quote.at[srown, 'gamma C'] = gamma
                self.quotedatadict[symbol][month].quote.at[srown, 'vega C'] = vega



# if __name__ == '__main__':
#     # conlist = []
#     # monthlist = ['20200221', '20200320', '20200417', '20200515', '20200619', '20200717', '20200821', '20200918', '20210115',
#     #              '20210618', '20220121', '20220617']
#     filepath = r'E:\ibdata3'
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)
#     underlying = make_contract('VXX', 303019419, exchange='SMART')
#     Instricklist = list(range(7, 28, 1))
#     myapp = myClient3(underlying, Instricklist, filepath)
#     myapp.connect('127.0.0.1', 4002, 0)
#     myapp.run()

