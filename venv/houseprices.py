import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = r'E:\hp'
filename = 'Zip_Zhvi_AllHomes.csv'
file = pd.read_csv(filepath + os.sep + filename, encoding='gbk')
plist = list(file.iloc[0])[7:]
plt.plot(plist)
plt.tight_layout()
plt.grid()
plt.show()