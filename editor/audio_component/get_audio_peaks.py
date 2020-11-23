import pytest
import librosa
import time
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

MIN_CUT_LEN = 0.33
MAX_CUT_LEN = 3

def get_audio_peaks(path):
    x, sr = librosa.load(path)
    indexes = detect_peaks(x, mph = 0.8, mpd=sr/2)
    print(type(indexes))
    cut_list = []
    for counter,index in enumerate(indexes):
        if counter == 0:
            cut_list.append({'cut_start':0,'cut_end':index, 'used':False})
        else:
            prev_cut_end = cut_list[-1]['cut_end']
            cut_len = (indexes[counter] - indexes[counter-1])/sr
            print(cut_len)
            if cut_len > MIN_CUT_LEN and cut_len < MAX_CUT_LEN:
                cut_list.append({'cut_start':prev_cut_end+1,'cut_end':index, 'used':False})
                print(len(cut_list))
                # print('cut duration: {}'.format(abs(prev_cut_end - index)/sr))
    return cut_list

PATH = 'D:\\Programowanie\\AI\\editor\\data\\samples\\inputs\\temple_of_love-sisters_of_mercy.wav'

get_audio_peaks(PATH)

