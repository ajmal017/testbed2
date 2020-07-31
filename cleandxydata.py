import pandas as pd
import math
import os

path = 'E:\\newdata'
dxy = pd.read_csv(path + os.sep + 'DX-Y.NYB.csv')
c = list(dxy['Close'])
delidxs = []

for ci in range(len(c)):
    if math.isnan(c[ci]):
        delidxs.append(ci)

dxyc = dxy.drop(index=delidxs).reset_index(drop=True)

dxyc.to_csv(path + os.sep + 'DXY.csv', index=False)