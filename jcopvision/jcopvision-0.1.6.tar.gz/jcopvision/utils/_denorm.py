import numpy as np


def denorm_bbox(frame, boxes, to_int=True):
    """
    boxes: (N, 4)
        bounding box normalized coordinate (x1, y1, x2, y2)
    """
    h, w, c = frame.shape
    boxes = np.array(boxes).clip(0, 1)
    boxes = boxes * [w, h, w, h]
    if to_int:
        boxes = boxes.astype(int)
    return boxes


def denorm_point(frame, points, to_int=True):
    """
    points: (N, 2)
        points normalized coordinate (x, y)
    """
    h, w, c = frame.shape
    points = np.array(points).clip(0, 1)
    points = points * [w, h]
    if to_int:
        points = points.astype(int)
    return points


def denorm_landmark(frame, box, points, to_int=True):
    """
    box: (1, 4) or (4,)
        bounding box normalized coordinate (x1, y1, x2, y2) that contains points

    points: (N, 2)
        points coordinate normalized towards the bounding box
    """
    x1, y1, x2, y2 = box
    points = points * [x2 - x1, y2 - y1] + [x1, y1]
    points = denorm_point(frame, points, to_int)
    return points


def denorm_pixel(frame):
    return (frame * 255).astype(np.uint8)
