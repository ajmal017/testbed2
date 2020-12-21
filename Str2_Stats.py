import pandas as pd
import os

brickpath = r'D:\HIST Data\Bricks'
pairs = 'XAUUSD'
bp = 4
brickfile = brickpath + os.sep + pairs + '-bricks-{}ip.txt'.format(bp)

df = pd.read_csv(brickfile, header=None)
gn = df[3].values

dl = len(gn)
backnum = list(range(1, 11))
stats = {}

for bni in backnum:
    sels = 0
    tsels = 0
    for i in range(dl):
        if i > bni - 1:
            conP = True
            conN = True
            nums = list(range(1, bni + 1))
            for bi in nums:
                conP &= gn[i - bi] > 0
                conN &= gn[i - bi] < 0
            if conP or conN:
                tsels += 1
            conP &= gn[i] > 0
            conN &= gn[i] < 0
            if conP or conN:
                sels += 1
    rio = round(sels / tsels, 2)
    stats[bni] = [rio, (sels, tsels)]
pass