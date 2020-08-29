import matplotlib.pyplot as plt
import pandas as pd
import math
import os


def future_price(s: float, Rf: float, ret: int):
    return s * math.exp(Rf * ret)


interveT = 30
interveT2 = 60
interveT3 = 90
deltaT = list(range(91))
r = 0.02
rf = math.log(1 + r)
S = 5

combo = [future_price(S, rf, rei / 365) - future_price(S, rf, (rei + interveT) / 365) * 2 + future_price(S, rf, (rei + 2 * interveT) / 365) for rei in deltaT]
combo2 = [future_price(S, rf, rei / 365) - future_price(S, rf, (rei + interveT2) / 365) * 2 + future_price(S, rf, (rei + 2 * interveT2) / 365) for rei in deltaT]
combo3 = [future_price(S, rf, rei / 365) - future_price(S, rf, (rei + interveT3) / 365) * 2 + future_price(S, rf, (rei + 2 * interveT3) / 365) for rei in deltaT]

# combo = [future_price(S, rf, (rei + interveT) / 365) - future_price(S, rf, rei / 365) for rei in deltaT]
# combo2 = [future_price(S, rf, (rei + interveT2) / 365) - future_price(S, rf, rei / 365) for rei in deltaT]
# combo3 = [future_price(S, rf, (rei + interveT3) / 365) - future_price(S, rf, rei / 365) for rei in deltaT]

plt.plot(combo)
plt.plot(combo2)
plt.plot(combo3)
print(combo[-1] / combo[0], combo2[-1] / combo2[0], combo3[-1] / combo3[0])
plt.tight_layout()
plt.grid()
plt.show()