import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\stockdata'
ticker = 'svxy'
stock = pd.read_csv(path + os.sep + ticker + '.csv')
c = list(stock['Close'])
win = 60
adjclist = []
for i in range(len(c)):
    if i >= win:
        adjc = (c[i] - c[i - win]) / c[i - win]
        adjclist.append(adjc)

plt.hist(adjclist, bins=200, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.title(ticker.upper() + ', WIN = ' + str(win))
plt.show()