# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import os

from nvidia.dali.pipeline import Pipeline
import nvidia.dali.ops as ops
import nvidia.dali.types as types
from nvidia.dali.plugin.paddle import DALIGenericIterator

import paddle
from paddle import fluid


def convert_data_layout(data_layout):
    if data_layout == 'NCHW':
        return types.NCHW
    elif data_layout == 'NHWC':
        return types.NHWC
    else:
        assert False, "not supported data_layout:{}".format(data_layout)


class HybridTrainPipe(Pipeline):
    """
    Create train pipe line.  You can find document here:
    https://docs.nvidia.com/deeplearning/sdk/dali-master-branch-user-guide/docs/plugins/paddle_tutorials.html
    Note: You may need to find the newest DALI version.
    """

    def __init__(self,
                 file_root,
                 file_list,
                 batch_size,
                 resize_shorter,
                 crop,
                 min_area,
                 lower,
                 upper,
                 interp,
                 mean,
                 std,
                 device_id,
                 shard_id=0,
                 num_shards=1,
                 random_shuffle=True,
                 num_threads=4,
                 seed=42,
                 data_layout="NCHW"):
        super(HybridTrainPipe, self).__init__(
            batch_size,
            num_threads,
            device_id,
            seed=seed,
            prefetch_queue_depth=8,
            set_affinity=True)
        self.input = ops.FileReader(
            file_root=file_root,
            file_list=file_list,
            shard_id=shard_id,
            num_shards=num_shards,
            random_shuffle=random_shuffle)
        # set internal nvJPEG buffers size to handle full-sized ImageNet images
        # without additional reallocations
        device_memory_padding = 211025920
        host_memory_padding = 140544512
        self.decode = ops.ImageDecoderRandomCrop(
            device='mixed',
            output_type=types.RGB,
            device_memory_padding=device_memory_padding,
            host_memory_padding=host_memory_padding,
            random_aspect_ratio=[lower, upper],
            random_area=[min_area, 1.0],
            num_attempts=100)
        self.res = ops.Resize(
            device='gpu', resize_x=crop, resize_y=crop, interp_type=interp)
        self.cmnp = ops.CropMirrorNormalize(
            device="gpu",
            output_dtype=types.FLOAT,
            output_layout=convert_data_layout(data_layout),
            crop=(crop, crop),
            image_type=types.RGB,
            mean=mean,
            std=std)
        self.coin = ops.CoinFlip(probability=0.5)
        self.to_int64 = ops.Cast(dtype=types.INT64, device="gpu")

    def define_graph(self):
        rng = self.coin()
        jpegs, labels = self.input(name="Reader")
        images = self.decode(jpegs)
        images = self.res(images)
        output = self.cmnp(images.gpu(), mirror=rng)
        return [output, self.to_int64(labels.gpu())]

    def __len__(self):
        return self.epoch_size("Reader")


class HybridValPipe(Pipeline):
    """
    Create validate pipe line.
    """

    def __init__(self,
                 file_root,
                 file_list,
                 batch_size,
                 resize_shorter,
                 crop,
                 interp,
                 mean,
                 std,
                 device_id,
                 shard_id=0,
                 num_shards=1,
                 random_shuffle=False,
                 num_threads=4,
                 seed=42,
                 data_layout='NCHW'):
        super(HybridValPipe, self).__init__(
            batch_size, num_threads, device_id, seed=seed)
        self.input = ops.FileReader(
            file_root=file_root,
            file_list=file_list,
            shard_id=shard_id,
            num_shards=num_shards,
            random_shuffle=random_shuffle)
        self.decode = ops.ImageDecoder(device="mixed", output_type=types.RGB)
        self.res = ops.Resize(
            device="gpu", resize_shorter=resize_shorter, interp_type=interp)
        self.cmnp = ops.CropMirrorNormalize(
            device="gpu",
            output_dtype=types.FLOAT,
            output_layout=convert_data_layout(data_layout),
            crop=(crop, crop),
            image_type=types.RGB,
            mean=mean,
            std=std)
        self.to_int64 = ops.Cast(dtype=types.INT64, device="gpu")

    def define_graph(self):
        jpegs, labels = self.input(name="Reader")
        images = self.decode(jpegs)
        images = self.res(images)
        output = self.cmnp(images)
        return [output, self.to_int64(labels.gpu())]

    def __len__(self):
        return self.epoch_size("Reader")


