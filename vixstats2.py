import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from myfuncs import cumcovert
import os

path = 'E:\stockdata'
vix = pd.read_csv(path + os.sep + '^VIX.csv')
vixc = list(vix['Close'])
binnum = len(vixc)
plt.figure()
plt.subplot(121)
plt.hist(vixc, bins=200, density=True, cumulative=False)
#plt.tight_layout()
plt.grid()
plt.subplot(122)
plt.hist(vixc, bins=200, density=True, cumulative=True)
#plt.tight_layout()
plt.grid()
plt.show()