import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import math
import numpy as np
from maxima import findLocalMaximaMinima

plt.rcParams['agg.path.chunksize'] = 1000
rate, data = wav.read('D://Programowanie//AI//editor//data//samples//inputs//around_the_world-atc.wav')
f = data
# for chunk in f:
#     print(abs(chunk))

print(max(f))

# plt.title('Song WAVE file')
# plt.plot(data)
# plt.show()