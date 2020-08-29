import matplotlib.pyplot as plt
import numpy as np
import math

x = list(range(0, 1000))
rt = 0.04 / 365
rb = 0.01 / 365
f = 0.14
y = [f * math.pow(1 + rt, i) / math.pow(1 + rb, i) for i in x]

plt.plot(x, y)
plt.show()