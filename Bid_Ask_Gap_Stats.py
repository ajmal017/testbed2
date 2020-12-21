import matplotlib.pyplot as plt
import pandas as pd
import os

clearedfile = r'D:\IB Data\Tick Data\AMZN-tick.txt'
df = pd.read_csv(clearedfile, header=None)

gaps = (df[3] - df[2]).values
bl = len(gaps)
if bl > 10000:
    bl = 10000
plt.hist(gaps, bins=10000, density=True, cumulative=True)
plt.tight_layout()
plt.grid()
plt.show()