#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines TensorBay Resource Name (TBRN) related classes."""

from enum import Enum, Flag, auto
from typing import Tuple, Union


class _TBRNFlag(Flag):
    FIELD_HEAD = 1 << 0
    FIELD_DATASET = 1 << 1
    FIELD_SEGMENT = 1 << 2
    FIELD_FRAME = 1 << 3
    FIELD_SENSOR = 1 << 4
    FIELD_PATH = 1 << 5

    # tb:[dataset]
    DATASET = FIELD_HEAD | FIELD_DATASET

    # tb:[dataset]:[segment]
    SEGMENT = FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT

    # tb:[dataset]:[segment]:[frame]
    FRAME = FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT | FIELD_FRAME

    # tb:[dataset]:[segment]::[sensor]
    SENSOR_WITHOUT_FRAME = FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT | FIELD_SENSOR

    # tb:[dataset]:[segment]:[frame]:[sensor]
    SENSOR_WITH_FRAME = FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT | FIELD_FRAME | FIELD_SENSOR

    # tb:[dataset]:[segment]://[remote_path]
    NORMAL_FILE = FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT | FIELD_PATH

    # tb:[dataset]:[segment]:[frame]:[sensor]://[remote_path]
    FUSION_FILE = (
        FIELD_HEAD | FIELD_DATASET | FIELD_SEGMENT | FIELD_FRAME | FIELD_SENSOR | FIELD_PATH
    )


class TBRNType(Enum):
    """`TBRNType` represent the type of a TBRN, which has 6 types:
    1. `TBRNType.DATASET`:
        "tb:VOC2012"
        which means the dataset "VOC2012"
    2. `TBRNType.SEGMENT`:
        "tb:VOC2010:train"
        which means the "train" segment of dataset "VOC2012"
    3. `TBRNType.FRAME`:
        "tb:KITTI:test:10"
        which means the 10th frame of the "test" segment in dataset "KITTI"
    4. `TBRNType.SENSOR`:
        "tb:KITTI:test:10:lidar" or "tb:KITTI:test::lidar"
        which means the sensor "lidar" of the "test" segment in dataset "KITTI"
    5. `TBRNType.NORMAL_FILE`:
        "tb:VOC2012:train://2012_004330.jpg"
        which means the file "2012_004330.jpg" of the "train" segment in normal dataset "VOC2012"
    6. `TBRNType.FUSION_FILE`
        "tb:KITTI:test:10:lidar://000024.bin"
        which means the file "000024.bin" in fusion dataset "KITTI", its segment, frame index and
        sensor is "test", 10 and "lidar"
    """

    DATASET = auto()
    SEGMENT = auto()
    FRAME = auto()
    SENSOR = auto()
    NORMAL_FILE = auto()
    FUSION_FILE = auto()


