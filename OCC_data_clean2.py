import pandas as pd
import os

path = r'E:\newdata\OCC data\Adj Data'
mvname = '202006-Full-M.csv'
yvname = '202006-Full-Y.csv'
savename = '202006-Mergers.csv'

dl = 200
mv = pd.read_csv(path + os.sep + mvname)[:dl]
yv = pd.read_csv(path + os.sep + yvname)[:dl]

mvs = list(mv['Options Class'])
yvs = list(yv['Options Class'])

mergers = []
n = 0
for i in mvs:
    if i in yvs:
        mergers.append(n)
    n += 1

mergerdata = pd.DataFrame()
for mi in mergers:
    ps = mv.iloc[mi]
    mergerdata = mergerdata.append(ps, ignore_index=True)

mergerdata.to_csv(path + os.sep + savename, index=False)
