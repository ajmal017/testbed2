from datetime import date, timedelta
from workalendar.usa.core import UnitedStates
from dateutil.relativedelta import relativedelta
import functools
import json
import pandas as pd
import copy
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


def isoformat_to_date(sdate: str):
    bdate = sdate.split('-')
    return date(int(bdate[0]), int(bdate[1]), int(bdate[2]))


def monthdays(month: str):
    m = month.split('-')
    cm = date(int(m[0]), int(m[1]), 1)
    nm = cm + relativedelta(months=1)
    dayslist = []
    while cm < nm:
        dayslist.append(cm)
        cm = cm + timedelta(days=1)
    return dayslist


def termday_generator_NG(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = monthdays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-3]


def termdays_generator(start: date, end: date):
    holidays = []
    fyears = [yi for yi in range(start.year, end.year + 1)]
    US = UnitedStates()
    for fyi in fyears:
        cal = US.holidays(fyi)
        for ci in cal:
            lstr = ci[1].split(' ')[-1]
            if lstr != '(Observed)':
                holidays.append(ci[0])

    termdays = []

    adjstart = date(start.year, start.month, 1)
    adjend = date(end.year, end.month, 1)
    godate = adjstart
    while godate <= adjend:
        mstr = str(godate.year) + '-' + str(godate.month)
        mondays = monthdays(mstr)
        adjmdays = []
        for mi in mondays:
            if mi.weekday() != 5 and mi.weekday() != 6:
                if mi not in holidays:
                    adjmdays.append(mi)
        termd = adjmdays[-3]
        termdays.append(termd)
        godate = godate + relativedelta(months=1)

    return termdays


fpath = r'E:\newdata\quandl data\CHRIS-CME_NG'
spath = r'E:\newdata\quandl data\CHRIS-CME_NG\Singular Contracts'
if not os.path.exists(spath):
    os.mkdir(spath)
filelist = []
for roots, dirs, files in os.walk(fpath):
   if roots == fpath:
       filelist = files

fulldate_list = []
for fi in filelist:
    fdate = list(pd.read_csv(fpath + os.sep + fi)['Date'])
    fulldate_list += fdate

fulldate_list = list(sorted(list(set(fulldate_list))))

fulldate_dict = {}
n = 0
for fli in fulldate_list:
    fulldate_dict[fli] = n
    n += 1

filelist = sorted(filelist, key=functools.cmp_to_key(myfilenamesort))
superdata = {}
fn = 1
for fi2 in filelist:
    data2 = pd.read_csv(fpath + os.sep + fi2)
    data2 = data2.iloc[::-1].reset_index(drop=True)
    date2 = list(data2['Date'])
    Nos = [fulldate_dict[i] for i in date2]
    data2['Date No.'] = Nos
    data2['From File'] = [fn] * len(Nos)

    start = isoformat_to_date(date2[0])
    end = isoformat_to_date(date2[-1])
    termdays = termdays_generator(start, end)

    if termdays[-1] > end:
        termdays.pop(-1)
    if termdays[0] < start:
        termdays.pop(0)
    splitnums = [-1]

    tin = 0
    for ti in termdays:
        tis = ti.isoformat()
        print('\n----', tin, tis)
        if tis in date2:
            idx = date2.index(tis)
            splitnums.append(idx)
            print('*', tis, idx)
        else:
            date2_c = copy.deepcopy(date2)
            date2_c.append(tis)
            date2_c = list(sorted(date2_c))
            idx2 = date2_c.index(tis)
            if idx2 - 1 != splitnums[-1]:
                print(tis, idx2 - 1)
                splitnums.append(idx2 - 1)
        tin += 1

    splitnums.append(len(date2) - 1)

    for si in range(len(splitnums)):
        if si > 0:
            sn = splitnums[si - 1] + 1
            en = splitnums[si] + 1
            pdata = data2[sn: en]
            pdatel = isoformat_to_date(list(pdata['Date'])[-1])
            pdatel_c = date(pdatel.year, pdatel.month, 1) + relativedelta(months=fn)
            strmonth = str(pdatel_c.year) + '-' + str(pdatel_c.month)
            if strmonth not in superdata.keys():
                superdata[strmonth] = {}
            superdata[strmonth][fn] = pdata

    fn += 1

for k, v in superdata.items():
    connums = list(sorted(list(v.keys()), reverse=True))
    init = False
    combodata = ''
    for coi in connums:
        if not init:
            combodata = v[coi]
            init = True
        else:
            combodata = combodata.append(v[coi])
    combodata = combodata.reset_index(drop=True)
    print(k)
    combodata.to_csv(spath + os.sep + k + '.csv', index=False)
























