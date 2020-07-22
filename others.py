import pandas as pd
import json
import os

path = 'E:\stockdata2\stocksdata'
dpath ='E:\stockdata2'
fpath = 'E:\stockdata2\others'
files = os.listdir(fpath)
toldates = list(pd.read_csv(dpath + os.sep + 'FullDates.csv')['Date'])
for fi in files:
    ticker = pd.read_csv(fpath + os.sep + fi)
    fdate = list(ticker['Date'])
    for di in fdate:
        if di not in toldates:
            print(di)
            toldates.append(di)

toldates = sorted(toldates)
fdata = {'Date': toldates}
pdfdate = pd.DataFrame(fdata)
pdfdate.to_csv(dpath + os.sep + 'FullDates.csv')
pass