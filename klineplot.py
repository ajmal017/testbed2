import matplotlib.pyplot as plt
import pandas as pd
import os

def Klinesplot(ticker, lillist:list):
    path = 'E:\stockdata'
    vix = pd.read_csv(path + os.sep + '^VIX.csv')
    stock = pd.read_csv(path + os.sep + ticker + '.csv')
    h = list(stock['High'])
    l = list(stock['Low'])
    c = list(stock['Close'])
    o = list(stock['Open'])

    vix = vix.tail(len(h))
    vixl = list(vix['Low'])
    vixh = list(vix['High'])
    vixc = list(vix['Close'])
    vixo = list(vix['Low'])

    adjivixlinedict = {}
    for ai in lillist:
        adjivixlinedict[ai] = []

    xlist = list(range(len(vixh)))
    riolist = []
    for i in xlist:
        rio = h[i] / vixh[i]
        riolist.append(rio)
        for k, v in adjivixlinedict.items():
            adjv = k * rio
            v.append(adjv)

    for si in range(len(h)):
        color = 'black'
        if c[si] > o[si]:
            color = 'r'
        elif c[si] < o[si]:
            color = 'g'
        plt.plot([si, si], [h[si], l[si]], color=color, lw=3)

    lgs = []
    for k, v in adjivixlinedict.items():
        lg = ''
        lgs.append(lg)
        lgs[-1], = plt.plot(xlist, v, label=k)
    # i1, = plt.plot(xlist, riolist, label='Rio')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.title(ticker.upper() + ' AdjValues')
    plt.show()

lils = [10, 12, 14, 17, 20, 25, 30, 35, 40, 50, 60, 70]
symbol = 'uvxy'
Klinesplot(symbol, lils)