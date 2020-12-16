from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT, BASE_DIR
from moviepy.editor import *
from PIL import Image
import random
from copy import deepcopy
from fastai.vision.all import *
import cv2
import librosa
from PIL import ImageFont
from PIL import ImageDraw 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import scipy.signal
import scipy
import librosa
from colorthief import ColorThief
import time
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt
from video_controller import Video_controller
from audio_component.get_audio_peaks import get_audio_peaks
from editing_tool import Editing_tool
from scenedetect import VideoManager
from scenedetect import SceneManager
from scenedetect.detectors import ContentDetector

# video_path = os.path.join(SAMPLE_INPUTS, 'videoplayback.mp4')
model_path = os.path.join(BASE_DIR, 'model.pkl')
song_path = os.path.join(SAMPLE_INPUTS, 'song.mp3')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)

def find_scenes(video_path, threshold=10):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(
        ContentDetector(threshold=threshold))

    base_timecode = video_manager.get_base_timecode() 
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    return scene_manager.get_scene_list(base_timecode)

def init(video_paths, MAX_LEN):
    edit_tl = Editing_tool('D:\Programowanie\AI\shot_classifier\model.pkl')
    render_sequence = []
    vc = None
    all_subclips = {'extreme_wide_shot':[],'longShot':[],'medium_shot':[],'full_shot':[], 'close_up_shot':[], 'detail':[]}
    # whole_movie = edit_tl.frame_info_overlay(vc.clip)
    cut_list_used_once = False
    cut_list = None
    for video_path in video_paths:

        vc = Video_controller(video_path)

        if cut_list_used_once == False :
            cut_list = get_audio_peaks(song_path, vc.get_fps())
            new_list = []
            for i,element in enumerate(cut_list):
                if i%3 == 0: 
                    new_list.append(element)
            cut_list = new_list
            cut_list_used_once = True

        scene_cut_list = find_scenes(video_path)
        print(scene_cut_list)
        whole_movie = []
        slices = []
        sorted_cuts = []
        MAX_LEN = int(MAX_LEN * vc.get_fps())

        for i,frame in enumerate(vc.clip.iter_frames()):
            whole_movie.append(frame)

        for i, scene in enumerate(scene_cut_list):
            sub_clip = whole_movie[scene[0].get_frames() : scene[1].get_frames()]
            #statistical check
            if edit_tl.learn.predict(sub_clip[0])[0] == edit_tl.learn.predict(sub_clip[1])[0]:
                all_subclips[edit_tl.learn.predict(sub_clip[0])[0]].append(sub_clip)
        # for i in proper_order:
        #     flat_list = [item for sublist in all_subclips[i] for item in sublist]
        #     render_sequence= flat_list+render_sequence
        #     print('ok')
    
    all_subclips_copy = deepcopy(all_subclips)
    for i in all_subclips_copy:
        if len(all_subclips[i]) == 0:
            del all_subclips[i]
    all_subclips_copy = deepcopy(all_subclips)
    counter = 0
    done = False

    # while True:
    #     if done == True:
    #         break
    for i, tup in enumerate(cut_list):
        proper_order = list(all_subclips.keys())
        size = len(proper_order)
        number_of_frames = cut_list[i]['cut_end'] - cut_list[i]['cut_start']
        l = i
        key = proper_order[l % size]
        cur_shot = all_subclips[key]
        print(l % size)
        if len(cur_shot) == 0:
            del all_subclips[key]
            l = i + 1
            key = proper_order[l % size]
        done = True
        print(done)
        for j,scene in enumerate(cur_shot):
            if len(scene) >= number_of_frames:
                chunk = cur_shot.pop(j)
                print(np.shape(chunk), 'chunk')
                print(np.shape(cur_shot), 'cur_shot')
                render_sequence = render_sequence + edit_tl.detect_blur(chunk, number_of_frames)
                counter = len(render_sequence)
                counter = len(chunk) + counter
                print(counter)
                break
                # print(key)
                # print(counter)
                print(number_of_frames,len(chunk))
                # done = False
                # break
            # if done == True:
            #     print('EXIT')
            #     break

            

    print('Hello')
    clips = [ImageClip(frame).set_duration(1/vc.get_fps()) for frame in render_sequence]
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile("2nd_test.mp4", audio=song_path, codec="libx264", fps=vc.get_fps())
