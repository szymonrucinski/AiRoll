import sys
import numpy as np
import PIL
from collections import Counter
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image

import cv2
import onnxruntime as nxrun
import numpy as np
from skimage.transform import resize
from skimage import io


class Editing_tool:
    def __init__(self, model_path):
        pth = model_path

    def predict_frame(self,frame):
        classes = ['close_up_shot','detail','extreme_wide_shot','full_shot','long_shot','medium_shot']
        # n_img = Image.fromarray(frame, 'RGB')
        res = cv2.resize(frame, dsize=(640, 360), interpolation=cv2.INTER_CUBIC)
        res = res.astype(np.float32)





        

        # print("The model expects input shape: ", self.sess.get_inputs()[0].shape)
        # print("The shape of the Image is: ", res.shape)
        # input_name = self.sess.get_inputs()[0].name
        # label_name = self.sess.get_outputs()[0].name
        # result = self.sess.run(None, {input_name: res})
        # prob = result[0]
        # final = prob.ravel()[:10]
        img224 = resize(res / 255, (3, 640, 360), anti_aliasing=True)
        ximg = img224[np.newaxis, :, :, :]
        ximg = ximg.astype(np.float32)

        sess = nxrun.InferenceSession('D:\\Programowanie\\AI\\editor\\shot_classifier.onnx')


        print("The model expects input shape: ",sess.get_inputs()[0].shape)
        print("The shape of the Image is: ", ximg.shape)
        input_name = sess.get_inputs()[0].name
        label_name = sess.get_outputs()[0].name
        result = sess.run(None, {input_name: ximg})
        prob = result[0]
        final = prob.ravel()[:10]
        print(classes[np.argmax(final)])

        return classes[np.argmax(final)]


    def frame_info_overlay(self, clip):
        start = []
        f_path = r'C:\\WINDOWS\FONTS\AGENCYR.TTF'
        font = ImageFont.truetype(f_path, 50)
        evaluate_shot = clip[::30]
        verdict = []
        for frame in evaluate_shot:
            verdict.append(self.predict_frame(frame))

        counter = Counter(verdict)
        verdict = counter.most_common(1)
        print('It is a ', verdict[0][0])

        for i, frame in enumerate(clip):
            n_img = Image.fromarray(frame, 'RGB')
            draw = ImageDraw.Draw(n_img)
            draw.text((0, 0), verdict[0][0], (255, 255, 255), font)
            frame = np.array(n_img)
            start.append(frame)
        return start

    def are_frames_similar(self, imageA, imageB):
        return np.square(np.subtract(imageA, imageB)).mean()

    def extract_frames(self, clip, path, name):
        for i, frame in enumerate(clip.iter_frames()):
            if i % 20 == 0:
                n_img = Image.fromarray(frame, 'RGB')
                n_img.save(os.path.join(path, f'{name}-{i}.png'))

    def detect_blur(self, chunk, number_of_frames):
        lap_values = []
        compared_values = []

        for i, frame in enumerate(chunk):
            # print(frame)
            # img = cv2.fromarray()
            # img = Image.fromarray(frame, 'RGB')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            lap_values.append([fm, i])

        lap_values.sort(key=lambda x: x[0], reverse=True)

        for i, val in enumerate(lap_values):
            if val[1] + number_of_frames - 1 <= len(chunk):
                print('CUT ON MOTION')
                ind1 = val[1]
                ind2 = val[1] + number_of_frames - 1
                return chunk[ind1:ind2]

        return chunk
