import pytest
import librosa
import numpy as np
from PIL import Image
import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import scipy.signal
import scipy
import librosa 
import numpy as np
from detect_peaks import detect_peaks


def get_audio_peaks(path):
    x, sr = librosa.load(path)
    indexes = detect_peaks(x, mph = 0.9, mpd=sr/2)
    sample = np.zeros(len(x))
    for index in indexes:
        sample[index] = 1        
    return sample