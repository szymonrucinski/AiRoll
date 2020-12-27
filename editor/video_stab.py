# Import numpy and OpenCV
import numpy as np
import cv2
from matplotlib import pyplot as plt 
from scipy.misc import derivative
import math
import time

def get_stable_footage(video_path):
    print('Searching for most stable part')

    cap = cv2.VideoCapture(video_path)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)


    #step 2
    # Read first frame
    _, prev = cap.read() 

    # Convert frame to grayscale
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY) 

    #translation
    # Pre-define transformation-store array
    transforms = np.zeros((n_frames-4, 3), np.float32) 

    for i in range(n_frames-4):
      # Detect feature points in previous frame
      prev_pts = cv2.goodFeaturesToTrack(prev_gray,
                                         maxCorners=200,
                                         qualityLevel=0.01,
                                         minDistance=30,
                                         blockSize=3)
    
      # Read next frame
      success, curr = cap.read() 
      if not success: 
        break 

      # Convert to grayscale
      curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY) 

      # Calculate optical flow (i.e. track feature points)
      curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None) 

      # Sanity check
      assert prev_pts.shape == curr_pts.shape 

      # Filter only valid points
      idx = np.where(status==1)[0]
      prev_pts = prev_pts[idx]
      curr_pts = curr_pts[idx]

      #Find transformation matrix
    #   m = cv2.estimateRigidTransform(prev_pts, curr_pts, fullAffine=False) 
      #will only work with OpenCV-3 or less
      m, inliers = cv2.estimateAffinePartial2D(prev_pts, curr_pts)

      # Extract traslation
      dx = m[0,2]
      dy = m[1,2]

      # Extract rotation angle
      da = np.arctan2(m[1,0], m[0,0])
    
      # Store transformation
      transforms[i] = [dx,dy,da]

      # Move to next frame
      prev_gray = curr_gray
      trajectory = np.cumsum(transforms, axis=0)



    graph = []
    for el in trajectory:
        graph.append(el[1])

    dif_x = []
    for i,el in enumerate(graph):
        if i> 0:
           dif_x.append(round(el - graph[i-1]))

    for i, el in enumerate(dif_x):
        if el <= 5 and el >= -5:
            dif_x[i] = 0
        else:
            dif_x[i] = 100
    container = []
    j = 0

    for i, el in enumerate(dif_x):
        if i>0:
            if dif_x[i-1] ==0 and el == 0:
                container[j].append(i)
            else:
                j = j + 1
                container.append([])
        else:
            container.append([])
    container = [x for x in container if x]
    container.sort(key=len, reverse=True)
    return (container[0][0],container[0][-1])

