import pandas as pd
import math
import os

path = r'E:\newdata\OCC data\Adj Data'
filename = '202006-Mergers-Adj-NonDrop.csv'

pricelimit = 50
savename = '202006-Mergers-Adj-U' + str(pricelimit) + '.csv'

data = pd.read_csv(path + os.sep + filename)
prices = list(data['Underlying Price'])
dropidxs = []
n = 0
for i in prices:
    if math.isnan(i):
        dropidxs.append(n)
    elif i < pricelimit:
        dropidxs.append(n)
    n += 1

data = data.drop(dropidxs).reset_index(drop=True)
data.to_csv(path + os.sep + savename, index=False)