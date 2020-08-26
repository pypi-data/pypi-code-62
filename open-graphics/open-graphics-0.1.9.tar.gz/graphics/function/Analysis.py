import os
import shutil

import cv2
import numpy as np
from ..common.logs import logs
from .Format import get_file_md5

__all__ = ["delete_file",
           "extract_frames"]


def delete_file(src, dst="../"):
    all_md5 = {}
    dirs = os.listdir(src)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    for p in dirs:
        md5 = get_file_md5(os.path.join(src, p))
        if md5 in all_md5.values():
            shutil.move(os.path.join(src, p), os.path.join(dst, p))
            logs.info(os.path.join(src, p))
        else:
            all_md5[p] = md5


def extract_frames(path, threshold=30.0):
    """
    提取视频关键帧
    :param path: the video path
    :param threshold: the threshold of two frames`s pixel diff
    :return: [frame for (idx, frame) in key_frames.items()]
    """
    idx, key_frames, prev_frame = 0, {}, None
    try:
        video_capture = cv2.VideoCapture(path)
        success, frame = video_capture.read()
        height, width = frame.shape[:2]
        key_frames[idx] = frame[:, :, ::-1]
        idx += 1
        while success:
            curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            if curr_frame is not None and prev_frame is not None:
                diff = cv2.absdiff(curr_frame, prev_frame)
                diff_sum_mean = np.sum(diff) / (width * height)
                if diff_sum_mean > threshold:
                    key_frames[idx] = frame[:, :, ::-1]
            idx += 1
            prev_frame = curr_frame
            success, frame = video_capture.read()
        video_capture.release()
    except ValueError:
        pass

    return key_frames
