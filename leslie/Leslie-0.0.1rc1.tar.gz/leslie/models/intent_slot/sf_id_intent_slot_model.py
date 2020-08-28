# -*- coding: utf-8 -*-
"""
@author: kebo
@contact: kebo0912@outlook.com

@version: 1.0
@file: sf_id_intent_slot_model.py
@time: 2020/3/13 15:34

这一行开始写关于本文件的说明与解释


"""
import tensorflow as tf

from leslie.models.model import Model

gpu = tf.config.list_physical_devices('GPU')  # tf2.1版本该函数不再是experimental
print(gpu)  # 前面限定了只使用GPU1(索引是从0开始的,本机有2张RTX2080显卡)
tf.config.experimental.set_memory_growth(gpu[0], True)  # 其实gpus本身就只有一个元素


class SfIdIntentSlotModel(Model):
    def __init__(self,
                 vocab_size,
                 max_seq_length,
                 embedding_size,
                 hidden_size,
                 intent_size,
                 slot_size,
                 use_crf,
                 priority_order="intent_first"):
        super(SfIdIntentSlotModel, self).__init__()
        self.vocab_size = vocab_size
        self.max_seq_length = max_seq_length
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.intent_size = intent_size
        self.slot_size = slot_size
        self.use_crf = use_crf
        self.priority_order = priority_order

    def call(self, inputs, training=None, mask=None):
        embedded = tf.keras.layers.Embedding(self.vocab_size, self.embedding_size)(inputs)
        # print(embedded.numpy())
        state_outputs, forward_h, forward_c, backward_h, backward_c = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(units=self.hidden_size, return_sequences=True, return_state=True))(embedded)
        # state_outputs 层返回序列结果  (b, s, 2*e); forward_h (b, e)； forward_c (b, e); backward_h  (b, e); backward_c (b, e)
        final_state = tf.concat(values=[forward_h, forward_c, backward_h, backward_c], axis=1)  # [b, 4*e]
        state_shape = state_outputs.get_shape()  # [b, s, 2*e]
        #   ##calculate slot attention
        with tf.name_scope(name="slot_attention"):
            slot_inputs = state_outputs  # [b, s, 2*e]
            attn_size = state_shape[2]  # [2*e]
            origin_shape = tf.shape(state_outputs)  # [b, s, 2*e]
            hidden = tf.expand_dims(state_outputs, 1)  # [b, 1, s, 2*e]
            hidden_convolution = tf.expand_dims(state_outputs, 2)  # [b, s, 1, 2*e]
            k = tf.Variable(name="AttnW",
                            initial_value=tf.initializers.GlorotNormal()(shape=[1, 1, attn_size, attn_size]))
            # [1, 1, 2*e, 2*e]
            hidden_features = tf.nn.conv2d(input=hidden_convolution, filters=k, strides=[1, 1, 1, 1], padding="SAME")
            # [b, s, 1, 2*e]
            hidden_features = tf.reshape(hidden_features, origin_shape)  # [b, s, 2*e]
            hidden_features = tf.expand_dims(hidden_features, 1)  # [b, 1, s, 2*e]
            v = tf.Variable(name="AttnV", initial_value=tf.initializers.GlorotNormal()(shape=[attn_size]))  # [2*e]
            slot_inputs_shape = tf.shape(slot_inputs)  # [b, s, 2*e]
            slot_inputs = tf.reshape(slot_inputs, [-1, attn_size])  # [b*s, 2*e]
            y = tf.keras.layers.Dense(units=attn_size, use_bias=True)(slot_inputs)  # [b*s, 2*e]
            y = tf.reshape(y, slot_inputs_shape)  # [b, s, 2*e]
            y = tf.expand_dims(y, 2)  # [b, s, 1, 2*e]
            s = tf.reduce_sum(v * tf.tanh(hidden_features + y), axis=3)  # [b, s, s]  相加的时候会自动使用广播机制
            a = tf.nn.softmax(s)  # [b, s, s]
            a = tf.expand_dims(a, -1)  # [b, s, s, 1]
            slot_d = tf.reduce_sum(a * hidden, axis=2)  # [b, s, 2*e]
            slot_reinforce_state = tf.expand_dims(slot_d, axis=2)  # [b, s, 1, 2*e]

        #  ##calculate intent attention
        with tf.name_scope(name="intent_attention"):
            intent_input = final_state  # [b, 4*e]
            attn_size = state_shape[2]  # [2*e]
            hidden = tf.expand_dims(state_outputs, 2)  # [b, s, 1, 2*e]
            k = tf.Variable(name="AttnW",
                            initial_value=tf.initializers.GlorotNormal()(shape=[1, 1, attn_size, attn_size]))
            # [1, 1, 2*e, 2*e]
            hidden_features = tf.nn.conv2d(input=hidden, filters=k, strides=[1, 1, 1, 1], padding="SAME")
            # [b, s, 1, 2*e]
            v = tf.Variable(name="AttnV", initial_value=tf.initializers.GlorotNormal()(shape=[attn_size]))  # [2*e]
            y = tf.keras.layers.Dense(units=attn_size, use_bias=True)(intent_input)  # [b, 2*e]
            y = tf.reshape(y, [-1, 1, 1, attn_size])  # [b, 1, 1, 2*e]
            s = tf.reduce_sum(v * tf.tanh(hidden_features + y), axis=[2, 3])  # [b, s]
            a = tf.nn.softmax(s)  # [b, s]
            a = tf.expand_dims(a, axis=-1)  # [b, s, 1]
            a = tf.expand_dims(a, axis=-1)  # [b, s, 1, 1]
            r_intent = tf.reduce_sum(a * hidden, axis=[1, 2])  # [b, 2*e]
            intent_context_states = r_intent  # [b, 2*e]

        if self.priority_order == "intent_first":
            with tf.name_scope(name="intent_subnet"):
                attn_size = state_shape[2]  # [2*e]
                hidden = tf.expand_dims(state_outputs, axis=2)  # [b, s, 1, 2*e]
                k1 = tf.Variable(name="W1",
                                 initial_value=tf.initializers.GlorotNormal()(shape=[1, 1, attn_size, attn_size]))
                # [1, 1, 2*e, 2*e]
                k2 = tf.Variable(name="W2",
                                 initial_value=tf.initializers.GlorotNormal()(shape=[1, 1, attn_size, attn_size]))
                # [1, 1, 2*e, 2*e]
                slot_reinforce_features = tf.nn.conv2d(slot_reinforce_state, filters=k1, strides=[1, 1, 1, 1],
                                                       padding="SAME")
                # [b, s, 1, 2*e]
                hidden_features = tf.nn.conv2d(hidden, filters=k2, strides=[1, 1, 1, 1],
                                               padding="SAME")  # [b, s, 1, 2*e]
                v1 = tf.Variable(name="AttnV", initial_value=tf.initializers.GlorotNormal()(shape=[attn_size]))
                # [s*e]
                bias = tf.Variable(name="Bias", initial_value=tf.initializers.GlorotNormal()(shape=[attn_size]))
                # [2*e]
                s = tf.reduce_sum(v1 * tf.tanh(hidden_features + slot_reinforce_features + bias),
                                  axis=[2, 3])  # [b, s, 1, 2*e]
                a = tf.nn.softmax(s)  # [b, s]
                a = tf.expand_dims(a, axis=-1)  # [b, s, 1]
                a = tf.expand_dims(a, axis=-1)  # [b, s, 1, 1]
                r = tf.reduce_sum(a * slot_reinforce_state, axis=[1, 2])  # [b, 2*e]
                r_intent = r + intent_context_states  # [b, 2*e]
                intent_output = tf.concat([r_intent, intent_input], 1)  # [b, 6*e]

            with tf.name_scope(name="slot_subnet"):
                intent_gate = tf.keras.layers.Dense(units=attn_size, use_bias=True)(r_intent)  # [b, 2*e]
                intent_gate = tf.reshape(intent_gate, [-1, 1, intent_gate.get_shape()[1]])  # [b, 1, 2*e]
                v1 = tf.Variable(name="gateV", initial_value=tf.initializers.GlorotNormal()(shape=[attn_size]))
                # [2*e]
                relation_factor = v1 * tf.tanh(slot_d + intent_gate)  # [b, s, 2*e]
                relation_factor = tf.reduce_sum(relation_factor, axis=2)  # [b, s]
                relation_factor = tf.expand_dims(relation_factor, axis=-1)  # [b, s, 1]
                slot_reinforce_state1 = slot_d + relation_factor  # [b, s, 2*e]
                slot_reinforce_state = tf.expand_dims(slot_reinforce_state1, axis=2)  # [b, s, 2*e, 1]
                slot_reinforce_vector = tf.reshape(slot_reinforce_state1, [-1, attn_size])  # [b*s, 2*e]
                slot_output = tf.concat([slot_reinforce_vector, slot_inputs], 1)  # [b*s, 4*e]
        with tf.name_scope('intent_part'):
            intent = tf.keras.layers.Dense(units=self.intent_size, use_bias=True)(intent_output)
        with tf.name_scope('slot_part'):
            slot = tf.keras.layers.Dense(units=self.slot_size, use_bias=True)(slot_output)
            if self.use_crf:
                slot = tf.reshape(slot, [-1, origin_shape[1], self.slot_size])
        outputs = [slot, intent]
        return outputs

    def train(self):
        pass


if __name__ == '__main__':
    model = SfIdIntentSlotModel(vocab_size=1000, max_seq_length=32, embedding_size=200, hidden_size=200, intent_size=3,
                                slot_size=8, use_crf=True)
    res = model(inputs=tf.constant([[1, 2, 3], [4, 5, 6]]))
    print(res)
