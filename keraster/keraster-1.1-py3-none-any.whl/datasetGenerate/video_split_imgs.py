"""
@author HeTongHao
@since 2020/7/27 17:02
"""
import cv2
from datetime import datetime
import os
from tools import os_tools

# 图片输出路径
OUTPUT_PATH = 'facade'
# 读取毫秒间隔
READ_INTERVAL_MS = 100


def current_time_str():
    """
    获取当前时间字符串
    :return:
    """
    return datetime.now().strftime('%Y-%m-%d_%H_%M_%S')[:-3]


os_tools.ensure_path_exists(OUTPUT_PATH)
print('图片输出路径:', OUTPUT_PATH)
video_path = input('请输入视频地址:')
print(video_path)
cap = cv2.VideoCapture(video_path)  # 创建一个视频获取对象
flag = 0  # 用于指定帧的序号
fr = 1
time = 0  # 用于指定帧的时长
img_prefix = current_time_str()
while cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_MSEC, time)
    # cap.set(cv2.CAP_PROP_POS_FRAMES,flag) #设置帧数标记
    ret, im = cap.read()  # 获取图像
    if not ret:  # 如果获取失败，则结束
        print("exit")
        break
    # cv2.waitKey(100)#延时
    # cv2.imshow('a',im)#显示图像，用在循环中可以播放视频
    imgOutputPath = os.path.join(OUTPUT_PATH, '{0}__{1:05d}.jpg'.format(img_prefix, fr))
    print('img output path:', imgOutputPath)
    cv2.imwrite(imgOutputPath, im)  # 保存图片
    time += READ_INTERVAL_MS  # 设置每隔ms读取帧
    # flag+=10  #每隔10帧读取一帧
    fr += 1
