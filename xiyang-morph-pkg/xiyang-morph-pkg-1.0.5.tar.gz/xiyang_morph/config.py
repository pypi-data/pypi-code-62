import cv2
import os

env_dist = os.environ
env_path = env_dist['_'].split("/bin/python")[0]

PREDICTOR_PATH = os.path.join(env_path, "models/shape_predictor_68_face_landmarks.dat")
CASCADE_PATH = os.path.join(env_path,"models/haarcascade_frontalface_default.xml")
OPENCV_OBJECT_TRACKERS = {
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}
