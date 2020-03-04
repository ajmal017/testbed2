from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.common import *
from ibapi.ticktype import *
import pandas as pd
import os, threading, time


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
    contract.localSymbol = localSymbol
    contract.right = right
    contract.lastTradeDateOrContractMonth = lastTradeDateOrContractMonth
    contract.strike = strike
    return contract


class underlyingdatafram():
    def __init__(self, symbol):
        row = [symbol, None, None, None, None, None, None, None, None, None, None, None, None, None]
        self.quote = pd.DataFrame([row], columns=['symbol', 'bid', 'ask', 'last', 'bidSize', 'askSize', 'lastSize',
                     'updateTime', 'open', 'high', 'low', 'close', 'vol', 'IV'])


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


class myClient(EWrapper, iclient):
    def __init__(self, contractlist:list, filepath):
        EWrapper.__init__(self)
        iclient.__init__(self, wrapper=self)
        self.contractlist = contractlist
        self.reqID = 0
        self.csvpath = filepath
        self.optreqIDdict = {}
        self.underlyingIDdict = {}
        self.reqOptParamsIDdict = {}
        self.optionsquotesdict = {}
        self.refresher = threading.Timer(10, self.refreshfun)


    def refreshfun(self):
        #print('刷新！')
        for v in self.underlyingIDdict.values():
            csvname = v.quote['symbol'][0]
            fullcsvpath = self.csvpath + os.sep + csvname +os.sep + csvname + '.csv'
            # fullcsvdir = self.csvpath + os.sep + csvname
            if not os.path.exists(fullcsvpath):
                v.quote.to_csv(fullcsvpath, index=False)
            else:
                 try:
                     v.quote.to_csv(fullcsvpath, index=False)
                 except Exception as e:
                     repr(e)
                     continue
        for k, v in self.optionsquotesdict.items():
            for mk, mv in v.items():
                optcsvname = k + '-' + mk
                fulloptcsvpath = self.csvpath + os.sep + k + os.sep + 'options' + os.sep + optcsvname + '.csv'
                if not os.path.exists(fulloptcsvpath):
                    mv.quote.to_csv(fulloptcsvpath, index=False)
                else:
                     try:
                         mv.quote.to_csv(fulloptcsvpath, index=False)
                     except Exception as oe:
                         repr(oe)
                         continue
        #self.optionsquotesdict
        self.refresher = threading.Timer(2, self.refreshfun)
        self.refresher.start()

    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId:int):
       self.reqMarketDataType(3)
       for c in self.contractlist:
           self.reqID += 1
           self.reqMktData(self.reqID, c, '106', False, False, [])
           underlydir = self.csvpath + os.sep + c.symbol
           if not os.path.exists(underlydir):
               os.makedirs(underlydir)
           ud = underlyingdatafram(c.symbol)
           self.underlyingIDdict[self.reqID] = ud
           self.reqID += 1
           self.reqSecDefOptParams(self.reqID, c.symbol, '', c.secType, c.conId)
           optionsdir = self.csvpath + os.sep + c.symbol + os.sep + 'options'
           if not os.path.exists(optionsdir):
               os.makedirs(optionsdir)
           self.reqOptParamsIDdict[self.reqID] = [c.symbol]
       self.refresher.start()


    def marketDataType(self, reqId:TickerId, marketDataType:int):
        print('reqID:', reqId, ' marketDataType:', marketDataType)

    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float,
                  attrib: TickAttrib):
        print('reqID:', reqId, ' tickType:', tickType, ' price:', price)
        if reqId in self.underlyingIDdict.keys():
            if tickType == 66:
                self.underlyingIDdict[reqId].quote.at[0, 'bid'] = price
            elif tickType == 67:
                self.underlyingIDdict[reqId].quote.at[0, 'ask'] = price
            elif tickType == 68:
                self.underlyingIDdict[reqId].quote.at[0, 'last'] = price
            elif tickType == 72:
                self.underlyingIDdict[reqId].quote.at[0, 'high'] = price
            elif tickType == 73:
                self.underlyingIDdict[reqId].quote.at[0, 'low'] = price
            elif tickType == 75:
                self.underlyingIDdict[reqId].quote.at[0, 'close'] = price
            elif tickType == 76:
                self.underlyingIDdict[reqId].quote.at[0, 'open'] = price


        elif reqId in self.optreqIDdict.keys():
            symbol = self.optreqIDdict[reqId][0]
            ex = self.optreqIDdict[reqId][1]
            stk = self.optreqIDdict[reqId][2]
            rig = self.optreqIDdict[reqId][3]
            rownum = None
            if self.optionsquotesdict[symbol][ex].quote.empty:
                self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(self.optionsquotesdict[symbol][ex].quote, 0, optionnullrow)
                self.optionsquotesdict[symbol][ex].quote.at[0, 'strike'] = stk
                rownum = 0
            else:
                strikeS = list(self.optionsquotesdict[symbol][ex].quote['strike'])
                if stk in strikeS:
                    rownum = strikeS.index(stk)
                else:
                    strikeS.append(stk)
                    strikeS = sorted(strikeS)
                    rownum = strikeS.index(stk)
                    self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(self.optionsquotesdict[symbol][ex].quote, rownum, optionnullrow)
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'strike'] = stk
            if tickType == 66:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'bid C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'bid P'] = price
            elif tickType == 67:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'ask C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'ask P'] = price
            elif tickType == 68:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'last C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'last P'] = price
            elif tickType == 72:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'high C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'high P'] = price
            if tickType == 73:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'low C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'low P'] = price
            if tickType == 75:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'close C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'close P'] = price
            if tickType == 76:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'open C'] = price
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'open P'] = price


    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        print('reqID:', reqId, ' tickType:', tickType, ' size:', size)

        if reqId in self.underlyingIDdict.keys():
            if tickType == 69:
                self.underlyingIDdict[reqId].quote.at[0, 'bidSize'] = size
            elif tickType == 70:
                self.underlyingIDdict[reqId].quote.at[0, 'askSize'] = size
            elif tickType == 71:
                self.underlyingIDdict[reqId].quote.at[0, 'lastSize'] = size
            elif tickType == 74:
                self.underlyingIDdict[reqId].quote.at[0, 'vol'] = size

        elif reqId in self.optreqIDdict.keys():
            symbol = self.optreqIDdict[reqId][0]
            ex = self.optreqIDdict[reqId][1]
            stk = self.optreqIDdict[reqId][2]
            rig = self.optreqIDdict[reqId][3]
            rownum = None
            if self.optionsquotesdict[symbol][ex].quote.empty:
                self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(self.optionsquotesdict[symbol][ex].quote,
                                                                              0, optionnullrow)
                self.optionsquotesdict[symbol][ex].quote.at[0, 'strike'] = stk
                rownum = 0
            else:
                strikeS = list(self.optionsquotesdict[symbol][ex].quote['strike'])
                if stk in strikeS:
                    rownum = strikeS.index(stk)
                else:
                    strikeS.append(stk)
                    strikeS = sorted(strikeS)
                    rownum = strikeS.index(stk)
                    self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(
                        self.optionsquotesdict[symbol][ex].quote, rownum, optionnullrow)
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'strike'] = stk
            if tickType == 69:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'bidSize C'] = size
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'bidSize P'] = size
            elif tickType == 70:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'askSize C'] = size
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'askSize P'] = size
            elif tickType == 71:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'lastSize C'] = size
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'lastSize P'] = size
            elif tickType == 74:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'vol C'] = size
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'vol P'] = size



    def tickGeneric(self, reqId:TickerId, tickType:TickType, value:float):
        print('reqID:', reqId, ' tickType:', tickType, ' value:', value)

        if reqId in self.underlyingIDdict.keys():
            if tickType == 24:
                self.underlyingIDdict[reqId].quote.at[0, 'IV'] = value

    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        print('reqID:', reqId, ' tickType:', tickType, ' value:', value)

        if reqId in self.underlyingIDdict.keys():
            if tickType == 88:
                self.underlyingIDdict[reqId].quote.at[0, 'updateTime'] = value

        elif reqId in self.optreqIDdict.keys():
            symbol = self.optreqIDdict[reqId][0]
            ex = self.optreqIDdict[reqId][1]
            stk = self.optreqIDdict[reqId][2]
            rig = self.optreqIDdict[reqId][3]
            rownum = None
            if self.optionsquotesdict[symbol][ex].quote.empty:
                self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(self.optionsquotesdict[symbol][ex].quote,
                                                                              0, optionnullrow)
                self.optionsquotesdict[symbol][ex].quote.at[0, 'strike'] = stk
                rownum = 0
            else:
                strikeS = list(self.optionsquotesdict[symbol][ex].quote['strike'])
                if stk in strikeS:
                    rownum = strikeS.index(stk)
                else:
                    strikeS.append(stk)
                    strikeS = sorted(strikeS)
                    rownum = strikeS.index(stk)
                    self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(
                        self.optionsquotesdict[symbol][ex].quote, rownum, optionnullrow)
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'strike'] = stk
            if tickType == 88:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'updateTime C'] = value
                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'updateTime P'] = value

    def tickOptionComputation(self, reqId: TickerId, tickType: TickType,
                              impliedVol: float, delta: float, optPrice: float, pvDividend: float,
                              gamma: float, vega: float, theta: float, undPrice: float):
        print('reqID:', reqId, ' tickType:', tickType,  ' OptPrice:', optPrice, ' undPrice:', undPrice, ' IV:',
              impliedVol, ' delta:', delta, ' gamma:', gamma, ' vega:', vega, ' theta:', theta)

        if reqId in self.optreqIDdict.keys():
            symbol = self.optreqIDdict[reqId][0]
            ex = self.optreqIDdict[reqId][1]
            stk = self.optreqIDdict[reqId][2]
            rig = self.optreqIDdict[reqId][3]
            rownum = None
            if self.optionsquotesdict[symbol][ex].quote.empty:
                self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(self.optionsquotesdict[symbol][ex].quote,
                                                                              0, optionnullrow)
                self.optionsquotesdict[symbol][ex].quote.at[0, 'strike'] = stk
                rownum = 0
            else:
                strikeS = list(self.optionsquotesdict[symbol][ex].quote['strike'])
                if stk in strikeS:
                    rownum = strikeS.index(stk)
                else:
                    strikeS.append(stk)
                    strikeS = sorted(strikeS)
                    rownum = strikeS.index(stk)
                    self.optionsquotesdict[symbol][ex].quote = dataframeinsertrow(
                        self.optionsquotesdict[symbol][ex].quote, rownum, optionnullrow)
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'strike'] = stk
            if tickType == 83:
                if rig == 'C':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'IV C'] = impliedVol
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'delta C'] = delta
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'theta C'] = theta
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'vega C'] = vega
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'gamma C'] = gamma

                elif rig == 'P':
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'IV P'] = impliedVol
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'delta P'] = delta
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'theta P'] = theta
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'vega P'] = vega
                    self.optionsquotesdict[symbol][ex].quote.at[rownum, 'gamma P'] = gamma

    def securityDefinitionOptionParameter(self, reqId:int, exchange:str,
        underlyingConId:int, tradingClass:str, multiplier:str,
        expirations:SetOfString, strikes:SetOfFloat):
        print('reqID:', reqId, ' exchange:', exchange, ' underlyingConID:', underlyingConId, ' tradindClass:',
              tradingClass, ' multiplier:', multiplier, ' expirations:', expirations, ' strikes:', strikes)
        if reqId in self.reqOptParamsIDdict.keys():
            if exchange == 'SMART':
                self.reqOptParamsIDdict[reqId].append(expirations)
                self.reqOptParamsIDdict[reqId].append(strikes)
                self.reqOptParamsIDdict[reqId].append(tradingClass)
                self.reqOptParamsIDdict[reqId].append(multiplier)


    def securityDefinitionOptionParameterEnd(self, reqId: int):
        print('options done: ', reqId)
        if reqId in self.reqOptParamsIDdict.keys():
            symbol = self.reqOptParamsIDdict[reqId][0]
            exs = self.reqOptParamsIDdict[reqId][1]
            strs = self.reqOptParamsIDdict[reqId][2]
            trc = self.reqOptParamsIDdict[reqId][3]
            mul = self.reqOptParamsIDdict[reqId][4]

            self.optionsquotesdict[symbol] = {}

            optconC = make_contract(symbol, secType='OPT', tradingClass=trc, multiplier=mul, right='C', exchange='SMART')
            optconP = make_contract(symbol, secType='OPT', tradingClass=trc, multiplier=mul, right='P', exchange='SMART')
            for e in exs:
                self.optionsquotesdict[symbol][e] = optionsdatefram(symbol, e)
                for s in strs:
                    optconC.strike = s
                    optconC.lastTradeDateOrContractMonth = e
                    optconP.strike = s
                    optconP.lastTradeDateOrContractMonth = e
                    self.reqID += 1
                    self.optreqIDdict[self.reqID] = [symbol, e, s, 'C']
                    self.reqMktData(self.reqID, optconC, '106', False, False, [])
                    print('请求期权数据', self.reqID, e, s, 'C')
                    time.sleep(0.021)
                    self.reqID += 1
                    self.optreqIDdict[self.reqID] = [symbol, e, s, 'P']
                    self.reqMktData(self.reqID, optconP, '106', False, False, [])
                    print('请求期权数据', self.reqID, e, s, 'P')
                    time.sleep(0.021)


# if __name__ == '__main__':
#     aapl = make_contract('AAPL', 265598, exchange='SMART')
#     goog = make_contract('GOOG', 208813720, exchange='SMART')
#     clist = [aapl]
#     filepath = r'E:\ibdata'
#     myapp = myClient(clist, filepath)
#     myapp.connect('127.0.0.1', 4002, 0)
#     myapp.run()

