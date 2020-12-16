from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT, BASE_DIR
from moviepy.editor import *
from PIL import Image
from copy import deepcopy
from fastai.vision.all import *
import cv2
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa
import time
import numpy as np
import matplotlib.pyplot as plt
from video_stab import get_stable_footage
from video_controller import Video_controller
from audio_component.get_audio_peaks import get_audio_peaks
from editing_tool import Editing_tool

model_path = os.path.join(BASE_DIR, 'model.pkl')
song_path = os.path.join(SAMPLE_INPUTS, 'song.mp3')

def init(video_paths):
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

        # scene_cut_list = find_scenes(video_path)
        # print(scene_cut_list)
        whole_movie = []
        slices = []
        sorted_cuts = []

        for i,frame in enumerate(vc.clip.iter_frames()):
            whole_movie.append(frame)
        usable_part = get_stable_footage(video_path)
        whole_movie = whole_movie[usable_part[0]:usable_part[-1]]
        # edit_tl.detect_blur(whole_movie, round(vc.get_fps()*2))

        print('added {}'.format(video_path))
        all_subclips[edit_tl.learn.predict(whole_movie[-1])[0]].append(whole_movie)
 
    
    all_subclips_copy = deepcopy(all_subclips)
    for i in all_subclips_copy:
        if len(all_subclips[i]) == 0:
            del all_subclips[i]
    all_subclips_copy = deepcopy(all_subclips)
    counter = 0
    done = False

    for i, tup in enumerate(cut_list):
        proper_order = list(all_subclips.keys())
        if proper_order == []:
            break
        size = len(proper_order) 
        l = i
        number_of_frames = cut_list[i]['cut_end'] - cut_list[i]['cut_start']
        if size == 0: key = proper_order[0]
        else: key = proper_order[(l % size)]
        print(key)
        cur_shot = all_subclips[key]
        done = True
        print(done)
        for j,scene in enumerate(cur_shot):
            if len(scene) >= number_of_frames:
                chunk = cur_shot.pop(j)
                print(np.shape(chunk), 'chunk')
                print(np.shape(cur_shot), 'cur_shot')
                render_sequence = render_sequence + chunk
                counter = len(chunk) + counter
                print(counter)
                break
                print(number_of_frames,len(chunk))


    clips = [ImageClip(frame).set_duration(1/vc.get_fps()) for frame in render_sequence]
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile("2nd_test.mp4", audio=song_path, codec="libx264", fps=vc.get_fps())
