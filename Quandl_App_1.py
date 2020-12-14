from Quandl_Utils import QuandlDfCleaner as qdc
import matplotlib.pyplot as plt
import pandas as pd

symbol = 'ES'
frontm = 1
backm = 2
front = r'D:\Quandl Data\{}\CHRIS-CME_{}{}.csv'.format(symbol, symbol, frontm)
back = r'D:\Quandl Data\{}\CHRIS-CME_{}{}.csv'.format(symbol, symbol, backm)

dflist = [pd.read_csv(front), pd.read_csv(back)]
[dff, dfb] = qdc(dflist, True)

# spread = dfb['Last'] - dff['Last']
# spread_pc = spread / ((dfb['Last'] + dff['Last']) / 2)
# spread_pc_2 = list(sorted(spread_pc))[20: -20]
# spread_pc_abs = list(sorted(abs(spread_pc)))[:-40]

intradaychg = abs((dfb['Last'] - dff['Last']) - (dfb['Open'] - dff['Open'])) / ((dfb['Last'] + dff['Last'] + dfb['Open'] + dff['Open']) / 4)
chg = list(sorted(intradaychg))
chg = chg[: -40]
# plt.plot(spread)
plt.hist(chg, bins=1000, density=True, cumulative=True)

plt.tight_layout()
plt.title(symbol + ': M{} - M{}'.format(backm, frontm))
plt.grid()
plt.show()
