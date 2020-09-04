import urllib.request as request
from datetime import date, timedelta
from workalendar.usa.core import UnitedStates
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import functools
import math
import copy
import os


def Quandl_Treasury_Constant_Maturity_Rate_Downloader(maturity='all', savepath=r'E:\newdata\quandl data\Maturity Rate'):
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    maturitydict = {'1M': 'DGS1MO',
                    '2M': 'DGS2MO',
                    '3M': 'DGS3MO',
                    '6M': 'DGS6MO',
                    '1Y': 'DGS1',
                    '2Y': 'DGS2',
                    '3Y': 'DGS3',
                    '5Y': 'DGS5',
                    '7Y': 'DGS7',
                    '10Y': 'DGS10',
                    '20Y': 'DGS20',
                    '30Y': 'DGS30'}
    url1 = 'https://www.quandl.com/api/v3/datasets/FRED/'
    url3 = '.csv?api_key=fjZyjRt-6y5WRapHGiAY'
    if maturity == 'all':
        for k, v in maturitydict.items():
            url = url1 + v + url3
            savename = k + '.csv'
            savefile = savepath + os.sep + savename
            try:
                req = request.Request(url)
                res = request.urlopen(req)
                file = res.read()
                f = open(savefile, 'wb')
                f.write(file)
                f.close()
                print(savename, '下载完成！')
            except:
                print(savename, '下载失败！')
                continue
        print('下载完成！')
    else:
        url2 = maturitydict[maturity.upper()]
        url = url1 + url2 + url3
        savename = maturity.upper() + '.csv'
        savefile = savepath + os.sep + savename
        try:
            req = request.Request(url)
            res = request.urlopen(req)
            file = res.read()
            f = open(savefile, 'wb')
            f.write(file)
            f.close()
            print(savename, '下载完成！')
        except:
            print(savename, '下载失败！')


def Chris_Futures_Downloader(symbolnum: int, path=r'E:\newdata\quandl data'):
    # path = r'E:\newdata\quandl data'
    url1 = 'https://www.quandl.com/api/v3/datasets/'
    url3 = '?api_key=fjZyjRt-6y5WRapHGiAY'

    contractfile = r'E:\newdata\quandl data\continuous.csv'
    condf = pd.read_csv(contractfile)
    code = condf['Quandl Code'][symbolnum]
    num = condf['Number of Contracts'][symbolnum] * 2

    numlist = list(range(num + 1))
    numlist = numlist[1:]

    cs = code.split('/')
    subdir = cs[0] + '-' + cs[1]

    savepath = path + os.sep + subdir
    # adjpath = savepath + os.sep + 'AdjData'
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    #     os.mkdir(adjpath)

    for ni in numlist:
        url2 = code + str(ni) + '.csv'
        url = url1 + url2 + url3

        # us = url2.split('/')
        filename = subdir + '-' + str(ni) + '.csv'

        savename = savepath + os.sep + filename
        filelist = os.listdir(savepath)
        if filename not in filelist:
            try:
                req = request.Request(url)
                res = request.urlopen(req)
                file = res.read()
                f = open(savename, 'wb')
                f.write(file)
                f.close()
                print(ni, filename, '下载完成！')
            except:
                print(ni, filename, '下载失败！')
                continue

    print(subdir, '下载完成！')


def isoformat_to_date(sdate: str):
    bdate = ''
    if '-' in sdate:
        bdate = sdate.split('-')
    elif '/' in sdate:
        bdate = sdate.split('/')
    else:
        print('日期解析错误！')

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


def myFilenameSort_Month(x, y):
    xstr = x.split('.')[0].split('-')
    xdate = date(int(xstr[0]), int(xstr[1]), 1)

    ystr = y.split('.')[0].split('-')
    ydate = date(int(ystr[0]), int(ystr[1]), 1)

    if xdate < ydate:
        return -1
    elif xdate > ydate:
        return 1
    else:
        return 0


