import numpy as np


def filter_bbox_by_roi(boxes, pt1=(0, 0), pt2=(1, 1)):
    boxes = np.array(boxes)
    mask = (boxes > pt1 * 2) & (boxes < pt2 * 2)
    mask = mask.all(1)
    return boxes[mask]


def filter_bbox_by_area(boxes, area_range):
    boxes = np.array(boxes)

    pt1 = boxes[:, :2]
    pt2 = boxes[:, 2:]

    area = (pt2 - pt1).prod(1)
    mask = (area > area_range[0]) & (area < area_range[1])
    return boxes[mask]


def filter_bbox_by_score(boxes, scores, min_score=0.5):
    boxes = np.array(boxes)
    mask = scores > min_score
    return boxes[mask]
