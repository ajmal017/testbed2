from threading import Timer, Thread, Lock
from ibapi.contract import Contract, ContractDetails, ComboLeg
from ibapi.order import Order
from IB_Utils_3 import Json_to_Dict
# from IB_Utils_4_2 import myIB_Thread
from IB_Utils_4 import myClient_m_2
from IB_Utils_5 import myClient_m_conversion
import pandas as pd
import time
import os


def check_delete_bad_specs(ospath: str, oppath: str):
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


def check_delete_bad_specs_2(ospath: str):
    specsfilelist = os.listdir(ospath)
    deletedsymbols = []
    for si in specsfilelist:
        symbol = si.split('-')[0]
        filename = ospath + os.sep + si
        try:
            jd = Json_to_Dict(filename)
            for month, mv in jd.items():
                sc = list(sorted(list(mv['C'].keys())))
                sp = list(sorted(list(mv['P'].keys())))
                if sc != sp:
                    os.remove(filename)
                    print('删除残缺文件：', filename)
                    deletedsymbols.append(symbol)
                    break
        except:
            os.remove(filename)
            print('删除残缺文件：', filename)
            deletedsymbols.append(symbol)
    return deletedsymbols


class myIB_Pro_Client_2():
    def __init__(self, UDdf: pd.DataFrame, isTWS=True):
        self.API_Client = myClient_m_conversion(ProClient=self, UDdf=UDdf)
        self.runAPI_Timer = Timer(0.01, self.runAPI)
        self.isTWS = isTWS

        self.OpenOrder = {}
        self.OrderStatus = {}
        self.AccontValue = {}
        self.Position = {}
        self.NextValidID = 0

        self.dfsymbols = None
        self.dfIVs = None
        self.dfPrice = None

        self.AccontValue_details = {}
        self.Position_details = {}
        self.Position_details_exc = {}
        self.OpenOrder_details = {}
        self.place_orders_choice_data = {}

        self.APIfuncID = None
        self.APIfuncParameters = None
        self.APIreturnValues = None
        self.InitDone = False
        self.runAPI_Timer.start()
        while not self.InitDone:
            print('API初始化中......')
            time.sleep(0.1)
        print('API初始化完成！')

    def runAPI(self):
        port = 7497
        if not self.isTWS:
            port = 4002
        self.API_Client.connect('127.0.0.1', port, 1)
        self.API_Client.run()

    def scanAPIreturnValues(self):
        while True:
            if not (self.APIreturnValues is None):
                reValues = self.APIreturnValues
                self.APIreturnValues = None
                return reValues

    def reqContract_STK_batch(self):
        self.APIfuncID = 0
        return self.scanAPIreturnValues()

    def reqOPT_Paras_Details_batch(self, symbols: list, maxstricklimit=0.2, lessthanday=120):
        self.APIfuncID = 1
        self.APIfuncParameters = {}
        self.APIfuncParameters['symbols'] = symbols
        self.APIfuncParameters['maxstricklimit'] = maxstricklimit
        self.APIfuncParameters['lessthanday'] = lessthanday
        return self.scanAPIreturnValues()

    def reqCancel_Order_batch(self, orderIds: list):
        self.APIfuncID = 3
        self.APIfuncParameters = orderIds
        return self.scanAPIreturnValues()

    def Place_Order_batch(self, IDs_Contrcats_Orders: list):
        self.APIfuncID = 4
        self.APIfuncParameters = IDs_Contrcats_Orders
        return self.scanAPIreturnValues()

    def Place_Order_Singal(self, orderId:int, contract: Contract, order: Order):
        self.APIfuncID = 5
        self.APIfuncParameters = {'orderId': orderId, 'contract': contract, 'order': order}
        return self.scanAPIreturnValues()







