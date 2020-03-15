import matplotlib.pyplot as plt
from gapfunc import gapFunc

symbol = 'bac'
sumPnL, rltPnL, PnLNum = gapFunc(symbol, win=60, gaps=(-0.04, -0.02), sk=0.6, asrio=0.1, bars=3300)
xlist = list(range(len(rltPnL)))

plt.plot(rltPnL)
plt.show()