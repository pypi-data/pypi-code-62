import cv2
import numpy as np
from jcopvision.draw._cm import idx2color
from jcopvision.utils import denorm_point
from jcopvision.utils._denorm import denorm_pixel


def draw_bbox(frame, pt1, pt2, color, label=None, conf=None, thickness=1, font=cv2.FONT_HERSHEY_SIMPLEX, fontsize=0.5,
              fontcolor=(0, 0, 0), is_normalized=True):
    '''
    Draw a bounding box with its label


    === Input ===
    frame: array
        image / frame to be drawn

    pt1: (int, int) or (float, float)
        top left point of the bounding box.
        If is_normalized is True, then the point will be rescaled back based on the frame size.

    pt2: (int, int) or (float, float)
        bottom right point of the bounding box
        If is_normalized is True, then the point will be rescaled back based on the frame size.

    color: (int, int, int)
        The bounding box color in BGR format

    label: str
        A text or class label. It will be added to the inner top left of the bounding box

    conf: float
        The prediction confidence

    thickness: int
        The bounding box and text thickness

    font: opencv's font
        The text font. Check for the available font in opencv

    fontsize: float
        The font scaling factor towards the font's base size

    fontcolor: (int, int, int)
        The text font color in BGR format

    is_normalized: bool
        True if using normalized coordinate


    === Return ===
    frame: array
        annotated image / frame
    '''
    frame = frame.copy()
    if frame.dtype == np.float32:
        frame = denorm_pixel(frame)

    if isinstance(color, int):
        color = idx2color(color)

    if is_normalized:
        pt1 = tuple(denorm_point(frame, pt1))
        pt2 = tuple(denorm_point(frame, pt2))

    cv2.rectangle(frame, pt1, pt2, color, thickness)

    if label is not None:
        if conf is not None:
            text = f"{label} [{conf*100:.1f}%]"
        else:
            text = label

        # Handle text size
        (w_text, h_text), baseline = cv2.getTextSize(text, font, fontsize, thickness)

        # Filled textbox
        pt1_box = pt1
        pt2_box = (pt1[0] + w_text + 2 * baseline, pt1[1] + h_text + 2 * baseline)
        cv2.rectangle(frame, pt1_box, pt2_box, color, cv2.FILLED)

        # Add text
        pt_text = (pt1[0] + baseline, pt1[1] + h_text + baseline - thickness)
        cv2.putText(frame, text, pt_text, font, fontsize, fontcolor, thickness)
    return frame
