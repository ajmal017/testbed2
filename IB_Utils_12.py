from IB_Utils import _myClient, make_contract, ComboLeg, Contract, Order
from ibapi.common import *
from ibapi.ticktype import *
import numpy as np
from threading import Timer
from datetime import datetime
import os
import time


def make_future_spread_combo(symbol: str, buysideID: int, sellsideID: int, exchange: str, currency='USD'):
    comcon = make_contract(symbol, secType='BAG', exchange=exchange, currency=currency)

    legbuy = ComboLeg()
    legbuy.conId = buysideID
    legbuy.ratio = 1
    legbuy.action = 'BUY'
    legbuy.exchange = exchange

    legsell = ComboLeg()
    legsell.conId = sellsideID
    legsell.ratio = 1
    legsell.action = 'SELL'
    legsell.exchange = exchange

    comcon.comboLegs = []
    comcon.comboLegs.append(legbuy)
    comcon.comboLegs.append(legsell)
    return comcon


def make_combo_limit_order(action: str, price: float, quantity=1, transmit=True):
    order = Order()
    order.action = action
    order.orderType = 'LMT'
    order.lmtPrice = price
    order.totalQuantity = quantity
    order.transmit = transmit
    return order


def make_combo_limit_order_child(parentID:int, action: str, price: float, quantity=1):
    order = Order()
    order.parentId = parentID
    order.action = action
    order.orderType = 'LMT'
    order.lmtPrice = price
    order.totalQuantity = quantity
    order.transmit = True
    return order


def make_combo_limit_order_parent_child(parentID:int, parentaction: str, parentprice: float, childprice: float, quantity=1):
    order = Order()
    order.action = parentaction
    order.orderType = 'LMT'
    order.lmtPrice = parentprice
    order.totalQuantity = quantity
    order.transmit = False

    orderc = Order()
    orderc.parentId = parentID
    orderc.action = 'BUY'
    if parentaction == 'BUY':
        orderc.action = 'SELL'
    orderc.orderType = 'LMT'
    orderc.lmtPrice = childprice
    orderc.totalQuantity = quantity
    orderc.transmit = True

    return order, orderc


class myClient_place_orders_futuresgap(_myClient):
    def __init__(self):
        _myClient.__init__(self)
        self.combolist = []
        self.nextID = None
        self.timer = Timer(1, self.Scan)
        self.timer.start()

    def Scan(self):
        while True:
            if self.nextID is not None:
                self.myPlace_Orders(self.combolist)
                print('所有订单发送完成！')
                break

    def get_conlist(self, combolist):
        self.combolist = combolist

    def error(self, reqId: TickerId, errorCode: int, errorString: str):
        print('reqID:', reqId, ' errorCode:', errorCode, ' errorString:', errorString)

    def nextValidId(self, orderId: int):
        if self.nextID is None:
            print('API初始化完成！')
        print('nextValidId:', orderId)
        self.nextID = orderId

    def waitupdateNextID(self, cID:int):
        while True:
            if self.nextID > cID:
                break

    def myPlace_Orders(self, combolist:list):
        for ci in combolist:
            symbol = ci[0].symbol
            for i in range(ci[3]):
                ci[2].parentId = self.nextID

                cID = self.nextID
                self.placeOrder(self.nextID, ci[0], ci[1])
                print(i, '发送父订单', self.nextID)
                self.reqIds(-1)
                self.waitupdateNextID(cID)
                time.sleep(0.03)

                cID = self.nextID
                self.placeOrder(self.nextID, ci[0], ci[2])
                print(i, '发送子订单', self.nextID)
                self.reqIds(-1)
                self.waitupdateNextID(cID)
                time.sleep(0.03)
            print(symbol, '发送完成！')


ES = make_future_spread_combo('ES', 396336017, 383974339, 'GLOBEX')
ESorder, ESorderC = make_combo_limit_order_parent_child(0, 'BUY', -8.9, -8.1, 50)
ESc = [ES, ESorder, ESorderC, 1]

MES = make_future_spread_combo('MES', 396336054, 383974345, 'GLOBEX')
MESorder, MESorderC = make_combo_limit_order_parent_child(0, 'BUY', -9.7, -6.7)
MESc = [MES, MESorder, MESorderC, 20]

NQ = make_future_spread_combo('NQ', 396335999, 383974419, 'GLOBEX')
NQorder, NQorderC = make_combo_limit_order_parent_child(0, 'BUY', -6.6, -4, 50)
NQc = [NQ, NQorder, NQorderC, 1]

MNQ = make_future_spread_combo('MNQ', 396336057, 383974408, 'GLOBEX')
MNQorder, MNQorderC = make_combo_limit_order_parent_child(0, 'BUY', -8.5, -2.5)
MNQc = [MNQ, MNQorder, MNQorderC, 20]

YM = make_future_spread_combo('YM', 412888950, 396335960, 'ECBOT')
YMorder, YMorderC = make_combo_limit_order_parent_child(0, 'BUY', -102, -93, 100)
YMc = [YM, YMorder, YMorderC, 1]

MYM = make_future_spread_combo('MYM', 412888963, 396335954, 'ECBOT')
MYMorder, MYMorderC = make_combo_limit_order_parent_child(0, 'BUY', -106, -88)
MYMc = [MYM, MYMorder, MYMorderC, 20]

RTY = make_future_spread_combo('RTY', 396336027, 383974422, 'GLOBEX')
RTYorder, RTYorderC = make_combo_limit_order_parent_child(0, 'SELL', -2.6, -3.6, 50)
RTYc = [RTY, RTYorder, RTYorderC, 1]

M2K = make_future_spread_combo('M2K', 396335982, 383974342, 'GLOBEX')
M2Korder, M2KorderC = make_combo_limit_order_parent_child(0, 'BUY', -4.5, -1.2)
M2Kc = [M2K, M2Korder, M2KorderC, 20]

SI = make_future_spread_combo('SI', 362937126, 217648764, 'NYMEX')
SIorder, SIorderC = make_combo_limit_order_parent_child(0, 'BUY', 0.095, 0.14, 50)
SIc = [SI, SIorder, SIorderC, 1]

mSI = make_future_spread_combo('SI', 415176807, 397594866, 'NYMEX')
mSIorder, mSIorderC = make_combo_limit_order_parent_child(0, 'BUY', 0.1, 0.115)
mSIc = [mSI, mSIorder, mSIorderC, 20]

GC = make_future_spread_combo('GC', 358917044, 178747429, 'NYMEX')
GCorder, GCorderC = make_combo_limit_order_parent_child(0, 'SELL', 9, 5, 10)
GCc = [GC, GCorder, GCorderC, 1]

if __name__ == '__main__':
    conlist = [SIc]
    app = myClient_place_orders_futuresgap()
    app.get_conlist(conlist)
    app.connect('127.0.0.1', 7497, 2)
    app.run()