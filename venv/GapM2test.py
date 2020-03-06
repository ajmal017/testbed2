import matplotlib.pyplot as plt
from GapM2ValueStats import gapM2func

symbol = 'ba'
statgaps = [-0.05, -0.02]
gapnum = 30
datadict = gapM2func(symbol, statgaps, gapnum)

x = datadict[(-0.05, -0.02)][0][1]
y = datadict[(-0.05, -0.02)][0][0]

plt.plot(x, y)
plt.tight_layout()
plt.title(symbol.upper())
plt.grid()
plt.show()

