import pandas as pd
import math
import os

# path = 'E:\\newdata'
path = 'E:\\newdata\Oils'
# path2 = 'E:\\newdata\cleaneddataFX'
path2 = 'E:\\newdata\Oils\Cleaneddata'
buffpath = 'E:\\newdata\Oils\\buff'
# forexs = ['DX-Y.NYB', 'EURUSD=X', 'GBPUSD=X', 'JPYUSD=X', 'CHFUSD=X', 'CADUSD=X', 'AUDUSD=X', 'NZDUSD=X', 'UUP', 'FXA', 'FXB', 'FXC', 'FXE', 'FXF', 'FXY'] #  'CADUSD', 'AUDUSD', 'NZDUSD',, 'GLD', 'SLV', 'BTCUSD=X', 'CNYUSD=X'
# forexs = ['DX-Y.NYB', 'FXA', 'FXB', 'FXC', 'FXE', 'FXF', 'FXY', 'UUP', 'UDN', 'USDU']
# forexs = ['DX-Y.NYB', 'DX=F']
forexs = ['CL=F', 'QM=F', 'SCO', 'USO', 'UCO', 'USL']

for bi in forexs:
    data = pd.read_csv(path + os.sep + bi + '.csv')
    c = list(data['Close'])
    delidxs = []
    for ci in range(len(c)):
        if math.isnan(c[ci]):
            delidxs.append(ci)
    sdata = data.drop(index=delidxs).reset_index(drop=True)
    sdata.to_csv(buffpath + os.sep + bi + '.csv', index=False)

dates = []
for fi in forexs:
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['Date'])
    dates += fdate

totaldates = list(sorted(list(set(dates))))

deldates = []
for fi in forexs:
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['Date'])
    for di in totaldates:
        if di not in fdate:
            deldates.append(di)

adjdeldates = list(sorted(list(set(deldates))))

delnumsdict = {}
for fi in forexs:
    delnums = []
    fdate = list(pd.read_csv(buffpath + os.sep + fi + '.csv')['Date'])
    for adi in adjdeldates:
        if adi in fdate:
            idx = fdate.index(adi)
            delnums.append(idx)
    delnumsdict[fi] = delnums

for k, v in delnumsdict.items():
    fdata = pd.read_csv(buffpath + os.sep + k + '.csv')
    sdata = fdata.drop(index=v).reset_index(drop=True)
    sdata.to_csv(path2 + os.sep + k + '.csv', index=False)
