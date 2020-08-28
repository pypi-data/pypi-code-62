# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: text_classifier_model.py
@time: 2019/11/25 16:24

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf
import numpy as np


class TextClassifierModel(object):
    """
    文本分类模型基类
    """

    def __init__(self,
                 training_data,
                 training_labels,
                 val_data,
                 val_labels,
                 word_index,
                 model_path,
                 max_seq_length=64,
                 epochs=30,
                 batch_size=64,
                 use_pretrained=False,
                 pretrained_file=None,
                 save_best_only=True,
                 save_weights_only=False,
                 monitor="val_acc",
                 verbose=1):
        self.training_data = training_data
        self.training_labels = training_labels
        self.val_data = val_data
        self.val_labels = val_labels
        self.word_index = word_index
        self.model_path = model_path
        self.max_seq_length = max_seq_length
        self.epochs = epochs
        self.batch_size = batch_size
        self.save_best_only = save_best_only
        self.save_weights_only = save_weights_only
        self.monitor = monitor
        self.verbose = verbose
        self.use_pretrained = use_pretrained
        self.pretrained_file = pretrained_file

    def create_model(self):
        raise NotImplementedError

    def _encode_and_pad(self):
        self.training_data = tf.keras.preprocessing.sequence.pad_sequences(
            [[self.word_index.get(w, self.word_index["<UNK>"]) for w in line] for line in self.training_data],
            padding='post',
            maxlen=self.max_seq_length, value=self.word_index["<PAD>"]
        )
        self.training_labels = np.asarray(self.training_labels)
        self.val_data = tf.keras.preprocessing.sequence.pad_sequences(
            [[self.word_index.get(w, self.word_index["<UNK>"]) for w in line] for line in self.val_data],
            padding='post',
            maxlen=self.max_seq_length,
            value=self.word_index["<PAD>"]
        )
        self.val_labels = np.asarray(self.val_labels)

    def train(self):
        model = self.create_model()
        model.summary()
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=self.model_path,
            save_best_only=self.save_best_only,
            save_weights_only=self.save_weights_only,
            monitor=self.monitor
        )
        self._encode_and_pad()  # 原始数据encode用于输入后续模型
        model.fit(self.training_data,
                  self.training_labels,
                  validation_data=(self.val_data, self.val_labels),
                  epochs=self.epochs,
                  batch_size=self.batch_size,
                  verbose=self.verbose,
                  callbacks=[cp_callback]
                  )
