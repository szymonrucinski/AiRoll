import pytest
import librosa
import numpy as np
from get_audio_peaks import get_audio_peaks

PATH = 'D:\\Programowanie\\AI\\editor\\data\\samples\\inputs\\temple_of_love-sisters_of_mercy.wav'

def test_detect_peaks():
    audio_numpy_arr = get_audio_peaks(PATH)
    assert type(audio_numpy_arr) == np.ndarray and len(audio_numpy_arr) > 0
