import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = r'E:\stockdata'
vix = pd.read_csv(filepath + os.sep + '^VIX.csv')
vix = vix[: -2]
spikes = pd.read_csv(filepath + os.sep + 'SPIKES.csv')
ll = len(spikes)
vix = vix.tail(ll)
vc = list(vix['Close'])
sc = list(spikes['Price'])
diff = []
for i in range(len(vc)):
    diff.append(sc[i] - vc[i])
i1, = plt.plot(vc, label='VIX')
i2, = plt.plot(sc, label='SPIKES')
i3, = plt.plot(diff, label='diff')
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()

