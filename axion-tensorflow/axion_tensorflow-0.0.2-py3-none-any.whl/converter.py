import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from axion_tensorflow import layers as qlayers

__all__ = ["Converter"]


class Converter:
    def __init__(self):
        pass

    def convert_keras(self, keras_model, example):
        if isinstance(keras_model, models.Sequential):
            metas = self._convert_keras_sequential(keras_model)
        elif isinstance(keras_model, models.Model):
            metas = self._convert_keras_functional(keras_model)
        else:
            raise ValueError("Unsupported model type: {}".format(type(keras_model)))

        # Remove unpool opr from metas.
        for i in reversed(range(len(metas))):
            if metas[i]["type"] == "unpool":
                metas.pop(i)
        if "compnode" in metas[-1] and metas[-1]["compnode"] == "npu":
            metas[-1]["compnode"] = "cpu"
        self.fill_output(metas, example)
        metas = self.int_bittype_to_str_bittype(metas)
        metas = self.postprocess_mode_convert(metas)
        return metas

    def fill_output(self, metas, example):
        md = {l["name"]: l for l in metas}
        inputs = [l["output_tensor"] for l in metas if l["type"] == "data"]
        if len(inputs) != 1:
            raise ValueError("Unsupported number of inputs: {}.".format(len(inputs)))
        outputs = {l["name"]: l["output_tensor"] for l in metas}
        f = tf.keras.backend.function(inputs=inputs, outputs=outputs)
        output_values = f(example)
        for k, v in output_values.items():
            md[k]["output"] = v
        for l in metas:
            l.pop("output_tensor")

    def _convert_keras_sequential(self, sequential_model):
        metas = []
        last_layer = None
        last_non_unpool_layer = None
        last_meta = None

        default_input = "input"

        metas.append(
            {
                "name": default_input,
                "type": "data",
                # input is in [0; 1], set data_ratio to 255 to scale to [0; 255].
                "data_ratio": 255,
                "of_bit": 8,
                "output_tensor": sequential_model.input,
            }
        )

        for l in sequential_model.layers:
            if hasattr(l, "get_bitmeta"):
                m = l.get_bitmeta()
                m["output_tensor"] = l.output
                if last_layer is not None:
                    # layer_name, is_unpool
                    if isinstance(last_layer, qlayers.Unpooling2D):
                        m["input"].append((last_non_unpool_layer.name, True))
                    else:
                        m["input"].append((last_layer.name, False))
                else:
                    m["input"].append((default_input, False))
                metas.append(m)
                last_layer = l
                if not isinstance(l, qlayers.Unpooling2D):
                    last_non_unpool_layer = l
                last_meta = m
            elif isinstance(l, layers.InputLayer):
                raise ValueError("InputLayer is not supported in sequential model.")
            else:
                fuse_meta(last_meta, l)

        last_bits = None
        for m in metas:
            m["if_bit"] = last_bits
            if m.get("of_bit", None) is None:
                m["of_bit"] = m["if_bit"]
            last_bits = m["of_bit"]
        return metas

    def _convert_keras_functional(self, functional_model):
        metas = {}

        for l in functional_model.layers:
            if hasattr(l, "get_bitmeta"):
                m = l.get_bitmeta()
                m["output_tensor"] = l.output
                metas[m["name"]] = m
            elif isinstance(l, layers.InputLayer):
                m = {
                    "name": l.name,
                    "type": "data",
                    # input is in [0; 1], set data_ratio to 255 to scale to [0; 255].
                    "data_ratio": 255,
                    "of_bit": 8,
                    "output_tensor": l.output,
                }
                metas[m["name"]] = m

        # This is needed for nested concatenate.
        # l is axion layer or Concat
        def fill_input(metas, l, input, if_bit):
            if isinstance(l, layers.Concatenate):
                if l.axis != 1:
                    raise ValueError(
                        "Unsupported concatenate axis: {}, should be 1.".format(l.axis)
                    )
                for n in l.outbound_nodes:
                    fill_input(metas, n.outbound_layer, input, if_bit)
            else:
                m = metas.get(l.name)
                if m is None:
                    raise ValueError(
                        "Invalid network: {} should be a axion layer.".format(l.name)
                    )
                m["input"].append(input)
                if m.get("if_bit") is None:
                    m["if_bit"] = if_bit
                elif m["if_bit"] != if_bit:
                    raise ValueError("if_bit mismatch for {}".format(l.name))

        def try_fuse(metas, current_meta, current_layer):
            if current_meta.get("of_bit", None) is None:
                # Inference `of_bit` from `if_bit`.
                # If `if_bit` not set, use `of_bit` from opr in input.
                if current_meta.get("if_bit", None) is None:
                    assert len(current_meta["input"]) == 1
                    owner_opr_name = current_meta["input"][0][0]
                    owner_opr = metas[owner_opr_name]
                    current_meta["of_bit"] = current_meta["if_bit"] = owner_opr[
                        "of_bit"
                    ]
                else:
                    current_meta["of_bit"] = current_meta["if_bit"]
            num_outs = len(current_layer.outbound_nodes)
            if num_outs == 0:
                return
            if isinstance(current_layer, qlayers.unpooling.Unpooling2D):
                input_to_fill = (current_meta["input"][0][0], True)
            else:
                input_to_fill = (current_meta["name"], False)

            if num_outs > 1:
                for n in current_layer.outbound_nodes:
                    fill_input(
                        metas=metas,
                        l=n.outbound_layer,
                        input=input_to_fill,
                        if_bit=current_meta["of_bit"],
                    )
                return
            outbound_layer = current_layer.outbound_nodes[0].outbound_layer
            if isinstance(outbound_layer, layers.Concatenate) or (
                metas.get(outbound_layer.name) is not None
            ):
                fill_input(
                    metas=metas,
                    l=outbound_layer,
                    input=input_to_fill,
                    if_bit=current_meta["of_bit"],
                )
                return
            # outbound_layer is not axion layer nor Concat
            fuse_meta(current_meta, outbound_layer)
            try_fuse(metas, current_meta, outbound_layer)

        for name, meta in metas.items():
            l = functional_model.get_layer(name)
            try_fuse(metas, meta, l)

        metas = list(metas.values())
        return metas

    # (bits, is_logic, is_signed, name)
    def int_bittype_to_str_bittype(self, metas):
        def int_to_str(data):
            if data == 0:
                data = 16
            return "logic_uint" + str(data)

        for m in metas:
            for bit_to_change in ["if_bit", "of_bit", "w_bit"]:
                if m.get(bit_to_change, None) is not None:
                    m[bit_to_change] = (
                        16 if m[bit_to_change] == 0 else m[bit_to_change],
                        True,
                        False,
                        int_to_str(m[bit_to_change]),
                    )
        return metas

    def postprocess_mode_convert(self, metas):
        def convert_postprocess_mode_to_integer(postprocess_mode):
            assert postprocess_mode in ["normal", "direct", "affine"]
            return {"normal": 0, "direct": 2, "affine": 3}[postprocess_mode]

        for m in metas:
            if m["type"] in ["conv", "dense", "local_conv"]:
                if m["of_bit"] == 0:
                    m["of_bit"] = 16
                    m["postprocess_mode"] = convert_postprocess_mode_to_integer(
                        "affine"
                    )
                else:
                    m["postprocess_mode"] = convert_postprocess_mode_to_integer(
                        "normal"
                    )
        return metas


