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
import subprocess
from sys import platform
from conf import SAMPLE_OUTPUTS


MIN_CUT_LEN = 0.5
MAX_CUT_LEN = 4


def get_audio_peaks(path, frame_rate):
    run_spleeter(path)
    x, sr = librosa.load(path)
    onset_frames = librosa.onset.onset_detect(
        x,
        sr=sr,
        wait=1,
        pre_avg=1,
        post_avg=1,
        pre_max=1,
        post_max=1,
        backtrack=True)
    print()
    indexes = librosa.frames_to_time(onset_frames)

    cut_list = []
    for counter, index in enumerate(indexes):
        if counter == 0:
            cut_list.append({'cut_start': 0,
                             'cut_end': int((index) * frame_rate)})
        else:
            prev_cut_end = cut_list[-1]['cut_end']
            cut_start = (prev_cut_end) + 1
            cut_end = (index) * frame_rate
            cut_list.append(
                {'cut_start': int(cut_start), 'cut_end': int(cut_end)})
    print(cut_list)

    return cut_list


def run_spleeter(path):
    if platform == "win32" or platform == "win64":
        f = open("spleeter.bat", "w+")
        f.write(
            f'python -m spleeter separate -i {path} -o {SAMPLE_OUTPUTS}  -p spleeter:4stems')
        f.close()
        subprocess.call([r'spleeter.bat'])


run_spleeter(r'D:\Programowanie\AI\editor\data\samples\inputs\jazz.mp3')
