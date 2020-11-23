from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT
from moviepy.editor import *
from PIL import Image
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import scipy.signal
import scipy
import librosa 
import IPython.display as ipd
from playsound import playsound
import numpy as np
from audio_component.detect_peaks import detect_peaks
import matplotlib.pyplot as plt


arr = np.array([1,2,5,6,7,8,12,516,3])
detect_peaks(arr, mph = 1, mpd =1)
# indexes = detect_peaks(x, mph = 0.9, mpd=sr/2)

audio_dept = os.path.join(AUDIO_DEPT, 'mov')
source_path = os.path.join(SAMPLE_INPUTS, 'movie.mp4')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)

thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-frame")
thumbnail_per_half_second_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-half-second")


clip = VideoFileClip(source_path)

print(clip.reader.fps)
print(clip.reader.nframes)
duration = clip.duration
max_duration = int(duration) + 1

fps = clip.reader.fps
nframes = clip.reader.nframes
seconds = nframes / (fps*1.0)

#getAll frames
# for i in range(0, max_duration):
# # for i in range(0, max_duration + 1):
#     current_ms = int((i/fps) * 1000)
#     print(current_ms)
#     # if i % fps == 0:
#     # current_ms = int((i/fps) * 1000)
#     new_img_filepath = os.path.join(thumbnail_dir, f"{current_ms}.png")
#     frame = clip.get_frame(i)
#     new_img = Image.fromarray(frame)
#     new_img.save(new_img_filepath)

def saveFramesToImages():
    for i, frame in enumerate(clip.iter_frames()):
        # print(i, frame)
        fphs = int(fps/2)
        if i % fphs == 0:
            current_ms = int((i / fps) * 1000)
            new_img_filepath = os.path.join(SAMPLE_OUTPUTS, f"{current_ms}.jpg")
            # print(f"frame at {i} seconds saved at {new_img_filepath}")
            new_img = Image.fromarray(frame)
            new_img.save(new_img_filepath)


def main():
    detect_peaks('path')
    #   [{beginning:20.000, end:44.100,used: boolean}]
    #   convert to numpy array of video
    # remove 10s between [movie_movie_movie_movie_movie]

    #get
    #[0-20.000] -> [20.0001-44.100]
    #calculate length
def get_cuts_position(audio):