def fuse_meta(meta, l: layers.Layer):
    if isinstance(l, qlayers.Activation):
        meta["of_bit"] = l.activation_bits
        # y = multiplier * (gamma * x + beta)
        # => y = multiplier * (gamma * (k * x + b) + beta)
        # => k' = k * gamma * multiplier, b' = b * multiplier * gamma + beta * multiplier
        meta["affine_k"] *= l.gamma.numpy() * l.multiplier
        meta["affine_b"] = (
            meta["affine_b"] * l.gamma.numpy() * l.multiplier
            + l.beta.numpy() * l.multiplier
        )
    elif isinstance(l, tf.python.keras.layers.normalization.BatchNormalizationBase):
        # y = (x - mean) * tf.rsqrt(variance + eps)
        # => y = (k * x + b - mean) * tf.rsqrt(variance + eps)
        # => k' = k * tf.rsqrt(variance + eps), b' = (b - mean) * tf.rsqrt(variance + eps)
        inv_stddev = tf.math.rsqrt(l.moving_variance + l.epsilon).numpy()
        meta["affine_k"] *= inv_stddev
        meta["affine_b"] = (meta["affine_b"] - l.moving_mean.numpy()) * inv_stddev
        if l.center or l.scale:
            raise ValueError("BatchNormalization should not enable center or scale.")
    elif isinstance(l, layers.MaxPooling2D):
        if meta is None or meta["type"] != "conv":
            raise ValueError(
                "MaxPooling2D is only supported when immediately after a Conv2D layer."
            )
        ph, pw = l.pool_size
        if ph != pw:
            raise ValueError(
                "MaxPooling2D must have the same pool_size on both dimensions."
            )
        if l.pool_size != l.strides:
            raise ValueError("MaxPooling2D must have the same pool_size and strides.")
        meta["pooling"] = ph, pw
    elif isinstance(l, layers.Flatten):
        return
    elif isinstance(l, qlayers.unpooling.Unpooling2D):
        return
    else:
        raise ValueError("Unsupported layer: {}".format(l.name))
    # Update output tensor.
    meta["output_tensor"] = l.output
