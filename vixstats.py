import matplotlib.pyplot as plt
import pandas as pd
import os

filepath = r'E:\ibdata\vxx\options'
files = os.listdir(filepath)
files = sorted(files)
strikes = [10, 11, 12, 13, 14, 15, 16]
datadict = {}
for d in strikes:
    datadict[d] = []
for f in files:
    df = pd.read_csv(filepath + os.sep + f)
    if not df.empty:
        fs = list(df['strike'])
        for s in strikes:
            idx = fs.index(s)
            datadict[s].append(df.at[idx, 'close P'])

for v in datadict.values():
    plt.plot(v)

plt.tight_layout()
plt.grid()
plt.show()
