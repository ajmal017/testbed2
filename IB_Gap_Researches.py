import matplotlib.pyplot as plt
from myfuncs import cumcovert
from functools import cmp_to_key
import pandas as pd
import numpy as np
import os


def myCMP(x: tuple, y: tuple):
    if x[0] > y[0]:
        return 1
    elif x[0] < y[0]:
        return -1
    else:
        return 0


Fpath = r'E:\stockdata2\stocksdata'
filelist = os.listdir(Fpath)[:100]

rlen = 1
gaplist = []
changelist = []
for fi in filelist:
    file = Fpath + os.sep + fi
    df = pd.read_csv(file)
    c = df['Close'].to_list()
    o = df['Open'].to_list()

    for i in range(len(o)):
        if i > rlen + 1:
            if c[i - 1] >= 15 and o[i] >= 15 and c[i - 1 - rlen] >= 15:
                gap = (o[i] - c[i - 1]) / c[i - 1]
                change = (c[i - 1] - c[i - 1 - rlen]) / c[i - 1 - rlen]
                # if abs(gap) > 0.03:
                gaplist.append(gap)
                changelist.append(change)

# cmax = max(changelist)
# cmin = min(changelist)
#
# changeev = np.linspace(-0.15, 0.15, num=50)
# gapev = []
# gapevP = []
cumt = []
# for ci in range(len(changeev)):
#     if ci > 0:
#         tn = 0
#         gn = 0
#         gnp = 0
for i in range(len(changelist)):
    if abs(gaplist[i]) >= 0.03:
        cumt.append((abs(changelist[i]), 1))
    else:
        cumt.append((abs(changelist[i]), 0))
        #     if changeev[ci - 1] <= changelist[i] < changeev[ci]:
        #         tn += 1
        #         if gaplist[i] >= 0.03:
        #             gn += 1
        #         elif gaplist[i] <= -0.03:
        #             gnp += 1
        # if tn == 0:
        #     if len(gapev) == 0:
        #         gapev.append(0)
        #     else:
        #         gapev.append(gapev[-1])
        #
        #     if len(gapevP) == 0:
        #         gapevP.append(0)
        #     else:
        #         gapevP.append(gapevP[-1])
        # else:
        #     gapev.append(gn / tn)
        #     gapevP.append(gnp / tn)

# changeev = list(changeev)
# changeevT = []
# for hi in range(len(changeev)):
#     if hi > 0:
#         changeevT.append((changeev[hi] + changeev[hi - 1]) / 2)
#
# gapevT = [gapev[i] + gapevP[i] for i in range(len(gapev))]

# plt.hist(gaplist, bins=500, density=True, cumulative=True)
# plt.scatter(changelist, gaplist)
# I1, = plt.plot(changeevT, gapev, label='Positive')
# I2, = plt.plot(changeevT, gapevP, label='Negative')
# I3, = plt.plot(changeevT, gapevT, label='Total')

cumtS = sorted(cumt, key=cmp_to_key(myCMP))
cumtSc = [i[0] for i in cumtS]
cumtSv = [i[1] for i in cumtS]
cumtF = []
for i in range(len(cumtSc)):
    cumtF.append(sum(cumtSv[i:]) / len(cumtSv[i:]))

plt.plot(cumtSc, cumtF)
# plt.legend()
plt.tight_layout()
# plt.title('Total ' + str(len(gaplist)))
plt.grid()
plt.show()