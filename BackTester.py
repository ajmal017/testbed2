import pandas as pd
from random import randint
import copy
import os


class order:
    def __init__(self, symbol, openbarnum, openprice, currentbarnum, shares=1):
        self.Symbol = symbol
        self.OrderNum = None
        self.OpenBarNum = openbarnum
        self.CloseBarNum = None
        self.OpenPrice = openprice
        self.ClosePrice = None
        self.CurrentBarNum = currentbarnum
        self.CurrentBarNumList = [currentbarnum]
        self.Shares = shares
        self.InitAsset = 0
        self.TotalAsset = 0
        self.TotalAssetList = []
        self.Status = False

    def rolling(self):
        pass


class backtester:
    def __init__(self, tickerdatas:dict, initasset=100000):
        self.TickerDatas = tickerdatas
        self.InitAsset = initasset
        self.TotalAsset = initasset
        self.TotalAssetList =[initasset]
        self.AvailableAsset = initasset
        self.AvailableAssetList = [initasset]
        self.OccupedAsset = 0
        self.OccupedAsset = []
        self.CurrentBarNum = 0
        self.MassOrderlist = []
        self.SymbolOrderDict = {}
        self.IfOrderDict = {}
        self.DataLen = 0
        for k, v in tickerdatas.items():
            self.SymbolOrderDict[k] = []
            self.IfOrderDict[k] = False
            self.DataLen = len(v)

    def rolling(self):
        pass

    def updatedatas(self):
        pass


class mybacktester(backtester):
    def __init__(self, tickerdatas:dict, initasset=100000):
        backtester.__init__(self, tickerdatas, initasset)

    def rolling(self, win=45, randomNum=0.1, bias=0.01, closerio=0.03, sk=0.65, asrio=0.2):
        RandNumDict = {}
        for i in range(self.DataLen):
            for k, v in self.TickerDatas.items():
                o = v['Open']
                c = v['Close']
                h = v['High']
                l = v['Low']
                if i == 0:
                    RandNumDict[k] = randint(0, 100)
                if i == RandNumDict[k]:
                    if self.IfOrderDict[k]:
                        op = o[i]

                        od = order(k, i, op, i)