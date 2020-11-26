from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT
from moviepy.editor import *
from PIL import Image
import cv2
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import scipy.signal
import scipy
import librosa 
import time
import IPython.display as ipd
from playsound import playsound
import numpy as np
import matplotlib.pyplot as plt
from audio_component.get_audio_peaks import get_audio_peaks

video_path = os.path.join(SAMPLE_INPUTS, 'movie.mp4')
audio_path = os.path.join(SAMPLE_INPUTS, 'africa-toto.wav')
song_path = os.path.join(SAMPLE_INPUTS, 'song.mp3')


thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-frame")
thumbnail_per_half_second_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-half-second")
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

# def saveFramesToImages(cut_list):
#     for i, frame in enumerate(clip.iter_frames()):
#         # print(i, frame)
#         fphs = int(fps/2)
#         if i % fphs == 0:
#             current_ms = int((i / fps) * 1000)
#             new_img_filepath = os.path.join(SAMPLE_OUTPUTS, f"{current_ms}.jpg")
#             # print(f"frame at {i} seconds saved at {new_img_filepath}")
#             new_img = Image.fromarray(frame)
#             new_img.save(new_img_filepath)


def main():
    loaded_clip = VideoFileClip(video_path)
    loaded_music = AudioFileClip(audio_path)
    duration = loaded_clip.duration
    fps = loaded_clip.reader.fps
    nframes = loaded_clip.reader.nframes
    seconds = nframes / (fps*1.0)
    cut_list = get_audio_peaks(audio_path, fps)
    new_sequence = []
    print(type(new_sequence))

    for i,frame in enumerate(loaded_clip.iter_frames()):
        if i%2 ==0:
            new_sequence.append(np.ones([1080,1920,3]))
            # new_sequence.append(frame)
        else:
            new_sequence.append(frame)



        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # print(type(gray_frame))
        # print(np.shape(gray_frame))
    

    clips = [ImageClip(frame).set_duration(1/25) for frame in new_sequence]
    concat_clip = concatenate_videoclips(clips, method="compose")
    # concat_clip.set_audio(loaded_clip)
        # ImageClip(concat_clip).set_audio(audio_path)
    concat_clip.write_videofile("test.mp4",audio=song_path, codec="mpeg4",fps=25)

    # frames = np.asarray(new_sequence, dtype = None, order = None)
    # print(type(frames), np.shape(frames))
    # print(frames[1])
    # time.sleep(5)
    # work_clip = ImageSequenceClip(frames[2], fps=6)
    #         # print(frame)

    # work_clip.write_videofile("render.mp4")


main()
    #   [{beginning:20.000, end:44.100,used: boolean}]
    #   convert to numpy array of video
    # remove 10s between [movie_movie_movie_movie_movie]

    #get
    #[0-20.000] -> [20.0001-44.100]
    #calculate length
