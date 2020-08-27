#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Data"""

from typing import Any, Dict, Iterable, List, Optional, Set, TypeVar, Union, overload

from typing_extensions import Literal

from ..label import (
    Classification,
    Label,
    LabeledBox2D,
    LabeledBox3D,
    LabeledPolygon2D,
    LabeledPolyline2D,
    LabelType,
)

T = TypeVar("T", bound=Label)  # pylint: disable=invalid-name


class Data:
    """this class defines the concept of labels to one file

    :param fileuri: the file path of the labeled object in this data
    :param timestamp: the timestamp when collecting the labeled object in this data
    :param loads: {
        "fileuri": <str>,
        "timestamp": <float>,
        "labels_classification": {...},
        "labels_box2D": {...},
        "labels_box3D": {...},
        "labels_polygon": {...},
        "labels_polyline": {...},
    }
    :TypeError: when fileuri is not given
    """

    def __init__(
        self,
        fileuri: Optional[str] = None,
        *,
        remote_path: str = "",
        timestamp: Optional[float] = None,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:

        self._labels: Dict[LabelType, Any] = {}
        self.remote_path = remote_path  # The remote storage location of the data

        if loads:
            self._fileuri: str = loads["fileuri"]
            self._timestamp: Optional[float] = loads.get("timestamp", None)

            for label_type in LabelType:
                load_labels = loads.get(label_type.value, None)
                if not load_labels:
                    continue
                if label_type == LabelType.CLASSIFICATION:
                    self._labels[label_type] = label_type.type(loads=load_labels)
                else:
                    self._labels[label_type] = [
                        label_type.type(loads=label) for label in load_labels
                    ]
            return

        if not fileuri:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required positional argument: 'fileuri'"
            )

        self._fileuri = fileuri
        self._timestamp = timestamp

    def dumps(self) -> Dict[str, Any]:
        """dump a data into a dict"""

        data_dict: Dict[str, Any] = {}
        data_dict["fileuri"] = self._fileuri
        if self._timestamp is not None:
            data_dict["timestamp"] = self._timestamp

        data_dict.update(self.dump_labels())

        return data_dict

    def dump_labels(self) -> Dict[str, Any]:
        """dump all labels into a dict"""

        labels_dict: Dict[str, Any] = {}
        for key, labels in self._labels.items():
            if key == LabelType.CLASSIFICATION:
                labels_dict[key.value] = labels.dumps()
            else:
                labels_dict[key.value] = [label.dumps() for label in labels]

        return labels_dict

    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._fileuri}")'

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def fileuri(self) -> str:
        """Return fileuri of the data.

        :return: fileuri of the data
        """

        return self._fileuri

    @property
    def timestamp(self) -> Optional[float]:
        """Return timestamp of the data.

        :return: timestamp of the data
        """

        return self._timestamp

    def register_label(self, label_types: Union[LabelType, Iterable[LabelType]]) -> None:
        """register one or several label types to data

        :param label_types: the LabelType to register
        """
        # pylint: disable=isinstance-second-argument-not-valid-type
        # https://github.com/PyCQA/pylint/issues/3507
        if not isinstance(label_types, Iterable):
            label_types = [label_types]

        for label_type in label_types:
            if label_type == LabelType.CLASSIFICATION:
                continue

            self._labels[label_type] = []

    def append_label(self, label: Label) -> None:
        """append a label to labels

        :param label: a Label to append
        :raises TypeError: when the label type of the append label is not registerd
        """

        if label.enum == LabelType.CLASSIFICATION:
            self._labels[label.enum] = label
            return

        try:
            self._labels[label.enum].append(label)
        except KeyError:
            raise TypeError(
                "LabelType needs to be registerd before appending label "
                f"(call register_label(LabelType.{label.enum.name}))"
            )

    @overload
    def get_labels(self, label_type: Literal[LabelType.CLASSIFICATION]) -> Classification:
        ...

    @overload
    def get_labels(self, label_type: Literal[LabelType.BOX2D]) -> List[LabeledBox2D]:
        ...

    @overload
    def get_labels(self, label_type: Literal[LabelType.BOX3D]) -> List[LabeledBox3D]:
        ...

    @overload
    def get_labels(self, label_type: Literal[LabelType.POLYGON]) -> List[LabeledPolygon2D]:
        ...

    @overload
    def get_labels(self, label_type: Literal[LabelType.POLYLINE]) -> List[LabeledPolyline2D]:
        ...

    @overload
    def get_labels(self, label_type: LabelType) -> Union[Classification, List[T]]:
        ...

    def get_labels(self, label_type: LabelType) -> Union[Classification, List[T]]:
        """return one type of labels in a data

        :param label_type: required LabelType
        :raises TypeError: when the requested label type is not registerd
        """

        try:
            return self._labels[label_type]  # type: ignore[no-any-return]
        except KeyError:
            raise TypeError(f"LabelType.{label_type.name} is not registerd")

    def get_label_types(self) -> Set[LabelType]:
        """return label types in a data"""

        return set(self._labels.keys())
