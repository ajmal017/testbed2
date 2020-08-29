from datetime import date
import functools
import json
import pandas as pd
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


spath = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data Json'
if not os.path.exists(spath):
    os.mkdir(spath)
rpath = r'E:\newdata\quandl data\CHRIS-CME_NG\cleaned data'
filelist = os.listdir(rpath)
filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort))

datas = pd.read_csv(rpath + os.sep + filelist[0])
dates = list(datas['Date'])
NO = list(datas['Date NO.'])

sdatanums = []
month = []
initddate = date.fromisoformat(dates[0])
k = str(initddate.year) + '-' + str(initddate.month)
datasplitnumdict = {}

dn = 0
for di in dates:
    ddate = date.fromisoformat(di)
    if initddate.year == ddate.year and initddate.month == ddate.month:
        month.append(dn)
    else:
        datasplitnumdict[k] = month
        initddate = date.fromisoformat(di)
        month = [dn]
        k = str(initddate.year) + '-' + str(initddate.month)
    if di == dates[-1]:
        datasplitnumdict[k] = month
    dn += 1

datasplitnumdict_date = {}
datasplitnumdict_NO = {}
for k, v in datasplitnumdict.items():
    datasplitnumdict_date[k] = [dates[i] for i in v]
    datasplitnumdict_NO[k] = [NO[i] for i in v]

datasplitnumdict_Last = {}
fn = 1
for fi in filelist:
    data = pd.read_csv(rpath + os.sep + fi)
    last = list(data['Last'])
    jtmonth = {}
    for k, v in datasplitnumdict.items():
        jtmonth[k] = [last[i] for i in v]
    datasplitnumdict_Last[fn] = jtmonth
    fn += 1

fidx = open(spath + os.sep + 'Index.json', 'w')
json.dump(datasplitnumdict, fidx)
fidx.close()

fno = open(spath + os.sep + 'Date_NO.json', 'w')
json.dump(datasplitnumdict_NO, fno)
fno.close()

fdate = open(spath + os.sep + 'Date.json', 'w')
json.dump(datasplitnumdict_date, fdate)
fdate.close()

flast = open(spath + os.sep + 'Close.json', 'w')
json.dump(datasplitnumdict_Last, flast)
flast.close()