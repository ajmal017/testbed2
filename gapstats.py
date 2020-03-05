import matplotlib.pyplot as plt
import pandas as pd
from myfuncs import cumcovert
import os


def gapstatfunc(symbol:str, statgaps='all'):
    path = r'E:\stockdata'
    ticker = pd.read_csv(path + os.sep + symbol + '.csv')
    c = list(ticker['Close'])
    o = list(ticker['Open'])
    h = list(ticker['High'])
    l = list(ticker['Low'])
    slen = len(c)
    gapdict = {}

    idx = list(range(slen))
    gaplist = []
    for i in idx:
        if i > 0:
            om = o[i]
            cm = c[i - 1]
            gap = (om - cm) / cm
            up = max(om, cm)
            dp = min(om, cm)
            subidx = idx[i:]
            subminp = 10000000000000000
            submaxp = -1
            days = None
            for si in subidx:
                if h[si] > submaxp:
                    submaxp = h[si]
                if l[si] < subminp:
                    subminp = l[si]
                if subminp < dp and submaxp > up:
                    days = si - i
                    break
            gaplist.append((gap, days))

    if statgaps == 'all':
        gapdict['all'] = []
        dayslist = []
        nno = 0
        for gi in gaplist:
            if gi[1] != None:
                dayslist.append(gi[1])
            else:
                nno += 1
        nnolist = [max(dayslist) + 10] * nno
        dayslist = dayslist + nnolist
        count = len(dayslist)
        hist, bins = cumcovert(dayslist, count)
        gapdict['all'] = (hist, bins)
    else:
        for si in range(len(statgaps)):
            if si == 0:
                dayslist = []
                nno = 0
                for gi in gaplist:
                    if gi[0] <= statgaps[si]:
                        if gi[1] != None:
                            dayslist.append(gi[1])
                        else:
                            nno += 1
                nnolist = [max(dayslist) + 10] * nno
                dayslist = dayslist + nnolist
                count = len(dayslist)
                hist, bins = cumcovert(dayslist, count)
                gapdict[('D', statgaps[si])] = (hist, bins)
            else:
                dayslist = []
                nno = 0
                for gi in gaplist:
                    if statgaps[si - 1] < gi[0] <= statgaps[si]:
                        if gi[1] != None:
                            dayslist.append(gi[1])
                        else:
                            nno += 1
                nnolist = [max(dayslist) + 10] * nno
                dayslist = dayslist + nnolist
                count = len(dayslist)
                hist, bins = cumcovert(dayslist, count)
                gapdict[(statgaps[si - 1], statgaps[si])] = (hist, bins)
        dayslist = []
        nno = 0
        for gi in gaplist:
            if gi[0] > statgaps[-1]:
                if gi[1] != None:
                    dayslist.append(gi[1])
                else:
                    nno += 1
        nnolist = [max(dayslist) + 10] * nno
        dayslist = dayslist + nnolist
        count = len(dayslist)
        hist, bins = cumcovert(dayslist, count)
        gapdict[(statgaps[-1], 'U')] = (hist, bins)

    return gapdict

# symbol = 'amzn'
# statgaps = [-0.1, -0.05, -0.02, 0.02, 0.05, 0.1]
# allgapdict = gapstatfunc(symbol, statgaps)
# lglist = []
# for ak, av in allgapdict.items():
#     ii = ''
#     lglist.append(ii)
#     lb = str(ak[0]) + '< StatGap <= ' + str(ak[1])
#     lglist[-1], = plt.plot(av[1], av[0], label=lb)
#
# plt.tight_layout()
# plt.legend()
# plt.grid()
# plt.title(symbol.upper())
# plt.show()

