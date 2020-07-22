import json
import os
import pandas as pd

path = 'E:\stockdata2'
jfile = 'symbols.json'
jdata = open(path + os.sep + jfile)
jdict = json.load(jdata)
pddata = pd.DataFrame()
for i in jdict:
    sdict = {}
    if i['type'] == 'N/A':
        sdict['symbol'] = i['symbol']
        sdict['name'] = i['name']
        sdict['IEX ID'] = i['iexId']
        pddata = pddata.append(sdict, ignore_index=True)
pd.DataFrame.to_csv(pddata, path + os.sep + 'symbols.csv', index=False)


