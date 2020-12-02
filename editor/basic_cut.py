from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT
from moviepy.editor import *
from PIL import Image
import random
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

video_path = os.path.join(SAMPLE_INPUTS, 'videoplayback.mp4')
song_path = os.path.join(SAMPLE_INPUTS, 'song.mp3')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)
MAX_LEN = 30

def main():
    loaded_clip = VideoFileClip(video_path)
    duration = loaded_clip.duration
    frame_rate = loaded_clip.reader.fps
    nframes = loaded_clip.reader.nframes
    seconds = nframes / (frame_rate*1.0)
    cut_list = get_audio_peaks(song_path, frame_rate)
    print(cut_list)
    print(len(cut_list))


    start = []
    print("Rendering")
    for i ,frame in enumerate(loaded_clip.iter_frames()):
        start.append(frame)
        # num1 = random.randint(0, nframes)

        # print(cut_list[i])

        # if i== 300:
        #     break
        # if i <0 and i>500:
        #     start.append(frame)
        # elif i>4000 and i<4500:
        #     start.append(frame)
        # elif i>6000 and i<6500:
        #     start.append(frame)



        # if i%2 == 0:
        # np.append(new_sequence, np.ones((360,640,3))*255)
        # else:
        # print(frame)
        #     print(type(frame))
        #     print(np.shape(frame))
            # time.sleep(5)
        # print(i)
        # if i == 300:
        #     i = i + 100

        # if i == 500: 
        #     break
    render_sequence = []
    print(len(start))
    for i ,frame in enumerate(start):
        rand_num = random.randint(0, len(start)-1000)
        number_of_frames = cut_list[i]['cut_end'] - cut_list[i]['cut_start']
        print(number_of_frames)
        counter = 0
        while(counter<= number_of_frames):
            render_sequence.append(start[rand_num+counter])
            print(rand_num+counter)
            counter=counter+1
        if i== len(cut_list)-1:
            break

    print('done')
    # print(np.shape(loaded_clip.iter_frames()))
    clips = [ImageClip(frame).set_duration(1/frame_rate) for frame in render_sequence]
    # print(new_sequence)
    concat_clip = concatenate_videoclips(clips, method="compose")
    # del new_sequence
    # del new_sequence
    print(sys.getsizeof(clips))
    # del clips
    # loaded_music.set_duration(concat_clip)
    # ImageClip(concat_clip).set_audio(audio_path)
    concat_clip.write_videofile("2nd_test.mp4", audio=song_path, codec="mpeg4", fps=frame_rate)


main()
    #   [{beginning:20.000, end:44.100,used: boolean}]
    #   convert to numpy array of video
    # remove 10s between [movie_movie_movie_movie_movie]

    #get
    #[0-20.000] -> [20.0001-44.100]
    #calculate length
