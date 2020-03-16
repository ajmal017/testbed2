from stockcomstats import stockstats_sample
import matplotlib.pyplot as plt

symbol = 'amzn'
win = 45
samplerio = 0.1
datadict = stockstats_sample(symbol, win, samplerio)
I1, = plt.plot(datadict['Com'][1], datadict['Com'][0], label='Com')
I2, = plt.plot(datadict['Max'][1], datadict['Max'][0], label='Max')
I3, = plt.plot(datadict['Min'][1], datadict['Min'][0], label='Min')
I4, = plt.plot(datadict['Max-C'][1], datadict['Max-C'][0], label='Max-C')
I5, = plt.plot(datadict['Min-C'][1], datadict['Min-C'][0], label='Min-C')

ssize = len(datadict['Com'][1])
plt.legend()
plt.tight_layout()
plt.grid()
plt.title(symbol.upper() + ', Win=' + str(win) + ', Sample Size=' + str(ssize))
plt.show()