"""
视觉工具
@author HeTongHao
@since 2020/5/11 11:50
"""
import math
import cv2
import numpy as np


def show_imgs(*imgs):
    if isinstance(imgs[0], list):
        imgs = imgs[0]
    i = 0
    for img in imgs:
        img = revision_img_size(img, 0.5, 0.5)
        i = i + 1
        cv2.imshow("showImg-%s" % i, img)
    cv2.waitKey(0)  # 等待用户操作，里面等待参数是毫秒，我们填写0，代表是永远，等待用户操作
    cv2.destroyAllWindows()  # 销毁所有窗口


def revision_img_size(img, width_scale, height_scale):
    """
    按比例调整图片大小
    :param img:
    :param width_scale:
    :param height_scale:
    :return:
    """
    imgInfo = img.shape
    return cv2.resize(img, (int(imgInfo[1] * width_scale), int(imgInfo[0] * height_scale)))


def spin(img, angle, center):
    (h, w) = img.shape[:2]

    m = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = np.abs(m[0, 0])
    sin = np.abs(m[0, 1])

    # 高勾
    tick_off = (h * sin)
    # 宽勾
    tick_off_w = (w * sin)

    # 计算新中心点坐标
    # 重新设置矩形坐上顶点的坐标
    if angle > 0:
        new_center = (int(center[0] - m[0, 2]), int(center[1] + tick_off_w - m[1, 2]))
        m[0, 2] = 0
        m[1, 2] = int(w * sin)
    else:
        new_center = (int(center[0] + tick_off - m[0, 2]), int(center[1] - m[1, 2]))
        m[0, 2] = int(tick_off)
        m[1, 2] = 0
    # 执行实际旋转，并用外接矩形（新高宽）生成新图
    n_w = int(tick_off + (w * cos))
    n_h = int((h * cos) + tick_off_w)
    return cv2.warpAffine(img, m, (n_w, n_h)), new_center


def get_mask(src, hue, sensitivity):
    """
    获取遮罩
    :param src: 图片
    :param hue: 色相
    :param sensitivity: 色相上下范围
    :return:
    """
    min_hue = 0
    max_hue = 179
    lower_hue = hue - sensitivity
    upper_hue = hue + sensitivity
    if lower_hue >= min_hue and upper_hue <= max_hue:
        return cv2.inRange(src, np.array([lower_hue, 100, 100]), np.array([upper_hue, 255, 255]))
    else:
        lower_color_0 = None
        upper_color_0 = np.array([max_hue, 255, 255])
        lower_color_1 = np.array([min_hue, 100, 100])
        upper_color_1 = None
        if lower_hue < min_hue:
            lower_color_0 = np.array([max_hue + lower_hue, 100, 100])
            upper_color_1 = np.array([upper_hue, 255, 255])
        elif upper_hue > max_hue:
            lower_color_0 = np.array([lower_hue, 100, 100])
            upper_color_1 = np.array([min_hue + (upper_hue - max_hue), 255, 255])
        # 获取两个区间的遮罩合并
        return cv2.bitwise_or(cv2.inRange(src, lower_color_0, upper_color_0)
                              , cv2.inRange(src, lower_color_1, upper_color_1))


def distance(index1, index2):
    """
    计算两个坐标的直线距离
    :param index1:
    :param index2:
    :return:
    """
    return math.sqrt(math.pow(index1[0] - index2[0], 2) + math.pow(index1[1] - index2[1], 2))


def put_text(img, text, index, font_size=1, color=(0, 0, 255), thickness=1):
    cv2.putText(img, text, index, cv2.FONT_HERSHEY_SIMPLEX, font_size, color, thickness)


class CircumscribedRectangle:
    def __init__(self, contour):
        circumscribed_rectangle = cv2.minAreaRect(contour)
        self.center_index = tuple(map(lambda v: int(v), circumscribed_rectangle[0]))
        self.width = int(circumscribed_rectangle[1][0])
        self.height = int(circumscribed_rectangle[1][1])
        width_half = int(self.width / 2)
        height_half = int(self.height / 2)
        # 左上角坐标
        self.upper_left_corner_index = self.center_index[0] - width_half, self.center_index[1] - height_half
        # 右下角坐标
        self.down_right_corner_index = self.center_index[0] + width_half, self.center_index[1] + height_half


if __name__ == '__main__':
    distance((1, 2), (4, 2))
