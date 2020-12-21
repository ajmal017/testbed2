import yfinance as yf
import pandas as pd
import os

hpath = 'E:\Yahoo data\Hist Price'
spath = 'E:\Yahoo data\Earnings 2'
symbols = os.listdir(spath)

tn = len(symbols)
n = 0
for si in symbols:
    syi = si.split('.')[0]

    n += 1
    lrio = n / tn
    lriot = round(lrio * 100, 2)
    try:
        tiker = yf.Ticker(syi)
        hist = tiker.history(period='max')
        hname = hpath + os.sep + syi + '.csv'
        hist.to_csv(hname)
        print('保存', hname)
    except Exception:
        print(syi + '下载异常！')
        continue

    print('总进度：' + str(lriot) + '%')