import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
cyb = pd.read_csv(path + os.sep + 'CYB.csv')
cny = pd.read_csv(path + os.sep + 'CNY.csv')
dlen = min(len(cyb), len(cny))

cyb = cyb.tail(dlen)
cny = cny.tail(dlen)
cybC = list(cyb['Close'])
cnyC = list(cny['Close'])

bc = [1 / i for i in cybC]
yc = [1 / i for i in cnyC]

br = 1 / bc[0]
yr = 1 / yc[0]

abc = [i * br for i in bc]
ayc = [i * yr for i in yc]

diff = [(abc[i] - ayc[i]) * 1 for i in range(dlen)]

i1, = plt.plot(abc, label='CYB')
i2, = plt.plot(ayc, label='CNY')
i3, = plt.plot(diff, label='diff')
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()