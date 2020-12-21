from Quandl_Utils import QuandlDfCleaner_2
import matplotlib.pyplot as plt
import pandas as pd
from copy import deepcopy
import os

ustpath = r'E:\newdata\quandl data\Maturity Rate'
ustlist = os.listdir(ustpath)

ustdflist = []
names = []
for i in ustlist:
    names.append(i.split('.')[0])
    usti = pd.read_csv(ustpath + os.sep + i)
    ustdflist.append(deepcopy(usti))

adjustlist = QuandlDfCleaner_2(ustdflist, cvalue='Value', dfreverse=True)
Ls = []
n = 0
for ai in adjustlist:
    rate = list(ai['Value'])
    li = ''
    Ls.append(li)
    Ls[-1], = plt.plot(rate, label=names[n])
    n += 1

plt.legend()
plt.tight_layout()
plt.grid()
plt.show()