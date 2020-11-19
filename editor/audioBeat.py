import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=[16,12]

#create a simple signal with two frequencies
dt= 0.001
t = np.arange(0,1,dt)
#sum of 2 frequencies
f = np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t)
f_clean = f
f = f + 2.5 * np.random.randn(len(t))

plt.plot(t,f,color='c',linewidth=1.5,label='Noisy')
plt.plot(t,f_clean,color='r',linewidth=2,label='Clean')
plt.xlim(t[0],t[-1])
plt.legend()
plt.show()