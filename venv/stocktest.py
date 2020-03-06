from stockcomstats import stockstats
import matplotlib.pyplot as plt

symbol = 'uvxy'
win = 30
datadict = stockstats(symbol, win)
I1, = plt.plot(datadict['Com'][1], datadict['Com'][0], label='Com')
I2, = plt.plot(datadict['Max'][1], datadict['Com'][0], label='Max')
I3, = plt.plot(datadict['Min'][1], datadict['Com'][0], label='Min')
plt.legend()
plt.tight_layout()
plt.grid()
plt.title(symbol.upper() + ', Win = ' + str(win))
plt.show()