from IB_Utils_4 import myClient_m_2
import pandas as pd


class myClient_m_conversion(myClient_m_2):
    def __init__(self, ProClient, UDdf: pd.DataFrame):
        myClient_m_2.__init__(self, ProClient=ProClient, UDdf=UDdf)
        self.place_orders_choice_data = {}

    def extendFunc(self):
        place_orders_choice_data = {'API_over_Capital_total': False, 'Singular_over_Capital': [], 'Singular_Right': {}}

        API_over_Capital_total = self.AccontValue_details['ABS_API_Capital'] > \
                                 self.AccontValue_details['Total_Init_Capital'] * 0.8 * 2.5
        if API_over_Capital_total:
            Cancel_Order_IDs_All = self.OpenOrder_details['CancelableOrderIDs']
            if len(Cancel_Order_IDs_All) != 0:
                print('API资金超限， 撤销所有订单！')
                self.reqCancel_Orders_batch(Cancel_Order_IDs_All)

            place_orders_choice_data['API_over_Capital_total'] = True

        for sym, v in self.AccontValue_details['API_Capital_Class'].items():
            if abs(v) > self.AccontValue_details['Total_Init_Capital'] * 0.8 * 2.5 / 10:
                if sym in self.OpenOrder_details['CancelableOrderIDs_Class'].keys():
                    Cancel_Order_IDs_Singular = self.OpenOrder_details['CancelableOrderIDs_Class'][sym]['BUY'] +\
                                                self.OpenOrder_details['CancelableOrderIDs_Class'][sym]['SELL']
                    if len(Cancel_Order_IDs_Singular) != 0:
                        print(sym, '资金超限， 撤销其所有订单！')
                        self.reqCancel_Orders_batch(Cancel_Order_IDs_Singular)

                place_orders_choice_data['Singular_over_Capital'].append(sym)

        for sym, v in self.Position_details.items():
            Uposkey = list(v['underlying'].keys())[0]
            Upos = v['underlying'][Uposkey]['position']
            Cancel_Order_IDs_Singular_Right = []
            posright = True
            if Upos > 0:
                if sym in self.OpenOrder_details['CancelableOrderIDs_Class'].keys():
                    Cancel_Order_IDs_Singular_Right = self.OpenOrder_details['CancelableOrderIDs_Class'][sym]['SELL']
            else:
                posright = False
                if sym in self.OpenOrder_details['CancelableOrderIDs_Class'].keys():
                    Cancel_Order_IDs_Singular_Right = self.OpenOrder_details['CancelableOrderIDs_Class'][sym]['BUY']

            if len(Cancel_Order_IDs_Singular_Right) != 0:
                if posright:
                    print(sym, '已有 多头 头寸， 撤销其所有 空头 订单！')
                else:
                    print(sym, '已有 空头 头寸， 撤销其所有 多头 订单！')
                self.reqCancel_Orders_batch(Cancel_Order_IDs_Singular_Right)

            place_orders_choice_data['Singular_Right'][sym] = posright

        self.place_orders_choice_data = place_orders_choice_data
        self.ProClient.place_orders_choice_data = place_orders_choice_data
