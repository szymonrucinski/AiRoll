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
import glob
from sys import platform
import shutil
import os
import librosa.display
from conf import SAMPLE_OUTPUTS


MIN_CUT_LEN = 0.5
MAX_CUT_LEN = 4


def get_audio_peaks(path, frame_rate):
    x, sr = librosa.load(get_isolated_drums(path))
    # onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_frames = librosa.onset.onset_detect(
        x,
        sr=sr,
        wait=1,
        pre_avg=30,
        post_avg=1,
        pre_max=30,
        post_max=1,
        backtrack=True)

    print(onset_frames)
    onset_times = librosa.frames_to_time(onset_frames)
    onset_times = onset_times * frame_rate
    onset_times = onset_times.astype(int)
    new_time_list = []

    for i, value in enumerate(onset_times):
        for j, checked in enumerate(onset_times):
            if checked - value >= frame_rate and len(new_time_list) == 0:
                new_time_list.append(checked)
                break
            if len(new_time_list) > 0 and checked - \
                    new_time_list[-1] >= frame_rate:
                new_time_list.append(checked)
                break

    new_time_list = sorted(set(new_time_list))
    output_path = f'{SAMPLE_OUTPUTS}\\trimmed.mp3'
    trim_audio = f'ffmpeg -i {path} -ss {new_time_list[0]/frame_rate} -to {new_time_list[-1]/frame_rate} -c copy {output_path}'
    subprocess.run(trim_audio)

    const = new_time_list[0]
    new_time_list = np.asarray(new_time_list)
    new_time_list = new_time_list - const
    cut_list = []
    for counter, index in enumerate(new_time_list):
        if counter == 0:
            cut_list.append({'cut_start': 0, 'cut_end': int((index))})
        else:
            prev_cut_end = cut_list[-1]['cut_end']
            cut_start = (prev_cut_end) + 1
            cut_end = index
            cut_list.append({'cut_start': cut_start, 'cut_end': cut_end})
    cut_list.pop(0)
    cut_list[0]['cut_start'] = 0
    print(cut_list)

    onset_times = librosa.frames_to_time(onset_frames)
    draw_graph(x, sr, onset_times)

    return cut_list, output_path


def get_isolated_drums(path):
    try:
        shutil.rmtree(f'{SAMPLE_OUTPUTS}')
        os.mkdir(SAMPLE_OUTPUTS)
    except OSError:
        print("Creation of the directory failed")

    if platform == "win32" or platform == "win64":
        subprocess.run(
            f'python -m spleeter separate -i {path} -o {SAMPLE_OUTPUTS}  -p spleeter:4stems')

    for x in glob.glob(f'{SAMPLE_OUTPUTS}/**/drums.wav', recursive=True):
        return x


def draw_graph(x, sr, onset_times):
    start_sec = 1
    end_sec = 45
    librosa.display.waveplot(x[sr * start_sec:sr * end_sec], sr=sr)
    for hit in onset_times:
        plt.axvline(hit, color='r')
    plt.savefig('wykres.pdf', dpi=200)
