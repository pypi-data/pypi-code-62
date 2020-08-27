#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class SegmentClientBase, SegmentClient, FusionSegmentClient."""

import base64
import json
import os
import threading
import time
import uuid
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Union

import filetype
from requests_toolbelt import MultipartEncoder

from ..dataset import Data, Frame
from ..sensor import Camera, FisheyeCamera, Sensor, SensorType
from ..utility import NameSortedDict
from .exceptions import GASException, GASFrameError, GASPathError
from .requests import Client, post

T = TypeVar("T", bound=Sensor)  # pylint: disable=invalid-name


class SegmentClientBase(Client):
    """This class defines the concept of a segment client and some opertions on it.

    :param name: Segment name, unique for a dataset
    :param dataset_id: Dataset's id
    :param gateway_url: The url of the gas website
    :param access_key: User's access key
    """

    _PERMISSION_CATEGORY: str
    _SEGMENT_PATH_START: str = ".segment"
    _SEGMENT_PATH_END: str = ".segment_end"

    def __init__(self, name: str, dataset_id: str, access_key: str, gateway_url: str) -> None:
        super().__init__(access_key, gateway_url)

        self._name = name
        self._dataset_id = dataset_id
        self._permission = {"expireAt": 0}
        self._permission_lock = threading.Lock()
        self._expired_in_second = 60

        if not self._name:
            self._segment_prefix = PurePosixPath()
        else:
            self._segment_prefix = PurePosixPath(
                SegmentClientBase._SEGMENT_PATH_START, name, SegmentClientBase._SEGMENT_PATH_END
            )

    def upload_description(self, description: Optional[str] = None) -> None:
        """Upload description of the segment client.

        :param description: Description of the segment client to upload
        """
        if not description:
            return
        post_data = {"contentSetId": self._dataset_id, "name": self._name, "desc": description}
        self._dataset_post("createOrUpdateSegment", post_data)

    def get_segment_name(self) -> str:
        """Return the name of this segment client."""
        return self._name

    def _get_upload_permission(self) -> Dict[str, Any]:
        with self._permission_lock:
            if int(time.time()) + 30 >= self._permission["expireAt"]:
                post_data = {
                    "id": self._dataset_id,
                    "category": self._PERMISSION_CATEGORY,
                    "expiredInSec": self._expired_in_second,
                    "segmentName": self._name,
                }
                self._permission = self._dataset_post("getPutPermission", post_data)

            return deepcopy(self._permission)

    def _clear_upload_permission(self) -> None:
        with self._permission_lock:
            self._permission = {"expireAt": 0}

    def _get_object_path(self, remote_path: str, sensor_name: str = "") -> str:
        if not self._name and not sensor_name:
            return remote_path

        return str(PurePosixPath(self._segment_prefix, sensor_name, remote_path))

    def _get_remote_path(self, object_path: str, sensor_name: str = "") -> str:
        if not self._name and not sensor_name:
            return object_path

        header = PurePosixPath(self._segment_prefix, sensor_name)
        return object_path[len(str(header)) + 1 :]

    @staticmethod
    def _post_multipart_formdata(
        url: str, local_path: str, remote_path: str, data: Dict[str, Any]
    ) -> None:
        with open(local_path, "rb") as file:
            data["file"] = (remote_path, file, filetype.guess_mime(local_path))
            multipart = MultipartEncoder(data)
            post(url, data=multipart, content_type=multipart.content_type)


