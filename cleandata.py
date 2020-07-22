import pandas as pd
import json
import os


def dictsort(d: dict):
    nums = list(d.values())
    nums = list(set(nums))
    nums = sorted(nums)
    keys = []
    values = []
    for ni in nums:
        for k, v in d.items():
            if v == ni:
                keys.append(k)
                values.append(v)
    return keys, values


path = 'E:\stockdata2\stocksdata'
dpath ='E:\stockdata2'
fpath = 'E:\stockdata2\Datefile'
files = os.listdir(path)
# toldates = []
# n = 0
# for fi in files:
#     n += 1
#
#     print(n, '', fi)
#     ticker = pd.read_csv(fpath + os.sep + fi)
#     fdate = list(ticker['Date'])
#     for di in fdate:
#         if di not in toldates:
#             print(di)
#             toldates.append(di)
#
# toldates = sorted(toldates)
# fdata = {'Date': toldates}
# pdfdate = pd.DataFrame(fdata)
# pdfdate.to_csv(dpath + os.sep + 'FullDates.csv')
# pass

# fulldates = pd.read_csv(dpath + os.sep + 'FullDates.csv')
# fulldateslist = list(fulldates['Date'])
# fulldateslist = list(reversed(fulldateslist))
# fulldateslist.pop(408)
# fulldateslist.pop(860)
# fulldateslist.pop(893)
# fulldateslist.pop(1135)
# fulldateslist.pop(1943)
# fulldateslist.pop(2597)
# fulldateslist.pop(2722)
# fulldateslist.pop(4744)
# fulldateslist.pop(4744)
# filelendict = {}
# n = 0
# for fi in files:
#     n += 1
#     # print(n)
#     nlen = 0
#     ticker = pd.read_csv(path + os.sep + fi)
#     fdate = list(ticker['Date'])
#     fdate = list(reversed(fdate))
#     fnums = list(range(len(fdate)))
#     for fni in fnums:
#         if fdate[fni] == fulldateslist[fni]:
#             nlen += 1
#         else:
#             filelendict[fi] = nlen
#             print(n, ' ', fi, ':', nlen)
#             break
# jfilelen = open(dpath + os.sep + 'DataLenth.json', 'w')
# json.dump(filelendict, jfilelen)
# jfilelen.close()
# pass

jf = open(dpath + os.sep + 'DataLenth.json', 'r')
jdatalen = json.load(jf)
jsymbols = []
for jk, jv in jdatalen.items():
    if jv >= 2200:
        jsymbols.append(jk)

superdata = pd.DataFrame()
jn = 0
for sfi in jsymbols:
    symbol = sfi.split('.')[0]
    ticker = pd.read_csv(path + os.sep + sfi)
    ticker = ticker.tail(1100)
    line = list(ticker['Close'])
    superdata[symbol] = line
    jn += 1
    print(jn, '', symbol)

data_corr = superdata.corr()
data_corr.to_csv(dpath + os.sep + 'CorrMatrix.csv')
symbols = list(data_corr.columns)
sylenl = list(range(len(symbols)))[1:]
sylenv = sylenl
corrdict = {}
lnum = 0
for vi in sylenv:
    for li in range(sylenl[lnum]):
        pair = (symbols[vi], symbols[li])
        corrdict[pair] = data_corr.at[symbols[vi], symbols[li]]
    lnum += 1

# symbolscopy = symbols
# for i in range(len(symbols)):
#     for j in range(len(symbolscopy)):
#         if symbols[i] != symbolscopy[j]:
#             pair = (symbols[i], symbolscopy[j])
#             pair = sorted(pair)
#             if pair not in pairs:
#                 pairs.append(pair)
#
#
# for pi in pairs:
#     corrdict[pi] = data_corr.at[pi[0], pi[1]]

# sortedpairs, sortedvalues = dictsort(corrdict)
dfpairs = list(corrdict.keys())
dfvalues = list(corrdict.values())
corrdf = pd.DataFrame()
corrdf['Pair'] = dfpairs
corrdf['Values'] = dfvalues
corrdf.to_csv(dpath + os.sep + 'SortedPairs2.csv', index=False)