import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import pandas as pd
import os

brickpath = r'D:\TrueFX Data\Bricks Data'
pairs = 'EURUSD'
brickfile = brickpath + os.sep + pairs + '-bricks-10bp.txt'

df = pd.read_csv(brickfile, header=None)
c = df[3] * 100
o = df[2] * 100
gn = df[4]
dl = len(c)

fig, ax = plt.subplots()
for i in range(dl):
    cl = 'green'
    if gn[i] < 0:
        cl = 'red'

    wh = 0.4
    hi = c[i] - o[i]
    xy = (i, o[i])
    rect = mpathes.Rectangle(xy, wh, hi, color=cl)
    ax.add_patch(rect)

plt.tight_layout()
plt.axis('auto')
plt.grid()
plt.show()