from secedgar.filings import Filing, FilingType
from secedgar.utils import get_cik_map
import pandas as pd
import os


path = 'E:\stockdata3'
df = pd.DataFrame()
map = get_cik_map()
map2 = get_cik_map(key='title')

keys = list(map.keys())
values = list(map.values())
keys2 = list(map2.keys())
values2 = list(map2.values())
tv = values + values2
fullciks = list(sorted(list(set(tv))))
fulltitles = []
fulltickers = []
for vi in fullciks:
    if vi in values:
        tidx = values.index(vi)
        ticker = keys[tidx]
        fulltickers.append(ticker)
    else:
        fulltickers.append('')
    if vi in values2:
        tkidx = values2.index(vi)
        title = keys2[tkidx]
        fulltitles.append(title)
    else:
        fulltitles.append('')

df['Ticker'] = fulltickers
df['Title'] = fulltitles
df['CIK'] = fullciks
df.to_csv(path + os.sep + 'CIKs.csv', index=False)
pass
