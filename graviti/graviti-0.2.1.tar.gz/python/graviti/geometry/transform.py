#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Transform3D.
"""

import collections
from typing import Dict, Optional, Sequence, Union, overload

import numpy as np

from .quaternion import Quaternion
from .vector import Vector3D


class Transform3D:
    """A class used to represent a transformation in 3D.

    :param translation: Translation in a sequence of [x, y, z]
    :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or Quaternion
    :param loads: A dictionary containing the translation and the rotation
    :param matrix: A 4x4 transform matrix
    :param kwargs: Other parameters to initialize rotation of the transform based on pyquaternion
    :raises ValueError: When the shape of the input matrix is wrong
    """

    MatrixType = Union[None, Sequence[Sequence[float]], np.ndarray]

    def __init__(
        self,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        *,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        matrix: MatrixType = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        if loads:
            self._translation = Vector3D(loads=loads["translation"])
            self._rotation = Quaternion(loads=loads["rotation"])
            return

        if matrix is not None:
            if isinstance(matrix, collections.abc.Sequence):
                matrix = np.array(matrix)
            if matrix.shape != (4, 4):
                raise ValueError("The shape of input matrix must be 4x4.")

            self._translation = Vector3D(list(matrix[:3, 3]))
            self._rotation = Quaternion(matrix=matrix)
            return

        self._translation = Vector3D(translation)
        self._rotation = Quaternion(rotation, loads=None, **kwargs)

    def dumps(self) -> Dict[str, Dict[str, float]]:
        """Dumps the 3D transform as a dictionary.

        :return: A dictionary containing translation and rotation information of the transform3D
        """
        return {
            "translation": self._translation.dumps(),
            "rotation": self._rotation.dumps(),
        }

    @overload
    def __mul__(self, other: "Transform3D") -> "Transform3D":
        ...

    @overload
    def __mul__(self, other: Sequence[float]) -> Vector3D:
        ...

    def __mul__(
        self, other: Union["Transform3D", Sequence[float]]
    ) -> Union["Transform3D", Vector3D]:

        if isinstance(other, collections.abc.Sequence):
            return self._translation + list(self._rotation.rotate(other))

        if isinstance(other, Transform3D):
            transform: Transform3D = object.__new__(Transform3D)
            transform._rotation = self._rotation * other.rotation
            transform._translation = self * other.translation
            return transform

        return NotImplemented  # type: ignore[unreachable]

    def __str__(self) -> str:
        translation = self._translation
        rotation = self._rotation
        return (
            f"{self.__class__.__name__}("
            f"\n  Translation({translation.x}, {translation.y}, {translation.z}),"
            f"\n  Rotation({rotation.w}, {rotation.x}, {rotation.y}, {rotation.z}),"
            "\n)"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._translation.__eq__(other.translation) and self._rotation == other.rotation

        return False

    @property
    def translation(self) -> Vector3D:
        """Returns translation of the 3D transform.

        :return: Translation in Vector3D
        """
        return self._translation

    def set_translation(self, *args: Union[float, Sequence[float]], **kwargs: float) -> None:
        """Set the translation of the transform.

        :param args: Coordinates of the translation vector
        :param kwargs: keyword-only argument to set different dimension for translation vector
            transform.set_translation(x=1, y=2, z=3)
        """
        self._translation = Vector3D(*args, loads=None, **kwargs)

    @property
    def rotation(self) -> Quaternion:
        """Returns rotation of the 3D transform.

        :return: rotation in Quaternion
        """
        return self._rotation

    def set_rotation(
        self, *args: Union[Quaternion.ArgsType, float], **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the rotation of the transform.

        :param args: Coordinates of the Quaternion
        :param kwargs: keyword-only argument to the Quaternion
        """
        self._rotation = Quaternion(*args, loads=None, **kwargs)

    def inverse(self) -> "Transform3D":
        """Return the inverse of the transform.

        :return: A Transform3D object representing the inverse of this Transform3D
        """
        rotation = self._rotation.inverse
        translation = rotation.rotate(list(-self._translation))
        return Transform3D(translation, rotation)
