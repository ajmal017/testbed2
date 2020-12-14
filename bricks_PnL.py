import matplotlib.pyplot as plt
import pandas as pd

symbol = 'EURUSD'
ipnum = 10

brickfile = r'D:\HIST Data\Bricks\{}-bricks-{}bp.txt'.format(symbol, ipnum)
TrueFxfile = r'D:\TrueFX Data\Bricks Data\{}-bricks-{}bp.txt'.format(symbol, ipnum)
df = pd.read_csv(TrueFxfile, header=None)
c = list(df[2])
o = list(df[0])
gn = list(df[3])
dl = len(c)

initcap = 10000
SorP = True
percent = 3
expense = 0

PnL = [initcap]
pos = 1
haspos = False
openforth = None
popenforth = None
openpos = False
openposbarnum = 0
openprice = 0
for i in range(dl):
    forth = True
    if gn[i] < 0:
        forth = False

    if i == 0:
        openposbarnum = i + 1
        openforth = forth
        openpos = True

    else:
        if openforth != forth and not openpos:
            openposbarnum = i + 1
            popenforth = openforth
            openforth = forth
            openpos = True

        if openpos:
            if i == openposbarnum:
                if haspos:
                    pnl = 0
                    if popenforth:
                        pnl = PnL[-1] + (c[i] - openprice - expense) * pos
                    else:
                        pnl = PnL[-1] + (openprice - c[i] - expense) * pos

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



