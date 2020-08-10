import pandas as pd
import os


path = r'E:\newdata\OCC data'
savepath = r'E:\newdata\OCC data\Adj Data'
month = '202006'
files = os.listdir(path + os.sep + month)
fdata = ''
finit = False
for fi in files:
    ff = path + os.sep + month + os.sep + fi
    if os.stat(ff).st_size != 0:
        fdf = pd.read_csv(ff, thousands=',')
        fdf = fdf[: -2]
        if not finit:
            fdata = fdf
            finit = True
            continue
        fnames = list(fdata['Options Class'])
        dfnames = list(fdf['Options Class'])
        for ui in range(len(dfnames)):
            if dfnames[ui] in fnames:
                idx = fnames.index(dfnames[ui])
                fdata.at[idx, 'Trade Volume'] += fdf.at[ui, 'Trade Volume']
                fdata.at[idx, 'YTD Volume'] += fdf.at[ui, 'YTD Volume']
            else:
                ps = fdf.iloc[ui]
                fdata = fdata.append(ps, ignore_index=True)

fdata.sort_values('YTD Volume', ascending=False, inplace=True)
savename = month + '-Full-Y.csv'
fdata.to_csv(savepath + os.sep + savename, index=False)