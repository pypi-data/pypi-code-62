#! /usr/bin/env python
import dlib
import os
import numpy as np

env_dist = os.environ
env_path = env_dist['_'].split("/bin/python")[0]

PREDICTOR_PATH = os.path.join(env_path, "models/shape_predictor_68_face_landmarks.dat")

predictor = dlib.shape_predictor(PREDICTOR_PATH)
## Face and points detection
def face_points_detection(img, bbox:dlib.rectangle):
    # Get the landmarks/parts for the face in box d.
    shape = predictor(img, bbox)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    coords = np.asarray(list([p.x, p.y] for p in shape.parts()), dtype=np.int)

    # return the array of (x, y)-coordinates
    return coords
