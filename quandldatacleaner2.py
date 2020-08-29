from datetime import date, timedelta
import functools
import pandas as pd
import math
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

path = r'E:\newdata\quandl data\CHRIS-CME_NG'
cddir = 'cleaned data'
buff = 'buff'
cdpath = path + os.sep + cddir
buffpath = path + os.sep + buff
if not os.path.exists(cdpath):
    os.mkdir(cdpath)
cdfiles = os.listdir(cdpath)
for ci in cdfiles:
    os.remove(cdpath + os.sep + ci)

if not os.path.exists(buffpath):
    os.mkdir(buffpath)
bufffiles = os.listdir(buffpath)
for bi in bufffiles:
    os.remove(buffpath + os.sep + bi)

fnum = 24
filelist = []
for roots, dirs, files in os.walk(path):
   if roots == path:
       filelist = files

filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort))[:fnum]

for fi in filelist:
    data = pd.read_csv(path + os.sep + fi)
    c = list(data['Last'])
    d = list(data['Date'])
    dropnums = []
    for i in range(len(c)):
        wday = date.fromisoformat(d[i])
        if math.isnan(c[i]):
            dropnums.append(i)
        elif wday.weekday() == 5 or wday.weekday() == 6:
            dropnums.append(i)
    bdata = data.drop(index=dropnums).reset_index(drop=True)
    bdata = bdata.iloc[::-1].reset_index(drop=True)
    bdata.to_csv(buffpath + os.sep + fi, index=False)

bufffilelist = os.listdir(buffpath)

fulldates = []
for fi in bufffilelist:
    ddate = list(pd.read_csv(buffpath + os.sep + fi)['Date'])
    fulldates += ddate

fulldates = list(sorted(list(set(fulldates))))

sdate = date.fromisoformat(fulldates[0])
edate = date.fromisoformat(fulldates[-1])

fulldatesnumdict = {}
initdate = sdate

n = 0
while initdate <= edate:
    strdate = initdate.isoformat()
    fulldatesnumdict[strdate] = n
    initdate = initdate + timedelta(days=1)
    n += 1

deldatelist = []
for fi in bufffilelist:
    ddate = list(pd.read_csv(buffpath + os.sep + fi)['Date'])
    for di in fulldates:
        if di not in ddate:
            deldatelist.append(di)
deldatelist = list(sorted(list(set(deldatelist))))

getnums = True
datenums = []
for fi in bufffilelist:
    data = pd.read_csv(buffpath + os.sep + fi)
    ddate = list(data['Date'])
    delnums = []
    for i in deldatelist:
        if i in ddate:
            idx = ddate.index(i)
            delnums.append(idx)
    sdata = data.drop(index=delnums).reset_index(drop=True)
    if getnums:
        numsdate = list(sdata['Date'])
        datenums = [fulldatesnumdict[i] for i in numsdate]
        getnums = False
    sdata['Date NO.'] = datenums
    sdata.to_csv(cdpath + os.sep + 'Adj-' + fi, index=False)