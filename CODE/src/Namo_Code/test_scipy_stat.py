from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1, 1)

mean, var, skew, kurt = norm.stats(moments='mvsk')
x = np.linspace(norm.ppf(0.01),norm.ppf(0.99), 100)

ax.plot(x, norm.pdf(x),'r-', lw=5, alpha=0.6, label='norm pdf')

plt.show()
