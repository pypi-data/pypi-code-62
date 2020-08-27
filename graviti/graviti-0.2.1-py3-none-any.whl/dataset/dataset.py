#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetBase, Dataset and FusionDataset."""

from typing import Dict, Sequence, Set, TypeVar, Union, overload

from ..label import LabelTable, LabelType
from ..utility import NameClass, NameSortedList
from .segment import FusionSegment, Segment

T = TypeVar("T", FusionSegment, Segment)  # pylint: disable=invalid-name


class DatasetBase(NameClass, Sequence[T]):
    """This class defines the concept of DatasetBase,
    which represents a whole dataset contains several segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    """

    def __init__(self, name: str, is_continuous: bool = False) -> None:
        super().__init__(name)
        self._segments: NameSortedList[T] = NameSortedList()
        self._label_tables: Dict[LabelType, LabelTable] = {}
        self._is_continuous = is_continuous

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Sequence[T], T]:
        return self._segments.__getitem__(index)

    def __len__(self) -> int:
        return self._segments.__len__()

    def __str__(self) -> str:
        return f"{super()} {self._segments}"

    @property
    def is_continuous(self) -> bool:
        """Check whether the data in dataset is continuous

        :return: Return `True` if the data is continuous, otherwise return `False`
        """
        return self._is_continuous

    def add_label_table(self, label_table: LabelTable) -> None:
        """Add label table.

        :param label_table: a instance of LabelTable
        """

        self._label_tables[label_table.label_type] = label_table

    def get_label_table(self, label_type: LabelType) -> LabelTable:
        """return the label table corresponding to given LabeleType.

        :param label_type: a instance of LabelType
        :return: a label table
        """

        return self._label_tables[label_type]

    def get_label_types(self) -> Set[LabelType]:
        """return a set contains all label types.

        :return: a set of all label types
        """

        return set(self._label_tables.keys())

    def get_segment_by_name(self, name: str) -> T:
        """return the segment corresponding to given name.

        :param name: name of the segment
        :return: the segment which matches the input name
        """

        return self._segments.get_from_name(name)

    def add_segment(self, segment: T) -> None:
        """add segment to segment list.

        :param segment: a segment to be added
        """

        self._segments.add(segment)


class Dataset(DatasetBase[Segment]):
    """This class defines the concept of dataset,
    which contains a list of segments.
    """


class FusionDataset(DatasetBase[FusionSegment]):
    """This class defines the concept of multi-sensor dataset,
    which contains a list of multi-sensor segments.
    """
