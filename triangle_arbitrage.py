import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\\newdata'

f1 = 'EURUSD=X'
f2 = 'GBPUSD=X'

data1 = pd.read_csv(path + os.sep + f1 + '.csv')
data2 = pd.read_csv(path + os.sep + f2 + '.csv')

datalen = 220 * 2

p1 = list(data1.tail(datalen)['Close'])
p2 = list(data2.tail(datalen)['Close'])

ap1 = [1 / p1[i] for i in range(datalen)]
ap2 = [1 / p2[i] for i in range(datalen)]

