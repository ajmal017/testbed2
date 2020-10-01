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
from IB_Utils import contract_to_df, _myClient, make_contract
import time
import json
import math
import sys
import io
import os
import re

UnderlyingsPath = r'D:\IB Data\Underlying'
AdjUnderlyingfile = r'D:\IB Data\Adj Underlying\adjunderlyings.csv'
ContractDetailsfile = r'E:\newdata\IB data\Underlying Contract Details\Underlying_Contract_Details.csv'


def mixedType_to_float(x):
    rec = ('C', 'c', ',')
    y = x
    if isinstance(y, str):
        for ri in rec:
            if ri in y:
                y = y.replace(ri, '')
    return float(y)


def isfloat(x):
    gbs = ['inf', 'infinity', 'INF', 'INFINITY', 'True', 'NAN', 'nan', 'False', '-inf', '-INF', '-INFINITY',
           '-infinity', 'NaN', 'Nan']
    rec = ('C', 'c', ',')
    y = x
    if isinstance(y, str):
        for ri in rec:
            if ri in y:
                y = y.replace(ri, '')
    try:
        float(y)
        if str(y) in gbs:
            return False
        else:
            return True
    except:
        return False


def ispercentage(x):
    if isinstance(x, str):
        if '%' not in x:
            return False
        else:
            return True
    else:
        return False


def pick_same_nums(x: list):
    pickednums = []
    for i in range(len(x)):
        if i > 0:
            if x[i] == x[i - 1]:
                pickednums.append(i)
    return pickednums


def Pick_Underlyings(picknum=100, greatIV=0.4, greatVOL=100000):
    files = os.listdir(UnderlyingsPath)
    underlyingdf = ''
    init = False
    for fi in files:
        df = pd.read_csv(UnderlyingsPath + os.sep + fi, encoding='gb18030', thousands=',')
        if not init:
            underlyingdf = df
            init = True
        else:
            underlyingdf = underlyingdf.append(df, ignore_index=True)

    underlyingdf = underlyingdf.reset_index(drop=True)
    underlyingdf = underlyingdf.loc[:, ~underlyingdf.columns.str.contains('Unnamed')]

    IV = list(underlyingdf['期权隐含波动率%'])
    last = list(underlyingdf['最后价'])
    avgVol = list(underlyingdf['平均交易量'])

    delnums = []
    for li in range(len(last)):
        if not isfloat(last[li]):
            delnums.append(li)
    for ai in range(len(avgVol)):
        if not isfloat(avgVol[ai]):
            delnums.append(ai)
    for Ii in range(len(IV)):
        if not ispercentage(IV[Ii]):
            delnums.append(Ii)

    delnums = list(set(delnums))
    underlyingdf = underlyingdf.drop(index=delnums).reset_index(drop=True)
    IV = list(underlyingdf['期权隐含波动率%'].str.strip('%').astype(float) / 100)
    underlyingdf['期权隐含波动率'] = IV

    underlyingdf['最后价'] = [mixedType_to_float(i) for i in underlyingdf['最后价']]
    underlyingdf['平均交易量'] = [int(mixedType_to_float(i)) for i in underlyingdf['平均交易量']]
    underlyingdf.sort_values('金融产品', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)

    symbols = list(underlyingdf['金融产品'])
    delnums2 = pick_same_nums(symbols)
    underlyingdf = underlyingdf.drop(index=delnums2).reset_index(drop=True)
    underlyingdf.sort_values('期权隐含波动率', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)

    IV = list(underlyingdf['期权隐含波动率'])
    if IV[-1] > greatIV:
        pass
    elif IV[0] < greatIV:
        input('无IV大于{}的标的！'.format(greatIV))
        print('程序退出！')
        sys.exit(2)
    else:
        for ii in range(len(IV)):
            if IV[ii] < greatIV:
                underlyingdf = underlyingdf[: ii]
                break

    buffdf = deepcopy(underlyingdf)
    buffdf.sort_values('平均交易量', ascending=False, inplace=True)
    buffdf = buffdf.reset_index(drop=True)
    underlyingdf = deepcopy(buffdf)
    avgVol = list(underlyingdf['平均交易量'])
    if avgVol[-1] > greatVOL:
        pass
    elif avgVol[0] < greatVOL:
        input('无avgVOL大于{}的标的！'.format(greatVOL))
        print('程序退出！')
        sys.exit(3)
    else:
        for ai in range(len(avgVol)):
            if avgVol[ai] < greatVOL:
                underlyingdf = underlyingdf[: ai]
                break

    underlyingdf.sort_values('期权隐含波动率', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)
    if len(underlyingdf) > picknum:
        underlyingdf = underlyingdf.head(picknum)

    underlyingdf.to_csv(AdjUnderlyingfile, index=False)

    print('挑选标的完成，共选中{}个标的！'.format(len(underlyingdf)))
    return underlyingdf


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
                print('丢失的Symbols:', nonr)

            self.superdf.reset_index(drop=True)
            if os.path.exists(ContractDetailsfile):
                edf = pd.read_csv(ContractDetailsfile)
                self.superdf = edf.append(self.superdf, ignore_index=True).reset_index(drop=True)
            self.superdf.to_csv(ContractDetailsfile, index=False)
            print('Underlying Contract Details 文件已生成！')
            timer.cancel()
            sys.exit(0)
            # self.disconnect()
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


def get_underlying_details():
    adjsymbols = list(pd.read_csv(AdjUnderlyingfile)['金融产品'])
    esymbols = []
    if os.path.exists(ContractDetailsfile):
        esymbols = list(pd.read_csv(ContractDetailsfile)['symbol'])
    reqsymbols = []
    for i in adjsymbols:
        if i not in esymbols:
            reqsymbols.append(i)

    app = myClient_get_underlying_details(reqsymbols)
    app.connect('127.0.0.1', 7497, 1)
    app.run()


class myClient_get_opt_params(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.reqConsdict = {}
        self.recivedreqid = []
        self.non_recivedreqid = []

    def scan(self):
        timer = Timer(0.2, self.scan)
        reqidnums = list(self.reqConsdict.keys())
        if len(reqidnums) == len(self.recivedreqid + self.non_recivedreqid) and len(reqidnums) > 0:
            if len(self.non_recivedreqid) > 0:
                nonr = [self.reqConsdict[i] for i in self.non_recivedreqid]
                nondf = pd.DataFrame(data={'Symbol': nonr})
                nonsavename = r'E:\newdata\IB data\Missed Symbols-Opt Params.csv'
                nondf.to_csv(nonsavename, index=False)
            print('所有文件写入已完成！')
            timer.cancel()
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
        file = ContractDetailsfile
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
        # print('所有期权Params获取结束！')
        pass


def get_opt_params():
    app = myClient_get_opt_params()
    app.connect('127.0.0.1', 7497, 1)
    app.run()


# Pick_Underlyings(greatVOL=20000)

# get_underlying_details()

# get_opt_params()