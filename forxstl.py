import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\\newdata'
forxs = ['EURUSD=X', 'GBPUSD=X', 'JPYUSD=X', 'CHFUSD=X', 'CADUSD=X', 'AUDUSD=X', 'NZDUSD=X'] #  'CADUSD', 'AUDUSD', 'NZDUSD',, 'GLD', 'SLV', 'BTCUSD=X', 'CNYUSD=X'
flen = len(forxs)
dxy = pd.read_csv(path + os.sep + 'DXY.csv')
datalen = 220 * 2

dxyc = list(dxy.tail(datalen)['Close'])
adjdxy = [100 / dxyc[i] for i in range(datalen)]
urio = 100 / adjdxy[0]
usd = [urio * adjdxy[ui] for ui in range(datalen)]


compforx = []
for xi in forxs:
    forx = pd.read_csv(path + os.sep + xi + '.csv')
    forxc = list(forx.tail(datalen)['Close'])

    rio = 100 / forxc[0]
    adjforxc = [i * rio for i in forxc]

    if len(compforx) == 0:
        compforx = adjforxc
        continue
    buff = [(compforx[i] + adjforxc[i]) / flen for i in range(datalen)]

Iu, = plt.plot(usd, label='USD')
Ic, = plt.plot(compforx, label='Forx Comb')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()