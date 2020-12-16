import matplotlib.pyplot as plt
import pandas as pd
import os

ticksymbol = 'kss'
tickfile = r'D:\IB Data\Tick Data\{}-tick.txt'.format(ticksymbol)
df = pd.read_csv(tickfile, header=None)
price = list(df[5])

totalchg = []
abstotalchg = []
for i in range(len(price)):
    if i > 0:
       chg = (price[i] - price[i - 1]) / price[i - 1]
       totalchg.append(chg)
       abstotalchg.append(abs(chg))

plt.hist(abstotalchg, bins=len(abstotalchg), density=True, cumulative=True)
plt.tight_layout()
plt.title(ticksymbol.upper())
plt.grid()
plt.show()