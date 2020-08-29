import matplotlib.pyplot as plt
import pandas as pd
import os

path = r'E:\newdata\dictatorships fx\work data'

lenth = 648
IRR = pd.read_csv(path + os.sep + 'IRRUSD=X.csv')
IRR_C = list(IRR['Close'])


RUB = pd.read_csv(path + os.sep + 'RUBUSD=X.csv')
RUB_C = list(RUB['Close'])

PKR = pd.read_csv(path + os.sep + 'PKR=X.csv')
PKR_Cr = list(PKR['Close'])
PKR_C = [1 / i for i in PKR_Cr]

# VES = pd.read_csv(path + os.sep + 'USD_VES历史数据.csv', thousands=',').head(lenth)
# VES_Crr = list(VES['收盘'])
# VES_Cr = list(reversed(VES_Crr))
# VES_C = [1 / i for i in VES_Cr]

Ii, = plt.plot(IRR_C, label='IRR')
Ir, = plt.plot(RUB_C, label='RUB')
Ip, = plt.plot(PKR_C, label='PKR')
# Iv, = plt.plot(VES_C, label='VES')
plt.tight_layout()
plt.grid()
plt.legend()
plt.show()