
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import librosa 
import IPython.display as ipd


#Load a .wav file
x, sr = librosa.load('D:\\Programowanie\\AI\\editor\\data\\samples\\inputs\\around_the_world-atc.wav')
type(x)
print('x length ={}'.format(len(x)))
print('sample rate = {}'.format(sr))
print('sound clip is {} seconds long' .format((len(x)/sr)))

fhat = np.fft.fft(x)
type(fhat)
len(fhat)

#POWER SPECTRUM PSD
PSD = fhat * np.conj(fhat) /len(x)
indices = PSD<10000
PSDclean = PSD * indices
fhat = indices * fhat

ffilt = np.fft.ifft(fhat)
ffilt_new = np.int16(abs(ffilt))
write('first_sine_wave.wav', sr, ffilt_new)



