import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os

filepath = r'D:\Yahoo Data\Futures'
alignedfilepath = r'D:\Yahoo Data\Futures\Aligned Data'
symbols = ['CL=F', 'HO=F', 'RB=F']
sretime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
stmppath = alignedfilepath + os.sep + '+'.join(symbols + [sretime])
if not os.path.exists(stmppath):
    os.mkdir(stmppath)


def yahoo_align_data():
    dfbuff = {}
    datebuff = {}
    dateall = []
    for si in symbols:
        fname = filepath + os.sep + si + '.csv'
        df = pd.read_csv(fname)
        c = df['Close'].values
        nannums = []
        n = 0
        for i in c:
            if np.isnan(i):
                nannums.append(n)
            n += 1
        df = df.drop(index=nannums).reset_index(drop=True)
        datebuff[si] = list(df['Date'])
        dateall += list(df['Date'])
        dfbuff[si] = df
    dateall = list(sorted(datebuff))
    for si in symbols:
        delnums = []
        for i in dateall:
            if i not in datebuff[si]:
                delnums.append(datebuff[si].index(i))
        df2 = dfbuff[si].drop(index=delnums).reset_index(drop=True)
        afname = stmppath + os.sep + si + '-a.csv'
        df2.to_csv(afname, index=False)


yahoo_align_data()
