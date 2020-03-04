import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = r'E:\stockdata'
vx = pd.read_csv(filepath + os.sep + 'vx3.csv')
c = list(vx['Close'])
plt.plot(c)
plt.tight_layout()
plt.grid()
plt.show()