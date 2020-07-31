import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\\newdata'
forxs = ['EURUSD=X', 'GBPUSD=X', 'JPYUSD=X', 'CHFUSD=X', 'CNYUSD=X'] #  'CADUSD', 'AUDUSD', 'NZDUSD',, 'BTCUSD=X', 'GLD', 'SLV'
dxy = pd.read_csv(path + os.sep + 'DXY.csv')
datalen = 2200
dxyc = list(dxy.tail(datalen)['Close'])
adjdxy = [dxyc[i] / 100 for i in range(datalen)]

ls = []
for xi in forxs:
    forx = pd.read_csv(path + os.sep + xi + '.csv')
    forxc = list(forx.tail(datalen)['Close'])
    adjforxc = [forxc[i] * adjdxy[i] for i in range(datalen)]
    rio = 100 / adjforxc[0]
    adjforxcp = [i * rio for i in adjforxc]
    li = ''
    ls.append(li)
    ls[-1], = plt.plot(adjforxcp, label=xi)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()