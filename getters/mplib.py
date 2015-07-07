import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.ion()

X = np.linspace(-3, 2, 200)
Y = X ** 2 - 2 * X + 1.

plt.plot(X, Y)
plt.show()
