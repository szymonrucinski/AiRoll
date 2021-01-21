from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS, AUDIO_DEPT, BASE_DIR, MODEL_PATH
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
import concurrent.futures
import numpy as np
import subprocess
import random
import matplotlib.pyplot as plt
from video_stab import get_stable_footage
from video_controller import Video_controller
from get_audio_peaks import get_audio_peaks
from editing_tool import Editing_tool


def init(video_paths, song_path, progress):
    edit_tl = Editing_tool(MODEL_PATH)
    frame_rate = 25
    render_sequence = []
    all_subclips = {
        'extreme_wide_shot': [],
        'longShot': [],
        'medium_shot': [],
        'full_shot': [],
        'close_up_shot': [],
        'detail': []}
    # cut_list, new_song_path = get_audio_peaks(song_path, frame_rate)
    # pool = ThreadPool(processes=2)
    # async_result = pool.apply_async(get_audio_peaks, (song_path, frame_rate))
    # cut_list, song_path = async_result.get()
    cut_list, song_path = get_audio_peaks(song_path, frame_rate)
    all_videos = len(video_paths)
 
    for j, video_path in enumerate(video_paths):
        # handle corrupted video files
        try:
            vc = Video_controller(video_path)
        except: 
            KeyError
            continue

        n_frames = vc.clip.reader.nframes
        whole_movie = [frame for frame in vc.clip.iter_frames()]
        usable_part = get_stable_footage(video_path)
        try:
            whole_movie = whole_movie[usable_part[0]:usable_part[-1]]
            whole_movie = edit_tl.frame_info_overlay(whole_movie)
        except (IndexError, TypeError, cv2.error):
            print('Not usable')
            whole_movie = []
            continue
        if len(whole_movie) < 2*frame_rate:
            continue
        # edit_tl.detect_blur(whole_movie, round(vc.get_fps()*2))

        print('added {}'.format(video_path))
        print(f'{len(whole_movie)}')
        all_subclips[edit_tl.learn.predict(
            whole_movie[-1])[0]].append(whole_movie)
        progress['value'] = (j / all_videos) * 100

    all_subclips_copy = deepcopy(all_subclips)
    for i in all_subclips_copy:
        if len(all_subclips[i]) == 0:
            del all_subclips[i]
        else: random.shuffle(all_subclips[i])
        #shuffle videos in shot_type
        
    del all_subclips_copy
    counter = 0
    done = False

    for i, tup in enumerate(cut_list):
        proper_order = list(all_subclips.keys())
        if proper_order == []:
            break
        size = len(proper_order)
        l = i
        if i < len(cut_list) - 1:
            number_of_frames = cut_list[i]['cut_end'] - \
                cut_list[i]['cut_start']
            if size == 0:
                key = proper_order[0]
            else:
                key = proper_order[(l % size)]
            print(key)
            cur_shot = all_subclips[key]
            done = True
            print(done)
            for j, scene in enumerate(cur_shot):
                if len(scene) >= number_of_frames:
                    chunk = cur_shot.pop(j)
                    render_sequence = render_sequence + \
                        chunk[0:number_of_frames + 1]
                    counter = len(chunk) + counter
                    print('using:{}'.format(cut_list[i]), len(
                        chunk[0:number_of_frames + 1]))
                    break
                    # print(number_of_frames,len(chunk))

    old_song_path = f'{SAMPLE_OUTPUTS}\\trimmed.mp3'
    new_song_path = f'{SAMPLE_OUTPUTS}\\final.mp3'

    trim_audio = f'ffmpeg -i {old_song_path} -ss {0} -to {len(render_sequence)/25} -c copy {new_song_path}'
    subprocess.run(trim_audio)

    clips = [ImageClip(frame).set_duration(1 / vc.get_fps())
             for frame in render_sequence]
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(
        os.path.join(
            BASE_DIR,
            "render.mp4"),
        audio=new_song_path,
        codec="libx264",
        fps=vc.get_fps())
    progress['value'] = 100
    command = f'ffmpeg -i {os.path.join(BASE_DIR,"render.mp4")}  -filter_complex "afade=d=2, areverse, afade=d=2, areverse" {os.path.join(BASE_DIR,"output.mp4")}'
    subprocess.run(command)
    subprocess.run(
        f'explorer / select,"{os.path.join(BASE_DIR,"output.mp4")}"')
