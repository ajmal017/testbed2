import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
# stickers = ['uvxy', 'vxx', 'vixy', 'vixm', 'tvix', 'viix']
stickers = ['CNY', 'CYB']
pdata = {}
pdatac = {}

for s in stickers:
    pdata[s] = pd.read_csv(path + os.sep + s + '.csv')
    pdatac[s] = list(pdata[s]['Close'])
minl = 10000000000
for c in pdatac.values():
    l = len(c)
    if minl > l:
        minl = l
cor = {}
adjdatac = {}
for ck, cv in pdatac.items():
    scl = cv[len(cv) - minl:]
    cor = 100 / scl[0]
    adjl = [i * cor for i in scl]
    adjdatac[ck] = adjl
legenl = []
for adk, adv in adjdatac.items():
    I = 0
    legenl.append(I)
    legenl[-1], = plt.plot(adv, label=adk.upper())
plt.tight_layout()
plt.grid()
plt.legend()
plt.show()



