import matplotlib.pyplot as plt
import pandas as pd
import os

sapfile = r'D:\Other Data\IVE_tickbidask_cleared.csv'
df = pd.read_csv(sapfile)
date = list(df['Date'])
time = list(df['Time'])
price = list(df['Price'])
size = list(df['Size'])

stdopen = 0
stdcloseP = 0
stdcloseN = 0
open = 0
close = 0
high = 0
low = 0
vol = 0
opendate = 0
opentime = 0
closedate = 0
closetime = 0

PorD = False
percent = 0.01
dot = 0.3
gap = 0

superdata = []
newbar = False
dl = len(date)
for i in range(dl):
    if i == 0:
        stdopen = price[0]
        open = price[0]
        high = price[0]
        low = price[0]
        opendate = date[0]
        opentime = time[0]
        if PorD:
            stdcloseP = stdopen * (1 + percent)
            stdcloseN = stdopen * (1 - percent)
            gap = stdopen * (1 + percent)
        else:
            stdcloseP = stdopen + dot
            stdcloseN = stdopen - dot
            gap = dot
    else:
        if newbar:
            open = price[i]
            high = price[i]
            low = price[i]
            opendate = date[i]
            opentime = time[i]
            newbar = False

    if stdcloseN < price[i] < stdcloseP:
        if high < price[i]:
            high = price[i]
        if low > price[i]:
            low = price[i]
        vol += size[i]

    elif price[i] >= stdcloseP:
        close = price[i]
        vol += size[i]
        closedate = date[i]
        closetime = time[i]

        pn = 1
        while price[i] >= stdcloseP + gap * pn:
            pn += 1

        adjstdcloseP = stdcloseP + gap * (pn - 1)
        subdata = [opendate, opentime, closedate, closetime, stdopen, open, stdcloseP, adjstdcloseP, close, high, low, vol, pn - 1]
        superdata.append(subdata)

        stdopen = adjstdcloseP
        newbar = True
        vol = 0
        if PorD:
            stdcloseP = stdopen * (1 + percent)
            stdcloseN = stdopen * (1 - percent)
            gap = stdopen * (1 + percent)
        else:
            stdcloseP = stdopen + dot
            stdcloseN = stdopen - dot
            gap = dot

    elif price[i] <= stdcloseN:
        close = price[i]
        vol += size[i]
        closedate = date[i]
        closetime = time[i]

        pn = 1
        while price[i] <= stdcloseN - gap * pn:
            pn += 1

        adjstdcloseN = stdcloseN - gap * (pn - 1)
        subdata = [opendate, opentime, closedate, closetime, stdopen, open, stdcloseN, adjstdcloseN, close, high, low, vol, pn - 1]
        superdata.append(subdata)

        stdopen = adjstdcloseN
        newbar = True
        vol = 0
        if PorD:
            stdcloseP = stdopen * (1 + percent)
            stdcloseN = stdopen * (1 - percent)
            gap = stdopen * (1 + percent)
        else:
            stdcloseP = stdopen + dot
            stdcloseN = stdopen - dot
            gap = dot

columns = ['Open Date', 'Open Time', 'Close Date', 'Close Time', 'Std Open', 'Open', 'Std Close', 'Adj Std Close', 'Close', 'High', 'Low', 'Vol', 'Gap Num']
brickdf = pd.DataFrame(data=superdata, columns=columns)
brickfile = r'D:\Other Data\IVE_tickbidask_bricks.csv'
brickdf.to_csv(brickfile, index=False)

c = brickdf['Close']
stdo = brickdf['Std Open']
gn = brickdf['Gap Num']
dl2 = len(c)
previousF = None
dropinxs = []
for i in range(dl2):
    forth = True
    if stdo[i] > c[i]:
        forth = False
    if i > 0:
        if previousF != forth and gn[i] == 0:
            dropinxs.append(i)
    previousF = forth
simpdf = brickdf.drop(dropinxs).reset_index(drop=True)
simpfile = r'D:\Other Data\IVE_tickbidask_bricks_simp.csv'
simpdf.to_csv(simpfile, index=False)
