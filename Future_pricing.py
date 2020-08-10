import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
import os

r = 0.0001
rf = math.log(1 + r)


def future_price(S0: float, rt: int):
    Fp = S0 * math.pow((1 + rf), rt)
    return Fp


def Combo1(S0: float, rts: list):
    Cp = future_price(S0, rts[0]) - future_price(S0, rts[1]) * 2 + future_price(S0, rts[2])
    return Cp


br = [30, 60, 90]
dr = [30, 60, 90]
S0 = list(np.linspace(90, 110, 20))

for bi in br:
    for di in dr:
        Ls = []
        rts = []
        for ni in range(3):
            rt = bi + di * ni
            rts.append(rt)
        data = [Combo1(si, rts) for si in S0]
        Li = ''
        Ls.append(Li)
        Ls[-1], = plt.plot(S0, data, label='DR = ' + str(di))
    plt.title('BR = ' + str(bi))
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()







