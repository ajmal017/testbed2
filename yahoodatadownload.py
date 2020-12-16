import yfinance as yf
import pandas as pd
import os

path = 'D:\Yahoo Data\Stocks'
symbolscsv = 'D:\IEX Data\symbols.csv'
symbols = list(pd.read_csv(symbolscsv)['symbol'])
tn = len(symbols)
n = 0
for si in symbols:
    try:
        tiker = yf.Ticker(si)
        n += 1
        lrio = n / tn
        lriot = round(lrio * 100, 2)
        hist = tiker.history(period='max')

        hist.to_csv(path + os.sep + si + '.csv')
        print(si + '下载完成！ 总进度：' + str(lriot) + '%')
    except Exception:
        print(si + '下载异常！')
        continue


pass
