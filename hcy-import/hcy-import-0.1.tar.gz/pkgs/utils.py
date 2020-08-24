# -*- coding: utf-8 -*-
# @Author : Hcyang-NULL
# @Time   : 2020/8/24 5:36 下午
# - - - - - - - - - - -

import sys
import cv2
import json
import pickle
import numpy as np
from os import listdir
from os import system
from os.path import isfile
from os.path import isdir
from os.path import join
from PIL import Image
from random import randint
from random import choice
from random import sample
from matplotlib import pyplot as plt

def fplt(m, name=''):
    if name != '':
        print(f'{name}:')
    plt.imshow(m)
    plt.show()

def mplt(img, mask, name='', alpha=0.5):
    if name != '':
        print(f'{name}:')
    plt.imshow(img)
    plt.imshow(mask, alpha=alpha)
    plt.show()

def rjson(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as r:
        data = json.load(r)
    return data

def wjson(file_path, data, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as w:
        json.dump(data, w)
    return 0

def rpkl(file_path):
    with open(file_path, 'rb') as r:
        data = pickle.load(r)
    return data

def wpkl(file_path, data):
    with open(file_path, 'wb') as w:
        pickle.dump(data, w)
    return 0
