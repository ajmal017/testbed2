import matplotlib.pyplot as plt
from strfunc import strFunc


if __name__  == '__main__':
    symbol = 'uvxy'
    PnLLine, rPnLLine, xlist = strFunc(symbol, win=60, fd=False, gap=0.15, asrio=0.2, bars=1100)
    pxlist = list(range(len(PnLLine)))
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    i1, = ax1.plot(pxlist, PnLLine, label='Abs P / L')
    i2, = ax2.plot(pxlist, rPnLLine, label='Comp P / L')
    fig.legend()
    # fig.title(symbol.upper())
    # fig.grid()
    # fig.tight_layout()
    plt.show()
