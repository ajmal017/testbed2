import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import pandas as pd
import os

brickpath = r'D:\HIST Data\Bricks'
truefxpath = r'D:\TrueFX Data\Bricks Data'
pairs = 'EURUSD'
bp = 10
brickfile = truefxpath + os.sep + pairs + '-bricks-{}bp.txt'.format(bp)

df = pd.read_csv(brickfile, header=None)
o = df[0]
ro = df[1]
c = df[2]
gn = df[3]
dl = len(c)

fig, ax = plt.subplots()
for i in range(dl):
    cl = 'green'
    if gn[i] < 0:
        cl = 'red'
    wh = 0.4

    eo = o[i]
    if i > 0:
        if (gn[i] < 0 and gn[i - 1] > 0) or (gn[i] > 0 and gn[i - 1] < 0):
            eo = ro[i]

    hi = c[i] - eo
    xy = (i, eo)
    rect = mpathes.Rectangle(xy, wh, hi, color=cl)
    ax.add_patch(rect)

plt.tight_layout()
plt.axis('auto')
plt.grid()
plt.show()