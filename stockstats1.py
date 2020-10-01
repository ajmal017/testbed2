import matplotlib.pyplot as plt
import pandas as pd
import os

clearedfile = r'D:\Other Data\IVE_tickbidask_cleared.csv'
df = pd.read_csv(clearedfile)

price = list(df['Price'])
chglist = []
for i in range(len(price)):
    if i > 0:
        chg = abs((price[i] - price[i - 1]) / price[i - 1])
        if chg > 0:
            chglist.append(chg)

plt.hist(chglist, bins=10000, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.show()