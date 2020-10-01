import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import pandas as pd
import os

brickfile = r'D:\Other Data\IVE_tickbidask_bricks_simp.csv'
df = pd.read_csv(brickfile)
c = list(df['Close'])
stdo = list(df['Std Open'])
o = list(df['Open'])
gn = list(df['Gap Num'])
dl = len(c)

initcap = 1000
SorP = False
percent = 3
expenss = 0.003

PnL = [initcap]
pos = 1
haspos = False
openforth = None
openpos = False
openposbarnum = 0
openprice = 0
for i in range(dl):
    forth = True
    if stdo[i] > c[i]:
        forth = False

    if i == 0:
        openposbarnum = i + 1
        openforth = forth
        openpos = True

    else:
        if openforth != forth and not openpos:
            openposbarnum = i + 1
            openforth = forth
            openpos = True

        if openpos:
            if i == openposbarnum:
                if haspos:
                    popenforth = not openforth
                    pnl = 0
                    if popenforth:
                        pnl = PnL[-1] + (c[i] - openprice - expenss) * pos
                    else:
                        pnl = PnL[-1] + (openprice - c[i] - expenss) * pos

                    PnL.append(pnl)
                    haspos = False

                openprice = o[i]
                if not SorP:
                    pos = int((PnL[-1] * percent) / openprice)
                    if pos <= 0:
                        pos = 0
                openpos = False
                haspos = True

plt.plot(PnL)
plt.tight_layout()
plt.grid()
plt.show()



