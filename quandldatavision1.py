import matplotlib.pyplot as plt
from matplotlib import cm
import functools
import pandas as pd
import numpy as np
import os


def myfilenamesort(x, y):
    xb = int(x.split('.')[0].split('-')[-1])
    yb = int(y.split('.')[0].split('-')[-1])
    if xb < yb:
        return -1
    elif xb > yb:
        return 1
    else:
        return 0


path = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data'
filelist = os.listdir(path)
filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort))

superdata = []
datenum = []
fl = len(filelist)
dl = 0
for fi in filelist:
    data = pd.read_csv(path + os.sep + fi)
    close = list(data['Last'])
    datenum = list(data['Date NO.'])
    dl = len(close)
    superdata.append(close)


fig = plt.figure()
ax1 = plt.axes(projection='3d')

x = list(range(fl))
X = np.array([x for i in range(dl)])
Y = np.rot90(np.array([datenum for i in range(fl)]), -1)
z = np.array(superdata).T
Z = []
for i in z:
    bp = i[0]
    zi = (i - bp) / bp
    lzi = list(zi)
    Z.append(lzi)

Z = np.array(Z)

ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=5, antialiased=False)
plt.tight_layout()
plt.show()