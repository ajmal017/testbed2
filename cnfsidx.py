import matplotlib.pyplot as plt
import pandas as pd
import os

path = 'E:\CNFs'
symbols = ['fanh', 'noah', 'yrd', 'xrf', 'hx', 'dnjr', 'wei', 'cnf']
stikers = []
minl = 9999999999999999999
for si in symbols:
    st = pd.read_csv(path + os.sep + si + '.csv')
    l = len(st)
    if minl > l:
        minl = l
    stikers.append(st)

adjclist = []
sm = 10000
for sti in stikers:
    stii = sti.tail(minl)
    c = list(stii['Close'])
    sp = c[0]
    sha = sm / sp
    adjc = [ci * sha for ci in c]
    adjclist.append(adjc)

cl = len(adjclist)
rio = cl * 100
fcloselist = []
for i in range(minl):
    fc = 0
    for ti in range(cl):
        fc += adjclist[ti][i] / rio
    fcloselist.append(fc)

plt.plot(fcloselist)
plt.tight_layout()
plt.grid()
plt.show()



