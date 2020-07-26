import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata2\stocksdata'
pair = ['iyy', 'ivv']
s1 = pd.read_csv(path + os.sep + pair[0] + '.csv')
s2 = pd.read_csv(path + os.sep + pair[1] + '.csv')
dlen = 220

s1 = s1.tail(dlen)
s2 = s2.tail(dlen)
s1C = list(s1['Close'])
s2C = list(s2['Close'])

r1 = 100 / s1C[0]
r2 = 100 / s2C[0]
absr = s1C[0] / s2C[0]

ac1 = [i * r1 for i in s1C]
ac2 = [i * r2 for i in s2C]

diff = [ac1[i] - ac2[i] for i in range(dlen)]

i1, = plt.plot(ac1, label=pair[0].upper())
i2, = plt.plot(ac2, label=pair[1].upper())
i3, = plt.plot(diff, label='diff')
plt.legend()
plt.tight_layout()
plt.title('AbsRio = ' + str(absr))
plt.grid()
plt.show()