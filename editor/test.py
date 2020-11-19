import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import math
import numpy as np

plt.rcParams['agg.path.chunksize'] = 1000
rate, data = wav.read('D://Programowanie//AI//editor//data//samples//inputs//around_the_world-atc.wav')
f = np.array(data[1], dtype=int)

plt.title('Song WAVE file')
plt.plot(data)
plt.show()