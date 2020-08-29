from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import functools
import json
import pandas as pd
import os
import copy
import math


def myfilenamesort(x, y):
    xb = int(x.split('.')[0].split('-')[-1])
    yb = int(y.split('.')[0].split('-')[-1])
    if xb < yb:
        return -1
    elif xb > yb:
        return 1
    else:
        return 0


def isoformat_to_date(sdate: str):
    bdate = sdate.split('-')
    return date(int(bdate[0]), int(bdate[1]), int(bdate[2]))


def split_coors_generator(x: int, y: int):
    filedict = {}
    n = 0
    for xi in range(x):
        if xi > 0:
            coors = []
            xlist = list(range(xi))
            xlist_r = list(reversed(xlist))
            for ni in range(xi):
                coor = (xlist_r[ni], xlist[ni])
                coors.append(coor)
            filedict[n] = coors
            n += 1

    xlist_R = list(reversed(list(range(x))))

    for yi in range(y - x):
        # if yi > 0:
        coors = []
        yn = 0
        for xi in xlist_R:
            coor = (xi, yi + yn)
            yn += 1
            coors.append(coor)
        filedict[n] = coors
        n += 1

    xlist_e = list(range(x))

    for i in xlist_e:
        # if i > 0:
        xlist_e_y = list(range(y - x + i, y))
        xlist_e_x = list(reversed(list(range(i, x))))
        coors = []
        for ii in range(len(xlist_e_x)):
            coor = (xlist_e_x[ii], xlist_e_y[ii])
            coors.append(coor)
        filedict[n] = coors
        n += 1

    return filedict


jpath = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data Json'
cpath = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data'
finalpath = r'E:\newdata\quandl data\CHRIS-CME_NG\final data'
if not os.path.exists(finalpath):
    os.mkdir(finalpath)

filelist = os.listdir(cpath)
filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort))

jfile = open(jpath + os.sep + 'Index.json', 'r')
splitnumsdict = json.load(jfile)
jfile.close()

monthsl = list(splitnumsdict.keys())
ddate_s = isoformat_to_date(monthsl[0] + '-9')
ddate_e = isoformat_to_date(monthsl[-1] + '-9')

missedidxs = []
godate = ddate_s
mi = 0
gi = 0

finalfilenames = []
while godate <= ddate_e:
    mdate = isoformat_to_date(monthsl[mi] + '-9')
    if godate == mdate:
        mi += 1
    else:
        missedidxs.append(gi)

    filename = str(godate.year) + '-' + str(godate.month)
    finalfilenames.append(filename)

    godate = godate + relativedelta(months=1)
    gi += 1

while godate <= ddate_e + relativedelta(months=len(filelist) - 1):
    filename = str(godate.year) + '-' + str(godate.month)
    finalfilenames.append(filename)
    godate = godate + relativedelta(months=1)


superdata = []
getcol = True
col = []
for fi in filelist:
    data = pd.read_csv(cpath + os.sep + fi)
    if getcol:
        col = data.columns.values.tolist()
        getcol = False
    subdata = []
    for v in splitnumsdict.values():
        subsubdata = data[v[0]: v[-1] + 1]
        subdata.append(copy.copy(subsubdata))
    superdata.append(copy.copy(subdata))

su = []
for sui in superdata:
    su.append(len(sui))
print(su)

insertdf = pd.DataFrame([[float('nan')] * len(col)], columns=col)


for si in range(len(superdata)):
    for ii in missedidxs:
        superdata[si].insert(ii, insertdf)

su = []
for sui in superdata:
    su.append(len(sui))
print(su)

coorsdict = split_coors_generator(len(superdata), gi)

for k, v in coorsdict.items():
    sn = 0
    con = ''
    for ci in v:
        if sn == 0:
            print(ci, '-----')
            con = superdata[ci[0]][ci[1]]
            sn += 1
        else:
            print(ci)
            con = copy.deepcopy(con.append(copy.deepcopy(superdata[ci[0]][ci[1]])))

    con = con.reset_index(drop=True)
    checknan = list(con['Last'])
    dropidxs = []

    for ki in range(len(checknan)):
        if math.isnan(checknan[ki]):
            dropidxs.append(ki)

    con = con.drop(index=dropidxs).reset_index(drop=True)
    con.to_csv(finalpath + os.sep + finalfilenames[k] + '.csv', index=False)
