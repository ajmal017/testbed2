import matplotlib.pyplot as plt
import pandas as pd
import os

brickpath = r'D:\HIST Data\Bricks'
pairs = 'XAUUSD'
bp = 2
brickfile = brickpath + os.sep + pairs + '-bricks-{}ip.txt'.format(bp)

df = pd.read_csv(brickfile, header=None)
gn = df[3].values

dl = len(gn)
bricllen = []
bl = 0
bf = None
cf = None
for i in range(dl):
    if gn[i] < 0:
        cf = False
    else:
        cf = True

    if i == 0:
        bf = cf
        bl = gn[0]
    else:
        if bf == cf:
            bl += gn[i]
        else:
            bricllen.append(bl)
            bl = gn[i]
            bf = cf
    if i == (dl - 1):
        bricllen.append(bl)

maxl = max(bricllen)
minl = min(bricllen)
bn = maxl - minl
if bn > 100:
    bn = 100
plt.hist(bricllen, bins=bn, density=False, cumulative=False, rwidth=0.9)
plt.tight_layout()
plt.grid()
plt.show()
