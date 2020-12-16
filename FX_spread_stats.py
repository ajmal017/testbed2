import matplotlib.pyplot as plt
import pandas as pd
import os


symbol = 'XAUUSD'
month = 202005
file = r'D:\IB Data\Tick Data FX\{}-tick.txt'.format(symbol)
HISTfile = r'D:\HIST Data\unPacked\{}\DAT_ASCII_XAUUSD_T_{}.csv'.format(symbol, month)

df = pd.read_csv(HISTfile, header=None)
dl = len(df)
spreds = df[2] - df[1]

bins = dl
if dl > 10000:
    bins = 10000
plt.hist(spreds, bins=bins, density=True, cumulative=True)
plt.tight_layout()
plt.title(symbol)
plt.grid()
plt.show()
