import matplotlib.pyplot as plt
import pandas as pd
import os

path = r'E:\newdata\quandl data\CHRIS-CME_NG\final data'
files = os.listdir(path)

for fi in files:
    con = pd.read_csv(path + os.sep + fi)
    c = list(con['Last'])
    no = list(con['Date NO.'])

    plt.plot(no, c)
plt.grid()
plt.tight_layout()
plt.show()
