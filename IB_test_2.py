from IB_Utils_4_1 import myIB_Pro_Client_2
from IB_Utils_2 import Pick_Underlyings
from IB_Utils import pick_stricks_2, IBdate_to_Date
from IB_Utils_3 import Json_to_Dict, Dict_to_Contract, make_order, make_combo_Switch
from threading import Timer, Thread, Lock
from IB_Utils_4_1 import check_delete_bad_specs_2
from datetime import date
from copy import deepcopy
import pandas as pd
import time
import os

<<<<<<< HEAD
UDfile = r'D:\IB Data\Adj Underlying\adjunderlyings.csv'
UDpath = r'D:\IB Data\Underlying Details'
OSpath = r'D:\IB Data\Option Specs'

if __name__ == '__main__':
    SENT_ORDERS = True

    if SENT_ORDERS:
        # Pick_Underlyings(greatIV=0.6, greatVOL=200000)
        pass

    UDdf = pd.read_csv(UDfile)
    app = myIB_Pro_Client_2(UDdf, True)

    if SENT_ORDERS:
        sy = app.reqContract_STK_batch()
        excludesymbols = ['GRAF']
        for i in excludesymbols:
            if i in sy:
                sy.remove(i)
        app.reqOPT_Paras_Details_batch(symbols=sy)
=======
OSpath = r'E:\newdata\IB data\Option Specs'
UDpath = r'E:\newdata\IB data\Underlying Details'
UDfile = r'E:\newdata\IB data\adjunderlying\adjunderlyings.csv'

if __name__ == '__main__':
    SENT_ORDERS = False

    # if SENT_ORDERS:
    #     Pick_Underlyings(greatIV=0.6, greatVOL=150000)

    UDdf = pd.read_csv(UDfile)
    app = myIB_Pro_Client_2(UDdf, isTWS=False)

    if SENT_ORDERS:
        sy = app.reqContract_STK_batch()
        excludesymbols = ['GRAF', 'SHLL', 'HYLN']
        for i in excludesymbols:
            if i in sy:
                sy.remove(i)
        # app.reqOPT_Paras_Details_batch(symbols=sy)
>>>>>>> origin/master

        ds = check_delete_bad_specs_2(OSpath)

        Total_Init_Capital = app.AccontValue_details['Total_Init_Capital']

        OSfiles = os.listdir(OSpath)
        validOrderSymbols = []
        for si in app.dfsymbols:
<<<<<<< HEAD
            sisp = si + '-specs.json'
            if sisp in OSfiles:
                validOrderSymbols.append(si)
=======
            if si not in excludesymbols:
                sisp = si + '-specs.json'
                if sisp in OSfiles:
                    validOrderSymbols.append(si)
>>>>>>> origin/master

        today = date.today()
        OID = app.NextValidID
        ChildOrders = []

        for si in validOrderSymbols:
            if app.place_orders_choice_data['API_over_Capital_total']:
                break
            if si not in app.place_orders_choice_data['Singular_over_Capital']:
                if si in app.OpenOrder_details['CancelableOrderIDs_Class'].keys():
                    cids = app.OpenOrder_details['CancelableOrderIDs_Class'][si]['BUY'] +\
                           app.OpenOrder_details['CancelableOrderIDs_Class'][si]['SELL']
                    if len(cids) != 0:
                        app.reqCancel_Order_batch(cids)

                specsfile = OSpath + os.sep + si + '-specs.json'
                specs = Json_to_Dict(specsfile)
                for month, data in specs.items():
                    datefmonth = IBdate_to_Date(month)
                    if datefmonth > today:
                        idx = app.dfsymbols.index(si)
                        last = app.dfPrice[idx]
                        IV = app.dfIVs[idx]

                        strs = list(sorted(list(data['C'].keys())))
                        strs = [float(stri) for stri in strs]
                        pickedstrs = pick_stricks_2(last, strs, 10)
                        greats = []
                        lesss = []
                        for psi in pickedstrs:
                            if 0.7 <= psi / last < 1:
                                lesss.append(psi)
                            elif 1 <= psi / last <= 1.3:
                                greats.append(psi)

                        UDfile = UDpath + os.sep + si + '-Details.json'
                        UDcontract = Dict_to_Contract(Json_to_Dict(UDfile))
                        pricerio = pow(IV / 0.4, 0.5) * 0.04

                        existforth = None
                        if si in app.place_orders_choice_data['Singular_Right'].keys():
                            existforth = app.place_orders_choice_data['Singular_Right'][si]
                        if existforth is None or existforth:
                            for gi in greats:
                                limitPrice = round(gi * (1 - pricerio), 2)
                                quantity = round((Total_Init_Capital * 0.8 * 2.5) / (50 * limitPrice * 100))
                                if quantity > 0:
                                    call = Dict_to_Contract(data['C'][str(gi)])
                                    put = Dict_to_Contract(data['P'][str(gi)])
                                    combo_buy = make_combo_Switch(UDcontract, call, put)

                                    Porder = make_order(action='BUY', quantity=quantity, limitPrice=limitPrice, transmit=False)
                                    op = app.Place_Order_Singal(OID, combo_buy, Porder)

                                    Corder = make_order(action='SELL', quantity=quantity, limitPrice=gi, parentId=OID, transmit=True)
                                    ChildOrders.append((deepcopy(combo_buy), deepcopy(Corder)))
                                    OID += 1

                        if existforth is None or not existforth:
                            for li in lesss:
                                limitPrice = round(li * (1 + pricerio), 2)
                                quantity = round((Total_Init_Capital * 0.8 * 2.5) / (50 * limitPrice * 100))
                                if quantity > 0:
                                    call = Dict_to_Contract(data['C'][str(li)])
                                    put = Dict_to_Contract(data['P'][str(li)])
                                    combo_sell = make_combo_Switch(UDcontract, call, put)

                                    Porder = make_order(action='SELL', quantity=quantity, limitPrice=limitPrice, transmit=False)
                                    op = app.Place_Order_Singal(OID, combo_sell, Porder)

                                    Corder = make_order(action='buy', quantity=quantity, limitPrice=li, parentId=OID, transmit=True)
                                    ChildOrders.append((deepcopy(combo_sell), deepcopy(Corder)))
                                    OID += 1

        if not app.place_orders_choice_data['API_over_Capital_total']:
            app.Place_Order_batch(ChildOrders)

    while True:
        time.sleep(3)