class TBRNInfo:
    """`TBRNInfo` is a TensorBay Resource Name(TBRN) parser and generator.

    Use as a generator:
        >>> info = TBRNInfo("VOC2010", "train", remote_path="2012_004330.jpg")
        >>> info.type
        <TBRNType.NORMAL_FILE: 5>
        >>> info.get_tbrn()
        'tb:VOC2010:train://2012_004330.jpg'

    Use as a parser:
        >>> tbrn = "tb:VOC2010:train://2012_004330.jpg"
        >>> info = TBRNInfo(tbrn=tbrn)
        >>> print(info)
        TBRNInfo(
          dataset_name="VOC2010"
          segment_name="train"
          frame_index=""
          sensor_name=""
          remote_path="2012_004330.jpg"
        )

    :param dataset_name: name of the dataset.
    :param segment_name: name of the segment.
    :param frame_index: index of the frame.
    :param sensor_name: name of the sensor.
    :param remote_path: object path of the file.
    :param tbrn: full TBRN string
    :raises
        `TypeError`: The TBRN is invalid

    """

    _HEAD = "tb"
    _NAMES_SEPARATOR = ":"
    _NAMES_MAX_SPLIT = 4
    _PATH_SEPARATOR = "://"
    _PATH_MAX_SPLIT = 1

    _FLAG_TO_TYPE = {
        _TBRNFlag.DATASET: (TBRNType.DATASET, 2),
        _TBRNFlag.SEGMENT: (TBRNType.SEGMENT, 3),
        _TBRNFlag.FRAME: (TBRNType.FRAME, 4),
        _TBRNFlag.SENSOR_WITH_FRAME: (TBRNType.SENSOR, 5),
        _TBRNFlag.SENSOR_WITHOUT_FRAME: (TBRNType.SENSOR, 5),
        _TBRNFlag.NORMAL_FILE: (TBRNType.NORMAL_FILE, 3),
        _TBRNFlag.FUSION_FILE: (TBRNType.FUSION_FILE, 5),
    }

    def __init__(
        self,
        dataset_name: str = "",
        segment_name: str = "",
        frame_index: Union[str, int] = "",
        sensor_name: str = "",
        *,
        remote_path: str = "",
        tbrn: str = "",
    ) -> None:
        if tbrn:
            splits = tbrn.split(self._PATH_SEPARATOR, self._PATH_MAX_SPLIT)
            self._names = splits[0].split(self._NAMES_SEPARATOR, self._NAMES_MAX_SPLIT)

            if self._names[0] != self._HEAD:
                raise TypeError('TensorBay Resource Name should startwith "tb:"')

            self._names += [""] * (self._NAMES_MAX_SPLIT + 1 - len(self._names))

            if len(splits) == self._PATH_MAX_SPLIT + 1:
                self._names.append(splits[1])
            else:
                self._names.append("")

        else:
            if not isinstance(frame_index, str):
                frame_index = str(frame_index)

            self._names = [
                self._HEAD,
                dataset_name,
                segment_name,
                frame_index,
                sensor_name,
                remote_path,
            ]

        try:
            self._type, self._field_length = self._check_type()
        except KeyError:
            raise TypeError("Invalid TensorBay Resource Name")

    def _check_type(self) -> Tuple[TBRNType, int]:
        flag = 0
        for i, name in enumerate(self._names):
            if name:
                flag |= 1 << i

        return self._FLAG_TO_TYPE[_TBRNFlag(flag)]

    def __str__(self) -> str:
        str_list = [
            f"{self.__class__.__name__}(",
            f'  dataset_name="{self.dataset_name}"',
            f'  segment_name="{self.segment_name}"',
            f'  frame_index="{self.frame_index}"',
            f'  sensor_name="{self.sensor_name}"',
            f'  remote_path="{self.remote_path}"',
            ")",
        ]
        return "\n".join(str_list)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def dataset_name(self) -> str:
        """Returns the dataset name.

        :return: the dataset name.
        """
        return self._names[1]

    @property
    def segment_name(self) -> str:
        """Returns the segment name.

        :return: the segment name.
        """
        return self._names[2]

    @property
    def frame_index(self) -> str:
        """Returns the frame index.

        :return: the frame index.
        """
        return self._names[3]

    @property
    def sensor_name(self) -> str:
        """Returns the sensor name.

        :return: the sensor name.
        """
        return self._names[4]

    @property
    def remote_path(self) -> str:
        """Returns the object path.

        :return: the object path.
        """
        return self._names[5]

    @property
    def type(self) -> TBRNType:
        """Returns the type of this TBRN.

        :return: the type of this TBRN.
        """
        return self._type

    def get_tbrn(self) -> str:
        """Generate the full TBRN string

        :return: the full TBRN string
        """
        tbrn = f"{self._NAMES_SEPARATOR.join(self._names[: self._field_length])}"
        if self.remote_path:
            tbrn = f"{tbrn}{self._PATH_SEPARATOR}{self.remote_path}"
        return tbrn
