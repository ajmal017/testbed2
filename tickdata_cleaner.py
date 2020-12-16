import pandas as pd
import os

sapfile = r'D:\Other Data\IVE_tickbidask.csv'
df = pd.read_csv(sapfile)
price = list(df['Price'])

delnums = []
for i in range(len(price)):
    if price[i] <= 20:
        delnums.append(i)
    if i > 0:
        chg = abs((price[i] - price[i - 1]) / price[i - 1])
        if chg > 0.1:
            delnums.append(i)

fdf = df.drop(delnums).reset_index(drop=True)
clearedfile = r'D:\Other Data\IVE_tickbidask_cleared.csv'
fdf.to_csv(clearedfile, index=False)
