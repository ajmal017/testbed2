import matplotlib.pyplot as plt
import pandas as pd
import os

dapath = r'D:\Yahoo Data\Stocks'
symbol = 'DIS'
file = dapath + os.sep + symbol + '.csv'

df = pd.read_csv(file)
df = df.tail(5000)
c = df['Close'].values
h = df['High'].values
l = df['Low'].values

pren = 1
subn = 5
abvp = 0.05

skipn = []

pchg = []
subchg = []

dn = len(c)
for i in range(dn):
    if i >= pren + subn:
        if i not in skipn:
            print(i)
            preche = c[i - subn]
            prechs = c[i - subn - pren]
            prech = abs((preche - prechs) / prechs)
            if prech >= abvp:
                pchg.append(prech)
                subchmax = max(h[i - subn + 1: i + 1])
                subchmin = min(l[i - subn + 1: i + 1])
                maxch = abs((subchmax - c[i - subn]) / c[i - subn])
                minch = abs((subchmin - c[i - subn]) / c[i - subn])
                chg = maxch
                if minch > maxch:
                    chg = minch
                subchg.append(chg)
                skipn = range(i + 1, i + subn + 1)

lb = len(subchg)
if lb > 1000:
    lb = 1000
plt.hist(subchg, bins=lb, density=True, cumulative=True)
# plt.hist(subchg, bins=100, density=True, cumulative=False)
# plt.scatter(pchg, subchg)
plt.tight_layout()
plt.grid()
plt.title(symbol)
plt.show()
