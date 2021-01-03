from moviepy.editor import *
import sys
import numpy as np
import PIL
import moviepy
from collections import Counter 
from fastai.vision.all import *
from PIL import ImageFont
from PIL import ImageDraw
import cv2

class Editing_tool:
    def __init__(self, model_path):
        self.learn = load_learner(model_path)
    
    def frame_info_overlay(self,clip):
        start = []
        f_path = 'C:\\WINDOWS\FONTS\AGENCYR.TTF'
        font = ImageFont.truetype(f_path, 50)
        evaluate_shot = clip[::30]
        verdict = []
        for frame in evaluate_shot:
            verdict.append(str(self.learn.predict(frame)[0]))
        
        counter = Counter(verdict) 
        verdict = counter.most_common(1)
        print('It is a ',verdict[0][0])


        for i ,frame in enumerate(clip):
            n_img = Image.fromarray(frame, 'RGB')
            draw = ImageDraw.Draw(n_img)
            draw.text((0, 0),verdict[0][0],(255,255,255),font)
            frame = np.array(n_img)
            start.append(frame)
        return start
    
    def are_frames_similar(self,imageA, imageB):
        return np.square(np.subtract(imageA, imageB)).mean()
    
    def extract_frames(self,clip,path,name):
        for i ,frame in enumerate(clip.iter_frames()):
            if i%20 ==0:
                n_img = Image.fromarray(frame, 'RGB')
                n_img.save(os.path.join(path,f'{name}-{i}.png'))
    
    def detect_blur(self,chunk, number_of_frames):
        lap_values = []
        compared_values = []

        for i,frame in enumerate(chunk):
            # print(frame)
            # img = cv2.fromarray()
            # img = Image.fromarray(frame, 'RGB')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            lap_values.append([fm,i])

        lap_values.sort(key = lambda x: x[0], reverse=True)

        for i, val in enumerate(lap_values):
            if  val[1] + number_of_frames -1 <= len(chunk):
                print('CUT ON MOTION')
                ind1 = val[1]
                ind2 = val[1] + number_of_frames - 1
                return chunk[ind1:ind2]
        
        return chunk

        



