import pandas as pd
import math
import os


path = 'E:\\newdata\IV Data\Gold'
path2 = 'E:\\newdata\IV Data\Gold\cleaneddata'
buffpath = 'E:\\newdata\IV Data\Gold\\buff'

forexs = ['XAU_USD历史数据', '黄金期货历史数据']

for bi in forexs:
    data = pd.read_csv(path + os.sep + bi + '.csv')
    dt = data.dtypes

    if str(dt['收盘']) == 'object':
        c = list(data['收盘'])
        newc = []
        for i in c:
            if type(i) == type('str'):
                if ',' in i:
                    pi = i.replace(',', '')
                    newc.append(pi)
                else:
                    newc.append(i)
            else:
                newc.append(i)
        data['收盘'] = newc
        data.to_csv(buffpath + os.sep + bi + '.csv', index=False)
    else:
        data.to_csv(buffpath + os.sep + bi + '.csv', index=False)


for bi in forexs:
    data = pd.read_csv(buffpath + os.sep + bi + '.csv')
    dt = data.dtypes
    c = list(data['收盘'])
    delidxs = []
    for ci in range(len(c)):
        if isinstance(c[ci], float):
            if math.isnan(c[ci]):
                delidxs.append(ci)
        else:
            delidxs.append(ci)
    sdata = data.drop(index=delidxs).reset_index(drop=True)
    sdata.to_csv(buffpath + os.sep + bi + '.csv', index=False)

dates = []
for fi in forexs:
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['日期'])
    dates += fdate

totaldates = list(sorted(list(set(dates))))

deldates = []
for fi in forexs:
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['日期'])
    for di in totaldates:
        if di not in fdate:
            deldates.append(di)

adjdeldates = list(sorted(list(set(deldates))))

delnumsdict = {}
for fi in forexs:
    delnums = []
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['日期'])
    for adi in adjdeldates:
        if adi in fdate:
            idx = fdate.index(adi)
            delnums.append(idx)
    delnumsdict[fi] = delnums

for k, v in delnumsdict.items():
    fdata = pd.read_csv(buffpath + os.sep + k + '.csv')
    sdata = fdata.drop(index=v).reset_index(drop=True)
    sdata.to_csv(path2 + os.sep + k + '.csv', index=False)