from gapstats import gapstatfunc
import matplotlib.pyplot as plt

symbollist = ['AAPL', 'goog', 'bac', 'fb', 'ba', 'msft', 'v', 'cost', 'dis', 'nvda', 'amzn']
statgap = [-0.02, 0.02]
dictdict = {}
for si in symbollist:
    alldict = gapstatfunc(si, statgap)
    dictdict[si] = alldict[(-0.02, 0.02)]

lglist = []
for dk, dv in dictdict.items():
    ii = ''
    lglist.append(ii)
    lb = dk
    lglist[-1], = plt.plot(dv[1], dv[0], label=lb)

plt.tight_layout()
plt.legend()
plt.grid()
plt.title('GapCompares')
plt.show()
