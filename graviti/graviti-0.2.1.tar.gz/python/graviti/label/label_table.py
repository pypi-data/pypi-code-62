#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class CatagoryInfo, AttributeInfo and LabelTable."""

from typing import Any, Dict, List, Optional, Union

from ..utility import NameClass, NameSortedDict
from .label import LabelType


class CategoryInfo(NameClass):
    """ Information of a category, includes category name and description

    :param name: The name of the category
    :param loads: A dict contains all information of the category
    :raises
        TypeError: Name is required when not given loads
    """


class AttributeInfo(NameClass):
    """ Information of a attribute

    :param name: The name of the attribute
    :param values: The possible values of the attribute
    :param parent_categories: The parent categories of the attribute
    :param loads: A dict contains all information of the attribute
    :raises
        TypeError: Name and values are required when not given loads
    """

    def __init__(
        self,
        name: Optional[str] = None,
        values: Optional[List[str]] = None,
        parent_categories: Union[None, str, List[str]] = None,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ):
        if loads:
            super().__init__(loads=loads)
            self._values: List[str] = loads["values"]
            self._parent_categories: List[str] = loads.get("parent_categories", [])
            return

        super().__init__(name)

        if not values:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required positional argument: 'values'",
            )

        self._values = values
        if isinstance(parent_categories, str):
            parent_categories = [parent_categories]
        self._parent_categories = parent_categories if parent_categories else []

    def dumps(self) -> Dict[str, Any]:
        """Dumps the information of this attribute as a dictionary.

        :return: A dictionary contains all information of this attribute
        """
        data: Dict[str, Any] = super().dumps()
        data["values"] = self._values
        if self._parent_categories:
            data["parent_categories"] = self._parent_categories
        return data


class LabelTable:
    """A table contains all labels in a specific label type

    :param label_type: The label type of the label table
    :param loads: A dict contains all information of the label table
    :raises
        TypeError: Name and values are required when not given loads
    """

    def __init__(
        self,
        label_type: Optional[LabelType] = None,
        is_tracking: bool = False,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._categories: NameSortedDict[CategoryInfo] = NameSortedDict()
        self._attributes: NameSortedDict[AttributeInfo] = NameSortedDict()

        if loads:
            self._label_type = LabelType[loads["label_type"]]
            self._is_tracking = loads["is_tracking"]

            for category in loads.get("categories", []):
                self.add_category(loads=category)

            for attribute in loads.get("attributes", []):
                self.add_attribute(loads=attribute)

            return

        if not label_type:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required positional argument: 'label_type'."
            )

        self._label_type = label_type
        self._is_tracking = is_tracking

    def __str__(self) -> str:
        str_list = [f"{self.__class__.__name__}({self._label_type.name})["]

        for category in self._categories.values():
            str_list.append(f"  {str(category)},")

        for attribute in self._attributes.values():
            str_list.append(f"  {str(attribute)},")

        str_list.append("]")

        return "\n".join(str_list)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def label_type(self) -> LabelType:
        """Return label_type of the LabelTable.

        :return: label_type of the LabelTable.
        """
        return self._label_type

    @property
    def is_tracking(self) -> bool:
        """Return whether the label is a tracking label

        :return: If it this a tracking label, return `True`, otherwise return `False`
        """
        return self.is_tracking

    @property
    def categories(self) -> NameSortedDict[CategoryInfo]:
        """Return all the categories of the LabelTable.

        :return: A NameSortedDict of all the categories
        """
        return self._categories

    def dumps(self) -> Dict[str, Any]:
        """Dumps the information of this LabelTable as a dictionary.

        :return: A dictionary contains all information of this LabelTable
        """
        data: Dict[str, Any] = {
            "label_type": self._label_type.name,
            "is_tracking": self._is_tracking,
        }

        categories = [category.dumps() for category in self._categories.values()]
        attributes = [attribute.dumps() for attribute in self._attributes.values()]

        if categories:
            data["categories"] = categories
        if attributes:
            data["attribute"] = attributes

        return data

    def add_category(
        self, name: Optional[str] = None, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a category to the LabelTable

        :param name: The name of the category
        :param loads: A dict contains all information of the category
        """
        self._categories.add(CategoryInfo(name, loads=loads))

    def add_attribute(
        self,
        name: Optional[str] = None,
        values: Optional[List[str]] = None,
        parent_categories: Optional[List[str]] = None,
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a attribute to the LabelTable

        :param name: The name of the attribute
        :param values: The possible values of the attribute
        :param parent_categories: The parent categories of the attribute
        :param loads: A dict contains all information of the attribute
        """
        self._attributes.add(AttributeInfo(name, values, parent_categories, loads=loads))
