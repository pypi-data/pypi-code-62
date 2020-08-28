# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: model.py
@time: 2019/12/19 17:12

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf

_DEFAULT_WEIGHTS = "best.th"


class Model(tf.keras.Model):
    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

    def call(self, inputs, training=None, mask=None):
        raise NotImplementedError