def QuandlDfCleaner(dflist: list, dfreverse=False):
    cdflist = []
    for dfi in dflist:
        if dfreverse:
            cdf1 = dfi.iloc[::-1].reset_index(drop=True)
        else:
            cdf1 = dfi
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
        redflist.append(cdf)

    return redflist


def myDirScan_OnlyFile(path: str):
    filelist = []
    for roots, dirs, files in os.walk(path):
        if roots == path:
            filelist = files

    return filelist


def rangeTermDays_Generator(start: date, end: date, termfunc):
    termdays = []

    adjstart = date(start.year, start.month, 1)
    adjend = date(end.year, end.month, 1)
    godate = adjstart
    while godate <= adjend:
        termd = termfunc(godate)
        termdays.append(termd)
        godate = godate + relativedelta(months=1)

    return termdays


def df_to_3d_data(df: pd.DataFrame):
    shape = df.shape
    x = list(range(shape[0]))
    y = list(range(shape[1]))
    X = np.array([x for i in range(shape[1])])
    Y = np.rot90(np.array([y for i in range(shape[0])]), -1)
    Z = np.array(df.values).T

    return X, Y, Z


def myfilenamesort(x, y):
    xb = int(x.split('.')[0].split('-')[-1])
    yb = int(y.split('.')[0].split('-')[-1])
    if xb < yb:
        return -1
    elif xb > yb:
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


def Continueous_to_Singal(fpath: str, singaltermdaysfunc):
    # fpath = r'E:\newdata\quandl data\CHRIS-CME_NG'
    spath = fpath + os.sep + 'Singular Contracts'
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
        termdays = rangeTermDays_Generator(start, end, singaltermdaysfunc)

        if termdays[-1] >= end:
            termdays.pop(-1)
        if termdays[0] <= start:
            termdays.pop(0)
        splitnums = [-1]

        tin = 0
        for ti in termdays:
            tis = ti.isoformat()
            # print('\n----', tin, tis)
            if tis in date2:
                idx = date2.index(tis)
                splitnums.append(idx)
                # print('*', tis, idx)
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
        combodata = dfDeleteRepRow(combodata, 'Date')
        combodata.to_csv(spath + os.sep + k + '.csv', index=False)


#----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------


def FullMonthDays(month: str):
    m = month.split('-')
    cm = date(int(m[0]), int(m[1]), 1)
    nm = cm + relativedelta(months=1)
    dayslist = []
    while cm < nm:
        dayslist.append(cm)
        cm = cm + timedelta(days=1)
    return dayslist


def SingalTermday_generator_NG(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-3]



def SingalTermday_generator_GC(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-3]


def SingalTermday_generator_CL(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    mondays = mondays[: 25]
    _25thday = mondays[-1]
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)
    if _25thday in adjmdays:
        return adjmdays[-4]
    else:
        return adjmdays[-5]


def SingalTermday_generator_SI(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-3]


def SingalTermday_generator_HG(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-3]


def SingalTermday_generator_HO(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-1]


def SingalTermday_generator_ICE_B(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)
    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    return adjmdays[-1]


def SingalTermday_generator_GE(tdate: date):
    holidays = []
    US = UnitedStates()
    cal = US.holidays(tdate.year)
    for ci in cal:
        lstr = ci[1].split(' ')[-1]
        if lstr != '(Observed)':
            holidays.append(ci[0])

    mstr = str(tdate.year) + '-' + str(tdate.month)
    mondays = FullMonthDays(mstr)

    n = 0
    wn = 0
    for wi in mondays:
        if wi.weekday() == 2:
            n += 1
            if n == 2:
                break
        wn += 1
    mondays = mondays[: wn + 1]
    _3rdWednesday = mondays[-1]

    adjmdays = []
    for mi in mondays:
        if mi.weekday() != 5 and mi.weekday() != 6:
            if mi not in holidays:
                adjmdays.append(mi)

    if _3rdWednesday in adjmdays:
        return adjmdays[-3]
    else:
        return adjmdays[-2]