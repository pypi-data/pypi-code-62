import tensorflow as tf
from tensorflow.keras import layers


@tf.keras.utils.register_keras_serializable(package="Axion")
class Unpooling2D(layers.Layer):
    def __init__(
        self, **kwargs,
    ):
        super().__init__(**kwargs)

    def build(self, input_shape):
        unused_N, C, H, W = input_shape
        # use static shape inference
        # because using shape in eager execution will get errors
        self.origin_shape = H, W
        self.target_shape = H * 2, W * 2
        self.channels = C
        w = tf.constant([[1.0, 0.0], [0.0, 0.0]])
        w = tf.tile(tf.reshape(w, (2, 2, 1, 1)), [1, 1, C, C])
        I = tf.tile(tf.reshape(tf.eye(C), (1, 1, C, C)), [2, 2, 1, 1])
        self.w = w * I

    def call(self, inputs):
        x = tf.nn.conv2d_transpose(
            input=inputs,
            filters=self.w,  # h,w,oc,ic
            output_shape=(tf.shape(inputs)[0], self.channels) + self.target_shape,
            data_format="NCHW",
            strides=2,
            padding="VALID",
        )
        return x

    def get_config(self):
        config = super().get_config()
        return config

    def get_bitmeta(self):
        return {
            "name": self.name,
            "type": "unpool",
            "input": [],
            "compnode": "npu",
        }
