import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import math
import numpy as np

plt.rcParams['agg.path.chunksize'] = 1000
rate, audio_file = wav.read('D://Programowanie//AI//editor//data//samples//inputs//around_the_world-atc.wav')
f = np.array(audio_file[1], dtype=int)
#values
n = len((audio_file[1]))
t = np.arange(0,n)
time_seconds = n/audio_file[0]/60
#fhat vector s of fourier coefficients, complex values
fhat = np.fft.fft(f,n)
#Power spectrum (power per frequency)
PSD = fhat * np.conj(fhat)/n
freq = (1/(n)) * np.arange(n)
L = np.arange(1,np.floor(n/2), dtype='int')
fig, axs = plt.subplots(2,1)

#time vs frequency
# time = np.linspace(0., time_seconds, audio_file[1])
plt.sca(axs[0])
plt.title('Song WAVE file')
plt.plot(audio_file)
plt.xlim(t[0],t[-1])
plt.sca(axs[1])

#frequency vs power
plt.plot(freq[L], PSD[L])
plt.show()