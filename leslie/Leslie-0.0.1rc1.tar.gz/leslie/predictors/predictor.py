# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com
@version: 1.0

@file: predictor.py 
@time: 2020/7/16 上午12:03

这一行开始写关于本文件的说明与解释

"""
# import tensorflow as tf
# import codecs
# import os
#
#
# class TextBiClassifierPredictor(object):
#     """
#     classifier model predictor
#     """
#
#     def __init__(self, serialization_dir: str, is_padded: bool = True, oov_token: str = "@@UNKNOWN@@",
#                  namespace: str = "tokens"):
#         """
#
#         :param serialization_dir:
#         """
#         self.model = tf.keras.models.load_model(serialization_dir)
#         self._token_to_index = {}
#         self._index_to_token = {}
#         file_name = os.path.join(serialization_dir, "")
#         with codecs.open(filename, "r", "utf-8") as input_file:
#             lines = input_file.read().split("\n")
#             # Be flexible about having final newline or not
#             if lines and lines[-1] == "":
#                 lines = lines[:-1]
#             for i, line in enumerate(lines):
#                 index = i + 1 if is_padded else i
#                 token = line.replace("@@NEWLINE@@", "\n")
#                 self._token_to_index[token] = index
#                 self._index_to_token[index] = token
#
#     def _encode(self, query):
#         """
#         query -> encode_query
#         :param query:
#         :return:
#         """
#         encode_query = [self.word_index.get(w, self.word_index["<UNK>"]) for w in query]
#         return encode_query
#
#     def predict(self, query):
#         """
#         单query predict
#         :param query:
#         :return:
#         """
#         encode_query = self._encode(query=query)
#         encode_query_to_idx = tf.keras.preprocessing.sequence.pad_sequences(
#             [encode_query],
#             padding="post",
#             value=self.word_index["<PAD>"],
#             maxlen=self.max_seq_length
#         )
#         result = self.model.predict(encode_query_to_idx)
#         return result
#
#     def batch_predict(self, query_list):
#         """
#         query batch predict
#         :param query_list:
#         :return:
#         """
#         encode_query_list = [self._encode(query) for query in query_list]
#         encode_query_list_to_idx = tf.keras.preprocessing.sequence.pad_sequences(
#             encode_query_list,
#             padding="post",
#             value=self.word_index["<PAD>"],
#             maxlen=self.max_seq_length
#         )
#         result = self.model.predict(encode_query_list_to_idx)
#         return result
