import matplotlib.pyplot as plt
import pandas as pd
import os

def Kplot(ticker, lil=20):
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

    Numlist = []
    Plotlist = []
    for i in range(len(vixh)):
        if lil < vixh[i]:
            Numlist.append(i)

    for ni in Numlist:
        pp = (lil / vixh[ni]) * h[ni]
        pl = ([ni - 0.5, ni + 0.5], [pp, pp])
        Plotlist.append(pl)
    adplist = []
    adpNumlist = []
    for ip in range(len(Plotlist)):
        if ip > 0:
            if Plotlist[ip][0][0] == Plotlist[ip - 1][0][1]:
                adp = ([Plotlist[ip][0][0], Plotlist[ip][0][0]], [Plotlist[ip][1][0], Plotlist[ip - 1][1][0]])
                adplist.append(adp)
                adpNumlist.append(ip)
    adpNumlist = list(reversed(adpNumlist))
    adplist = list(reversed(adplist))
    for adpi in range(len(adplist)):
        Plotlist.insert(adpNumlist[adpi], adplist[adpi])


    for si in range(len(h)):
        color = 'black'
        if c[si] > o[si]:
            color = 'r'
        elif c[si] < o[si]:
            color = 'g'
        plt.plot([si, si], [h[si], l[si]], color=color, lw=3)

    for api in Plotlist:
        plt.plot(api[0], api[1], color='blue')
    plt.tight_layout()
    plt.grid()
    plt.title(ticker.upper() + ', VIX=' + str(lil))
    plt.show()


symbol = 'uvxy'
Kplot(symbol, lil=40)