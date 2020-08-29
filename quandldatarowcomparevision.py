import matplotlib.pyplot as plt
from datetime import date, timedelta
import functools
import math
import json
import numpy as np
import pandas as pd
from Quandl_Utils import myFilenameSort_Month
from dateutil.relativedelta import relativedelta
import functools
from collections import Counter
import copy
import os


def isoformat_to_date(sdate: str):
    bdate = sdate.split('-')
    return date(int(bdate[0]), int(bdate[1]), int(bdate[2]))


def myStrDateSort(x, y):
    dx = isoformat_to_date(x)
    dy = isoformat_to_date(y)
    if dx < dy:
        return -1
    elif dx > dy:
        return 1
    else:
        return 0


def dfDeleteRepRow(df: pd.DataFrame, column: str):
    col = list(df[column])
    delnums = []
    nums = []
    n = 0
    for i in col:
        if i not in nums:
            nums.append(i)
        else:
            delnums.append(n)
        n += 1
    rdf = df.drop(index=delnums).reset_index(drop=True)
    return rdf


def QuandlDfCleaner(dflist: list):
    cdflist = []
    for dfi in dflist:
        rdfp = dfDeleteRepRow(dfi, 'Date')
        cdf1 = rdfp.iloc[::-1].reset_index(drop=True)
        last = cdf1['Last']
        n = 0
        c1delnums = []
        for li in last:
            if li == 0 or math.isnan(li):
                c1delnums.append(n)
            n += 1
        cdf2 = cdf1.drop(index=c1delnums).reset_index(drop=True)
        cdflist.append(cdf2)

    redflist = []
    fulldate = []
    for dfi1 in cdflist:
        date1 = list(dfi1['Date'])
        fulldate += date1
    fulldate = list(sorted(list(set(fulldate)), key=functools.cmp_to_key(myStrDateSort)))

    deldate = []
    for dfi2 in cdflist:
        date2 = list(dfi2['Date'])
        for ddi2 in fulldate:
            if ddi2 not in date2:
                deldate.append(ddi2)

    for dfi3 in cdflist:
        date3 = list(dfi3['Date'])
        sdelnums = []
        for ddi3 in deldate:
            if ddi3 in date3:
                idx = date3.index(ddi3)
                sdelnums.append(idx)

        cdf = dfi3.drop(index=sdelnums).reset_index(drop=True)
        redflist.append(copy.deepcopy(cdf))


    if redflist[0].shape != redflist[1].shape:
        while True:
            print('-------------')

    return copy.deepcopy(redflist)


fpath = r'E:\newdata\quandl data\CHRIS-CME_ED\Singular Contracts'

file_list = []
for roots, dirs, files in os.walk(fpath):
    if roots == fpath:
        file_list = files

basemonth = 12
monthdiff = 3
mnrio = 0.05
file_list = sorted(file_list, key=functools.cmp_to_key(myFilenameSort_Month))

monthpairdict = {}
for i in file_list:
    sm = i.split('.')[0]
    lm = sm.split('-')
    year = int(lm[0])
    month = int(lm[1])
    if month == basemonth:
        greatmonth = date(year, month, 1) + relativedelta(months=monthdiff)
        greatmonthstr = str(greatmonth.year) + '-' + str(greatmonth.month) + '.csv'
        if greatmonthstr in file_list:
            monthpairdict[sm] = [i, greatmonthstr]

yticks = []
ylabels = []
mn = 0

for k, v in monthpairdict.items():
    lf = pd.read_csv(fpath + os.sep + v[0])
    gf = pd.read_csv(fpath + os.sep + v[1])
    rdfs = QuandlDfCleaner([lf, gf])
    lc = list(rdfs[0]['Last'])
    gc = list(rdfs[1]['Last'])
    diff = [gc[i] / lc[i] + (mn * mnrio) for i in range(len(lc))]
    yticks.append(mn * mnrio + 1)
    ylabels.append(k)
    mn += 1
    plt.plot(diff)

plt.yticks(yticks, ylabels)
plt.tight_layout()
plt.grid()
plt.show()

