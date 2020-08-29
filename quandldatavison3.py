from datetime import date, timedelta
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

rio = 0.5
fl = len(filelist)

data = pd.read_csv(path + os.sep + filelist[0])
daten = list(data['Date'])
datenumf = list(data['Date NO.'])
sdatanums = []
month = []
initddate = date.fromisoformat(daten[0])

dn = 0
for di in daten:
    ddate = date.fromisoformat(di)
    if initddate.year == ddate.year and initddate.month == ddate.month:
        month.append(dn)
    else:
        initddate = date.fromisoformat(di)
        if len(month) > 1:
            mnus = list(range(len(month)))
            snum = round(len(month) * rio)
            idx = mnus.index(snum)
            datanum = month[idx]
            sdatanums.append(datanum)
        else:
            sdatanums.append(month[0])
        month = [dn]

    dn += 1

dl = len(sdatanums)
datenum = [datenumf[di] for di in sdatanums]

superdata = []
for fi in filelist:
    sdata = pd.read_csv(path + os.sep + fi)
    c = sdata['Last']
    clist = [c[ci] for ci in sdatanums]
    superdata.append(clist)


# x = list(range(fl))
# X = np.array([x for i in range(dl)])
# Y = np.rot90(np.array([datenum for i in range(fl)]), -1)
z = np.array(superdata).T
Z = []
for i in z:
    bp = i[0]
    zi = (i - bp) / bp
    lzi = list(zi)
    Z.append(lzi)

Z = np.array(Z)


for i in Z:
    plt.plot(i)
    ul = max(i)
    dol = min(i)
    maxn = list(i).index(ul)
    minn = list(i).index(dol)
    tti = 'Max = ' + str(maxn) + ', Min = ' + str(minn)
    l6x = [7, 7]
    l6y = [ul, dol]
    plt.plot(l6x, l6y)
    l20x = [19, 19]
    l20y = [ul, dol]
    plt.plot(l20x, l20y)
    plt.title(tti)
    plt.tight_layout()
    plt.grid()
    plt.show()

# fig = plt.figure()
# ax1 = plt.axes(projection='3d')
# ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=5, antialiased=False)
# plt.tight_layout()
