import pandas as pd
from myfuncs import cumcovert
import os


def gapM2func(symbol:str, statgaps='all', gapnum=30):
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
            subidx = idx[i: i + gapnum]
            subminp = 10000000000000000
            submaxp = -1
            for si in subidx:
                if h[si] > submaxp:
                    submaxp = h[si]
                if l[si] < subminp:
                    subminp = l[si]

            M2 = ((subminp - cm) / cm, (submaxp - cm) / cm)
            gaplist.append((gap, M2))

    if statgaps == 'all':
        minv = [i[1][0] - i[0] for i in gaplist]
        maxv = [i[1][1] - i[0] for i in gaplist]
        count = len(minv)
        minhist, minbins = cumcovert(minv, count)
        maxhist, maxbins = cumcovert(maxv, count)
        gapdict['all'] = ((minhist, minbins), (maxhist, maxbins))
    else:
        for si in range(len(statgaps)):
            if si == 0:
                subgaplist = []
                for gi in gaplist:
                    if gi[0] <= statgaps[si]:
                        subgaplist.append(gi)
                minv = [i[1][0] - i[0] for i in subgaplist]
                maxv = [i[1][1] - i[0] for i in subgaplist]
                count = len(minv)
                minhist, minbins = cumcovert(minv, count)
                maxhist, maxbins = cumcovert(maxv, count)
                gapdict[('D', statgaps[si])] = ((minhist, minbins), (maxhist, maxbins))
            else:
                subgaplist = []
                for gi in gaplist:
                    if statgaps[si - 1] < gi[0] <= statgaps[si]:
                        subgaplist.append(gi)
                minv = [i[1][0] - i[0] for i in subgaplist]
                maxv = [i[1][1] - i[0] for i in subgaplist]
                count = len(minv)
                minhist, minbins = cumcovert(minv, count)
                maxhist, maxbins = cumcovert(maxv, count)
            gapdict[(statgaps[si - 1], statgaps[si])] = ((minhist, minbins), (maxhist, maxbins))
        subgaplist = []
        for gi in gaplist:
            if gi[0] > statgaps[-1]:
                subgaplist.append(gi)
        minv = [i[1][0] - i[0] for i in subgaplist]
        maxv = [i[1][1] - i[0] for i in subgaplist]
        count = len(minv)
        minhist, minbins = cumcovert(minv, count)
        maxhist, maxbins = cumcovert(maxv, count)
        gapdict[(statgaps[-1], 'U')] = ((minhist, minbins), (maxhist, maxbins))

    return gapdict