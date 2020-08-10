import matplotlib.pyplot as plt
import pandas as pd
import os

# path = 'E:\\newdata'
# path = 'E:\\newdata\cleaneddataFX'
path = 'E:\\newdata\IV Data\Gold\cleaneddata'
f1 = '黄金期货历史数据'
f2 = 'XAU_USD历史数据'

reverse = False

data1 = pd.read_csv(path + os.sep + f1 + '.csv')
data2 = pd.read_csv(path + os.sep + f2 + '.csv')

datalen = 220 * 10

c1 = list(data1['收盘'])
c2 = list(data2['收盘'])

adjc1 = list(reversed(c1))[-1 * datalen: -1]
adjc2 = list(reversed(c2))[-1 * datalen: -1]

diff = [adjc1[i] - adjc2[i] for i in range(len(adjc1))]

I1, = plt.plot(adjc1, label='Gold Future')
I2, = plt.plot(adjc2, label='Gold Spot')
Id, = plt.plot(diff, label='DIFF')

plt.tight_layout()
plt.grid()
plt.legend()
plt.show()