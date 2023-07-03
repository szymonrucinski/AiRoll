# Import numpy and OpenCV
import numpy as np
import cv2
from matplotlib import pyplot as plt
from scipy.misc import derivative
import math
import time


def get_stable_footage(video_path):
    print('Searching for most stable part')
    try:
        cap = cv2.VideoCapture(video_path)
    except cv2.error as e:
        print('Loaded file - incorrectly')
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # step 2
    # Read first frame
    _, prev = cap.read()

    # Convert frame to grayscale
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    # translation
    # Pre-define transformation-store array
    transforms = np.zeros((n_frames - 4, 3), np.float32)

    for i in range(n_frames - 4):
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
        try:
            curr_pts, status, err = cv2.calcOpticalFlowPyrLK(
                prev_gray, curr_gray, prev_pts, None)
        except cv2.error as e:
            print('OpenCV optical flow error')
            return e

        # Sanity check
        assert prev_pts.shape == curr_pts.shape

        # Filter only valid points
        idx = np.where(status == 1)[0]
        prev_pts = prev_pts[idx]
        curr_pts = curr_pts[idx]
        # print(curr_pts)

        # Find transformation matrix
    #   m = cv2.estimateRigidTransform(prev_pts, curr_pts, fullAffine=False)
        # will only work with OpenCV-3 or less
        try:
            m, inliers = cv2.estimateAffinePartial2D(prev_pts, curr_pts)
        except cv2.error as e:
            print('OpenCV estimate AffinePartial2D error')
            break

        # Extract traslation
        try:
            dx = m[0, 2]
            dy = m[1, 2]
        except TypeError:
            break

        # Extract rotation angle
        da = np.arctan2(m[1, 0], m[0, 0])

        # Store transformation
        transforms[i] = [dx, dy, da]

        # Move to next frame
        prev_gray = curr_gray
        trajectory_x = np.cumsum(transforms, axis=0)
        trajectory_y = np.cumsum(transforms, axis=1)

    container_x = calc_dif(trajectory_x)
    container_y = calc_dif(trajectory_y)

    container_x = [x for x in container_x if x]
    container_x.sort(key=len, reverse=True)

    container_y = [y for y in container_y if y]
    container_y.sort(key=len, reverse=True)

    try:
        container = np.intersect1d(container_x, container_y)
        return (container[0], container[-1])
    except (IndexError, TypeError):
        try:
            return (container_y[0][0], container_y[0][-1])
        except IndexError:
            return IndexError


def calc_dif(trajectory):
    graph = []
    for el in trajectory:
        graph.append(el[1])
    dif_x = []
    for i, el in enumerate(graph):
        if i > 0:
            dif_x.append(round(el - graph[i - 1]))
    for i, el in enumerate(dif_x):
        if el <= 2 and el >= -2:
            dif_x[i] = 0
        else:
            dif_x[i] = 100
    container = []
    j = 0
    for i, el in enumerate(dif_x):
        if i > 0:
            if dif_x[i - 1] == 0 and el == 0:
                container[j].append(i)
            else:
                j = j + 1
                container.append([])
        else:
            container.append([])

    return container
