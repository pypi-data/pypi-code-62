#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class SensorType, Sensor, Lidar, Radar, Camera and FisheyeCamera."""

from typing import Any, Dict, Optional, Sequence, Type, TypeVar, Union

from ..geometry import Quaternion, Transform3D
from ..utility import NameClass, TypeClass, TypeEnum
from .intrinsics import CameraIntrinsics

T = TypeVar("T", bound="Sensor")  # pylint: disable=invalid-name


class SensorType(TypeEnum):
    """this class defines the type of the sensors.

    :param sensor_name: The name string of the json format sensor
    """

    LIDAR = "LIDAR"
    RADAR = "RADAR"
    CAMERA = "CAMERA"
    FISHEYE_CAMERA = "FISHEYE_CAMERA"


class Sensor(NameClass, TypeClass[SensorType]):
    """A class representing sensor including
    name, description, translation and rotation.

    :param name: A string representing the sensor's name
    :loads: A dictionary containing name, description and sensor extrinsics
    :raises
        TypeError: Can't instantiate abstract class Sensor
        TypeError: Name required when not given loads
    """

    def __new__(
        cls: Type[T],
        name: Optional[str] = None,  # pylint: disable=unused-argument
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> T:
        obj: T
        if loads:
            obj = object.__new__(SensorType(loads["type"]).type)
            return obj

        if cls is Sensor:
            raise TypeError("Can't instantiate abstract class Sensor")

        obj = object.__new__(cls)
        return obj

    def __init__(
        self, name: Optional[str] = None, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        if loads:
            super().__init__(loads=loads)
            self._extrinsics = Transform3D(loads=loads["extrinsic"])
            return

        super().__init__(name)
        self._extrinsics = Transform3D()

    def dumps(self) -> Dict[str, Any]:
        """Dumps the sensor as a dictionary.

        :return: A dictionary containing name, description and extrinsic
        """
        data: Dict[str, Any] = super().dumps()
        data["type"] = self.enum.value
        data["extrinsics"] = self._extrinsics.dumps()

        return data

    @property
    def extrinsics(self) -> Transform3D:
        """Return extrinsic of the sensor.

        :return: Extrinsic of the sensor
        """
        return self._extrinsics

    def set_translation(
        self,
        *args: Union[float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> None:
        """Set the translation of the sensor.

        :param args: Coordinates of the translation vector
        :param loads: A dicitionary containing coordinates of a translation vector
        :param kwargs: keyword-only argument to set different dimension for translation vector
            sensor.set_translation(x=1, y=2, z=3)
        """
        self._extrinsics.set_translation(*args, loads=loads, **kwargs)

    def set_rotation(
        self,
        *args: Union[Quaternion.ArgsType, float],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the rotation of the sensor.

        :param args: Coordinates of the Quaternion
        :param loads: A dicitionary containing coordinates of a Quaternion
        :param kwargs: keyword-only argument to the Quaternion
        """
        self._extrinsics.set_rotation(*args, loads=loads, **kwargs)


class Lidar(Sensor, enum=SensorType.LIDAR):
    """This class defines the concept of lidar."""


class Radar(Sensor, enum=SensorType.RADAR):
    """This class defines the concept of radar."""


class Camera(Sensor, enum=SensorType.CAMERA):
    """A class representing camera including
    name, description, translation , rotation, camera_matrix and distortion_coefficient.

    :param name: A string representing camera's name
    :param loads: A dictionary containing name, description, extrinsics and intrinsics
    """

    def __init__(
        self, name: Optional[str] = None, *, loads: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(name, loads=loads)
        if loads:
            self._intrinsics = CameraIntrinsics(loads=loads.get("intrinsic", {}))
        else:
            self._intrinsics = CameraIntrinsics()

    def dumps(self) -> Dict[str, Any]:
        """Dumps the camera as a dictionary.

        :return: A dictionary containing name, description, extrinsic and intrinsic
        """
        message = super().dumps()
        message["intrinsic"] = self._intrinsics.dumps()
        return message

    @property
    def intrinsics(self) -> CameraIntrinsics:
        """Return intrinsics."""

        return self._intrinsics

    def set_camera_matrix(
        self,
        matrix: Optional[Sequence[Sequence[float]]] = None,
        *,
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> None:
        """Set camera matrix."""

        self._intrinsics.set_camera_matrix(matrix, loads=loads, **kwargs)

    def set_distortion_coefficient(
        self, *, loads: Optional[Dict[str, float]] = None, **kwargs: float
    ) -> None:
        """Set distortion coefficient."""

        self._intrinsics.set_distortion_coefficient(loads=loads, **kwargs)


class FisheyeCamera(Camera, enum=SensorType.FISHEYE_CAMERA):
    """This class defines the concept of fisheye camera."""
