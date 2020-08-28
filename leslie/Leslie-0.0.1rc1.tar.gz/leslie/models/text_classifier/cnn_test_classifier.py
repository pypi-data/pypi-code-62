# _*_ coding:utf-8 _*_
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file cnn_test_classifier.py
@time  22:17
这一行开始写文本解释与说明

"""
import tensorflow as tf

from leslie.models.model import Model


class CnnModel(Model):
    def __init__(self):
        super(CnnModel, self).__init__()
        self.embedding = tf.keras.layers.Embedding(3000, 512)
        self.conv_1 = tf.keras.layers.Conv1D(16, kernel_size=5, name="conv_1", activation="relu")
        # self.pool = tf.keras.layers.MaxPool1D()
        # self.conv_2 = tf.keras.layers.Conv1D(128, kernel_size=2, name="conv_2", activation="relu")
        self.flatten = tf.keras.layers.GlobalAveragePooling1D()
        self.dense = tf.keras.layers.Dense(4, activation='softmax')

    def call(self, inputs, training=None, mask=None):
        x = self.embedding(inputs)
        x = self.conv_1(x)
        # x = self.pool(x)
        # x = self.conv_2(x)
        # x = self.pool(x)
        x = self.flatten(x)
        x = self.dense(x)
        return x
