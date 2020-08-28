# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: simple_text_classifier.py
@time: 2019/12/21 10:46

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf

from leslie.models.model import Model


class AverPoolingTextClassifierModel(Model):
    def __init__(self, vocab_size, embed_size):
        super(AverPoolingTextClassifierModel, self).__init__()
        self.embedding = tf.keras.layers.Embedding(vocab_size, embed_size, trainable=True)
        self.average = tf.keras.layers.GlobalAveragePooling1D()
        self.d1 = tf.keras.layers.Dense(64, activation='relu')
        self.d2 = tf.keras.layers.Dense(4, activation='softmax')

    def call(self, inputs, training=None, mask=None):
        x = self.embedding(inputs)
        x = self.average(x)
        x = self.d1(x)
        x = self.d2(x)
        return x