class SegmentClient(SegmentClientBase):
    """SegmentClient has only one sensor, supporting upload_data method."""

    _PERMISSION_CATEGORY = "contentSet"

    def upload_data(self, local_path: str, remote_path: str = "") -> None:
        """Upload data with local path to the segment.

        :param local_path: The local path of the data to upload
        :param remote_path: The path to save the data in segment client
        :raises
            GASPathError: when remote_path does not follow linux style
            GASFrameError: when uploading frame has neither timestamp nor frame_index
        """

        if not remote_path:
            remote_path = os.path.basename(local_path)

        if "\\" in remote_path:
            raise GASFrameError()

        permission = self._get_upload_permission()
        post_data = permission["result"]
        post_data["key"] = permission["extra"]["objectPrefix"] + remote_path

        try:
            self._post_multipart_formdata(
                permission["extra"]["host"], local_path, remote_path, post_data
            )
        except GASException:
            self._clear_upload_permission()
            raise

    def upload_data_object(self, data: Data) -> None:
        """Upload data with local path in Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self.upload_data(data.fileuri, data.remote_path)

    def delete_data(self, remote_paths: Union[str, List[str]]) -> None:
        """Delete data with remote paths.

        :param remote_path_list: A single path or a list of paths which need to deleted,
        eg: test/os1.png or [test/os1.png]
        """
        if not isinstance(remote_paths, list):
            remote_paths = [remote_paths]

        object_paths = [self._get_object_path(remote_path) for remote_path in remote_paths]
        post_data = {
            "contentSetId": self._dataset_id,
            "filePaths": object_paths,
        }
        self._dataset_post("deleteObjects", post_data)

    def list_data(self) -> List[str]:
        """List all data in a segment client.

        :return: A list of data path
        """
        post_data = {"contentSetId": self._dataset_id, "segmentName": self._name}
        data = self._dataset_post("listObjects", post_data)
        return [self._get_remote_path(object_path) for object_path in data["objects"]]


class FusionSegmentClient(SegmentClientBase):
    """FusionSegmentClient has multiple sensors,
    supporting upload_sensor and upload_frame method.
    """

    _PERMISSION_CATEGORY = "frame"

    def upload_sensor_object(self, sensor: T) -> None:
        """Upload sensor to the segment client.

        :param sensor: The sensor to upload
        """
        post_data = {
            "name": sensor.name,
            "type": sensor.enum.value,
            "extrinsicParams": sensor.extrinsics.dumps() if sensor.extrinsics else {},
        }

        if isinstance(sensor, (Camera, FisheyeCamera)):
            if sensor.intrinsics:
                intrinsics = sensor.intrinsics.dumps()
                intrinsics["cameraMatrix"] = intrinsics.pop("camera_matrix")
                intrinsics["distortionCoefficient"] = intrinsics.pop("distortion_coefficients", {})
                post_data["intrinsicParams"] = intrinsics
            else:
                post_data["intrinsicParams"] = {}

        if sensor.description:
            post_data["desc"] = sensor.description

        post_data["contentSetId"] = self._dataset_id
        post_data["segmentName"] = self._name
        self._dataset_post("createOrUpdateSensor", post_data)

    def delete_sensors(self, sensor_names: Union[str, List[str]]) -> None:
        """Delete sensors with a single name or a name list.

        :param sensor_names: A single sensor name or a list of sensor names
        """
        if not isinstance(sensor_names, list):
            sensor_names = [sensor_names]
        post_data = {
            "contentSetId": self._dataset_id,
            "sensorNames": {self._name: sensor_names},
        }
        self._dataset_post("deleteSensors", post_data)

    def _list_sensor_summaries(self) -> List[Dict[str, Any]]:
        post_data = {"contentSetId": self._dataset_id, "segmentName": self._name}
        data = self._dataset_post("listSensors", post_data)
        return data["sensors"]  # type: ignore[no-any-return]

    def list_sensors(self) -> List[str]:
        """List all sensor names in a segment client.

        :return: A list of sensor name
        """
        sensor_summaries = self._list_sensor_summaries()
        sensor_names: List[str] = []
        for sensor_info in sensor_summaries:
            sensor_names.append(sensor_info["name"])
        return sensor_names

    def list_sensor_objects(self) -> NameSortedDict[Sensor]:
        """List all sensors in a segment client.

        :return: A NameSortedDict of `Sensor` object
        """
        sensor_summaries = self._list_sensor_summaries()
        sensors: NameSortedDict[Sensor] = NameSortedDict()
        for sensor_info in sensor_summaries:
            SensorClass = SensorType(sensor_info["type"]).type  # pylint: disable=invalid-name
            sensor = SensorClass(sensor_info["name"])
            sensor.description = sensor_info["desc"]
            extrinsics = json.loads(sensor_info["extrinsicParams"])
            if extrinsics:
                sensor.set_extrinsics(loads=extrinsics)
            if isinstance(sensor, Camera):
                intrinsics = json.loads(sensor_info["intrinsicParams"])
                if intrinsics:
                    sensor.set_camera_matrix(**intrinsics["cameraMatrix"])
                    if "distortionCoefficient" in intrinsics:
                        sensor.set_distortion_coefficients(**intrinsics["distortionCoefficient"])
            sensors.add(sensor)

        return sensors

    def upload_frame_object(self, frame: Frame, frame_index: Optional[int] = None) -> None:
        """Upload frame to the segment client.

        :param frame: The frame to upload
        :param frame_index: The frame index, used for TensorBay to sort the frame
        :raises
            GASPathError: when remote_path does not follow linux style
        """

        frame_id = str(uuid.uuid4())

        for sensor_name, data in frame.items():
            if "\\" in data.remote_path:
                raise GASPathError(data.remote_path)

            if frame_index is None and data.timestamp is None:
                raise GASPathError(data.remote_path)

            remote_path = data.remote_path if data.remote_path else os.path.basename(data.fileuri)

            permission = self._get_upload_permission()
            post_data = permission["result"]

            path = str(PurePosixPath(sensor_name, remote_path))
            post_data["key"] = permission["extra"]["objectPrefix"] + path

            data_info: Dict[str, Any] = {
                "sensorName": sensor_name,
                "segmentName": self._name,
                "frameId": frame_id,
                "objectPath": path,
            }
            if data.timestamp is not None:
                data_info["timestamp"] = data.timestamp

            if frame_index is not None:
                data_info["frameIndex"] = frame_index

            post_data["x:incidental"] = base64.urlsafe_b64encode(
                json.dumps(data_info).encode()
            ).decode()

            try:
                self._post_multipart_formdata(
                    permission["extra"]["host"], data.fileuri, remote_path, post_data,
                )
            except GASException:
                self._clear_upload_permission()
                raise

    def list_frame_objects(self) -> List[Frame]:
        """List all frames in the segment client.

        :return: A list `Frame` object
        """
        response = self._list_frames()
        frames = []
        for response_frame in response:
            frame = self._loads_frame_object(response_frame)
            frames.append(frame)

        return frames

    def _list_frame_objects_dict(self) -> Dict[int, Tuple[Frame, str]]:
        response = self._list_frames()
        frames: Dict[int, Tuple[Frame, str]] = {}
        for response_frame in response:
            frame = self._loads_frame_object(response_frame)
            frame_index = response_frame[0]["frameIndex"]
            frame_id = response_frame[0]["frameId"]

            frames[frame_index] = (frame, frame_id)

        return frames

    def _list_frames(self, offset: int = 0, page_size: int = -1) -> List[List[Dict[str, Any]]]:
        post_data = {
            "contentSetId": self._dataset_id,
            "segmentName": self._name,
            "offSet": offset,
            "pageSize": page_size,
        }
        return self._dataset_post("listFrames", post_data)["frames"]  # type: ignore[no-any-return]

    def _loads_frame_object(self, loads: List[Dict[str, Any]]) -> Frame:
        frame = Frame()
        for data_info in loads:
            sensor_name = data_info["sensorName"]
            remote_path = self._get_remote_path(data_info["objectPath"], sensor_name)
            data = Data(remote_path, timestamp=data_info.get("timestamp", None))
            frame[sensor_name] = data

        return frame

    def _delete_frames(self, frame_id: Union[str, List[str]]) -> None:
        if not isinstance(frame_id, list):
            frame_id = [frame_id]

        post_data = {"contentSetId": self._dataset_id, "frameIds": frame_id}
        self._dataset_post("deleteFrames", post_data)
