from threading import Timer, Thread, Lock
from IB_Utils_4 import myClient_m_2
# from IB_Utils_4_1 import myIB_Pro_Client_2
import pandas as pd


class myIB_Thread(Thread):
    def __init__(self, myIB_Pro_Client, UDdf: pd.DataFrame):  #: myIB_Pro_Client_2
        Thread.__init__(self)
        self.myIB_Pro_Client = myIB_Pro_Client
        self.UDdf = UDdf
        self.app = myClient_m_2(ProClient=self.myIB_Pro_Client, UDdf=self.UDdf)

    def run(self):

        self.app.connect('127.0.0.1', 7497, 1)
        self.app.run()