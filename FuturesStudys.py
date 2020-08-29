import matplotlib.pyplot as plt
import pandas as pd
import math
import os


dl = 220 * 10

path = r'E:\newdata\IB data'
ng = pd.read_csv(path + os.sep + 'ho=F.csv').tail(dl).reset_index(drop=True)

C = list(ng['Close'])
delidxs = [di for di in range(len(C)) if math.isnan(C[di])]
ng = ng.drop(index=delidxs).reset_index(drop=True)

C = list(ng['Close'])
Date = list(ng['Date'])

datadict = {}
year = int(Date[0].split('-')[0])

sn = 0
for i in range(len(Date)):
    iy = int(Date[i].split('-')[0])
    if year != iy:
        datadict[year] = C[sn: i]
        year += 1
        sn = i
    if i == len(Date) - 1:
        datadict[year] = C[sn:]


Is = []
for k, v in datadict.items():
    Ii = ''
    Is.append(Ii)
    Is[-1], = plt.plot(v, label=str(k))
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()