def build(filelist,
          batch_size,
          image_mean,
          image_std,
          resize_short_size,
          lower_scale,
          lower_ratio,
          upper_ratio,
          mode='train',
          trainer_id=None,
          trainers_num=None,
          gpu_id=0,
          data_layout='NCHW'):
    env = os.environ
    #assert settings.use_gpu, "gpu training is required for DALI"
    #assert not settings.use_mixup, "mixup is not supported by DALI reader"
    #assert not settings.use_aa, "auto augment is not supported by DALI reader"
    assert float(env.get('FLAGS_fraction_of_gpu_memory_to_use', 0.92)) < 0.9, \
        "Please leave enough GPU memory for DALI workspace, e.g., by setting" \
        " `export FLAGS_fraction_of_gpu_memory_to_use=0.8`"

    a = open(filelist, 'r')
    str = a.read()

    str = str.replace('JPEG', 'jpeg')
    b = open(filelist, 'w')
    b.write(str)
    b.close()
    for i in range(len(filelist)):
        if filelist[-i] == '/':
            file_root = filelist[:-i]
            break
    batch_size = batch_size

    mean = [v * 255 for v in image_mean]
    std = [v * 255 for v in image_std]
    image_shape = [3, 224, 224]
    crop = image_shape[1]
    resize_shorter = resize_short_size
    min_area = lower_scale
    lower = lower_ratio
    upper = upper_ratio

    interp = 1  # default to linear
    interp_map = {
        0: types.INTERP_NN,  # cv2.INTER_NEAREST
        1: types.INTERP_LINEAR,  # cv2.INTER_LINEAR
        2: types.INTERP_CUBIC,  # cv2.INTER_CUBIC
        4: types.INTERP_LANCZOS3,  # XXX use LANCZOS3 for cv2.INTER_LANCZOS4
    }
    assert interp in interp_map, "interpolation method not supported by DALI"
    interp = interp_map[interp]

    if mode != 'train':
        if not os.path.exists(filelist):
            file_list = None
            file_root = os.path.join(file_root, 'val')
        pipe = HybridValPipe(
            file_root,
            filelist,
            batch_size,
            resize_shorter,
            crop,
            interp,
            mean,
            std,
            device_id=gpu_id,
            data_layout=data_layout)
        pipe.build()
        return DALIGenericIterator(
            pipe, ['feed_image', 'feed_label'],
            size=len(pipe),
            dynamic_shape=True,
            fill_last_batch=True,
            last_batch_padded=True)

    file_root = os.path.join(file_root, 'train')

    if trainer_id is not None and trainers_num is not None:
        print("dali gpu_id:", gpu_id, "shard_id:", trainer_id, "num_shard:",
              trainers_num)
        shard_id = trainer_id
        num_shards = trainers_num
        pipe = HybridTrainPipe(
            file_root,
            filelist,
            batch_size,
            resize_shorter,
            crop,
            min_area,
            lower,
            upper,
            interp,
            mean,
            std,
            device_id=gpu_id,
            shard_id=shard_id,
            num_shards=num_shards,
            seed=42 + shard_id,
            data_layout=data_layout,
            num_threads=4)
        pipe.build()
        pipelines = [pipe]
        sample_per_shard = len(pipe) // num_shards
    else:
        pipelines = []
        places = fluid.framework.cuda_places()
        num_shards = len(places)
        for idx, p in enumerate(places):
            place = fluid.core.Place()
            place.set_place(p)
            device_id = place.gpu_device_id()
            pipe = HybridTrainPipe(
                file_root,
                filelist,
                batch_size,
                resize_shorter,
                crop,
                min_area,
                lower,
                upper,
                interp,
                mean,
                std,
                device_id,
                idx,
                num_shards,
                seed=42 + idx,
                data_layout=data_layout,
                num_threads=4)
            pipe.build()
            pipelines.append(pipe)
        sample_per_shard = len(pipelines[0])

    return DALIGenericIterator(
        pipelines, ['feed_image', 'feed_label'], size=sample_per_shard)


def train(filelist,
          batch_size,
          image_mean,
          image_std,
          resize_short_size,
          lower_scale,
          lower_ratio,
          upper_ratio,
          trainer_id=None,
          trainers_num=None,
          gpu_id=0,
          data_layout="NCHW"):
    return build(
        filelist,
        batch_size,
        image_mean,
        image_std,
        resize_short_size,
        lower_scale,
        lower_ratio,
        upper_ratio,
        'train',
        trainer_id=trainer_id,
        trainers_num=trainers_num,
        gpu_id=gpu_id,
        data_layout=data_layout)


def val(settings,
        trainer_id=None,
        trainers_num=None,
        gpu_id=0,
        data_layout="NCHW"):
    return build(
        settings,
        'val',
        trainer_id=trainer_id,
        trainers_num=trainers_num,
        gpu_id=gpu_id,
        data_layout=data_layout)
