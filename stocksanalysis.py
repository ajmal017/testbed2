import pandas as pd
import os
import matplotlib.pyplot as plt

filepath = r'E:\stockdata'
symbol = 'spy'

ticker = pd.read_csv(filepath + os.sep + symbol + '.csv')
close = list(ticker['Close'])
adjclist = []
for i in range(len(close)):
    if i > 0:
        adjc = (close[i] - close[i - 1]) / close[i - 1]
        adjclist.append(adjc)

win = 3
rclist = []
for ci in range(len(close)):
    if ci >= win + 3:
        if close[ci - 3 - win] > 0 and close[ci - 2 - win] and close[ci - 1 - win] > 0:
            adjcm = 1
            rclist.append(adjclist[ci])

plt.hist(rclist, bins=200, density=True, cumulative=True)
plt.title(symbol.upper())
plt.tight_layout()
plt.grid()
plt.show()