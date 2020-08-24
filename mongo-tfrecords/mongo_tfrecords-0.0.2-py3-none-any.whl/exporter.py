# Copyright 2020 Vadim Sharay <vadimsharay@gmail.com>
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

import math
import os
from typing import Union, Iterable, Callable

from pymongo import MongoClient
from pymongo.database import Database

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tensorflow as tf


def _bytes_feature(value):
    """Returns a bytes_list from a string / byte."""
    # If the value is an eager tensor BytesList won't unpack a string from an EagerTensor.
    if isinstance(value, type(tf.constant(0))):
        value = value.numpy()
    if isinstance(value, str):
        value = value.encode("utf-8")

    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def _float_feature(value):
    """Returns a float_list from a float / double."""
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))


def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


FEATURES_TYPES_MAP = {
    "bytes": _bytes_feature,
    "float": _float_feature,
    "int": _int64_feature,
    "int64": _int64_feature,
}


def serialize_example(features_values: dict, features_types: dict) -> tf.train.Example:
    """Returns TFExample object"""

    features_map = {}

    for name, feature_type in features_types.items():
        feature_value = features_values.get(name, ...)

        if feature_value is ...:
            return None

        if isinstance(feature_type, Callable):
            feature = feature_type(feature_value)
        else:
            feature_fn = FEATURES_TYPES_MAP[str(feature_type)]
            feature = feature_fn(feature_value)

        features_map[name] = feature

    return tf.train.Example(features=tf.train.Features(feature=features_map))


def generate_features_types_map(data: Iterable, callback: Callable = None):
    features_map = {}

    def _get_type(val):
        feature_type = "bytes"
        if isinstance(val, int):
            feature_type = "int"
        if isinstance(val, float):
            feature_type = "float"
        return feature_type

    for item in data:
        if callback:
            _item = callback(item)
            if _item is not None:
                item = _item

        for key, value in item.items():
            exists_feature_type = features_map.get(key)
            item_feature_type = _get_type(value)

            if exists_feature_type and item_feature_type != exists_feature_type:
                if item_feature_type == "float" or exists_feature_type == "int":
                    features_map[key] = "float"
                else:
                    raise ValueError("Broken schema of data")
            else:
                features_map[key] = item_feature_type

    return features_map


def database_from_uri(uri: str):
    client = MongoClient(uri)
    return client.get_default_database("default")


def export(
    collection: str,
    path=".",
    files_template="{}.tfrecord",
    count_per_file=100000,
    database: Union[str, Database] = None,
    features: Union[list, dict] = None,
    features_gen_batch: int = 100,
    callback: Callable = None,
    skip: int = None,
    limit: int = None,
    verbose=False,
):
    if not database:
        database = "mongodb://root:root@localhost:27017/default?authSource=admin"
    if isinstance(database, str):
        database = database_from_uri(database)

    assert isinstance(database, Database)
    assert features is None or isinstance(features, Iterable)

    collection = database[collection]

    if (
        not features
        or not isinstance(features, dict)
        and isinstance(features, Iterable)
    ):
        projection = {"_id": 0}

        if features:
            for f in features:
                projection[f] = 1

        pre_batch = collection.find({}, projection).limit(features_gen_batch)
        features = generate_features_types_map(pre_batch, callback)

    cursor = collection.find()
    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)

    dataset_size = cursor.count(True)
    files_count = math.ceil(dataset_size / count_per_file)

    glob_counter = 0

    for file_index in range(files_count):
        counter = 0

        file_path = os.path.join(path, files_template.format(file_index))
        with tf.io.TFRecordWriter(file_path) as writer:
            while counter < count_per_file:
                try:
                    item = cursor.next()
                except StopIteration:
                    break

                if callback:
                    _item = callback(item)
                    if _item is not None:
                        item = _item

                example = serialize_example(item, features)
                if not example:
                    dataset_size -= 1
                    continue

                writer.write(example.SerializeToString())
                counter += 1
                glob_counter += 1

                if verbose and glob_counter % 10 == 0:
                    print(
                        "Progress: {:.2f}%\r".format(glob_counter / dataset_size * 100),
                        end="",
                    )
