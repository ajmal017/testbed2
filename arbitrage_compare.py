import matplotlib.pyplot as plt
import pandas as pd
import os

# path = 'E:\\newdata'
# path = 'E:\\newdata\cleaneddataFX'
path = 'E:\\newdata\Gold\cleaneddata'
f1 = 'GLD'
f2 = 'GDX'

reverse = False

data1 = pd.read_csv(path + os.sep + f1 + '.csv')
data2 = pd.read_csv(path + os.sep + f2 + '.csv')

datalen = 220 * 1

c1 = list(data1.tail(datalen)['Close'])
c2 = list(data2.tail(datalen)['Close'])

rio1 = 100 / c1[0]
adjc1 = [rio1 * i for i in c1]

if reverse:
    adjc2buff = [1 / i for i in c2]
    rio2 = 100 / adjc2buff[0]
    adjc2 = [rio2 * i for i in adjc2buff]
else:
    rio2 = 100 / c2[0]
    adjc2 = [rio2 * i for i in c2]

diff = [adjc1[i] - adjc2[i] for i in range(len(adjc1))]

I1, = plt.plot(adjc1, label=f1.upper())
I2, = plt.plot(adjc2, label=f2.upper())
# Id, = plt.plot(diff, label='DIFF')

plt.tight_layout()
plt.grid()
plt.legend()
plt.show()



