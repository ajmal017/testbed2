from PyQt5.QtWidgets import QWidget
from switch_operation_panel import Ui_Form_switch


class Form_switch(QWidget, Ui_Form_switch):
    def __init__(self):
        QWidget.__init__(self)
        Ui_Form_switch.__init__(self)
        self.setupUi(self)

    def slot_update_OCC_data(self):
       pass

    def slot_pick_underlyings(self):
        pass

    def slot_update_underlyings_deltail(self):
        pass

    def slot_reqUnderlyings_price_IV(self):
        pass

    def slot_reqOptions_Params(self):
        pass

    def slot_reqOptions_deltail(self):
        pass

    def slot_place_orders_master(self):
        pass

    def slot_place_orders_chidren(self):
        pass

    def slot_plus_missed_orders(self):
        pass

    def slot_delete_outdatedOrders(self):
        pass

    def slot_one_do_all(self):
        pass