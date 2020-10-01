import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import pandas as pd
import os

brickfile = r'D:\Other Data\IVE_tickbidask_bricks_simp.csv'

df = pd.read_csv(brickfile)
c = df['Close']
stdo = df['Std Open']
o = df['Open']
gn = df['Gap Num']
dl = len(c)

fig, ax = plt.subplots()
for i in range(dl):
    cl = 'green'
    if stdo[i] > c[i]:
        cl = 'red'

    wh = 0.4
    hi = c[i] - o[i]
    xy = (i, o[i])
    rect = mpathes.Rectangle(xy, wh, hi, color=cl)
    ax.add_patch(rect)

plt.tight_layout()
plt.axis('equal')
plt.grid()
plt.show()
