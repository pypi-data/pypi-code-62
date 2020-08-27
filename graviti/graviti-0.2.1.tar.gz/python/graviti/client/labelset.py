#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines the class Labelset.
"""

from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional, Union

from ..dataset import Data
from ..label import LabelTable, LabelType
from .requests import Client
from .segment import SegmentClientBase


class LabelsetClient(Client):
    """A class used to respresent labelset.

    :param labelset_id: The id of the labelset
    :param labelset_client: The client of the labelset
    """

    TYPE_GROUND_TRUTH = 3
    _PUBLISH_STATUS = 2
    _TASK_TYPE = {
        LabelType.CLASSIFICATION: {"code": 7, "nameEn": "2D CLASSIFICATION"},
        LabelType.BOX2D: {"code": 10, "nameEn": "2D BOX"},
        LabelType.BOX3D: {"code": 4, "nameEn": "3D BOX"},
        LabelType.POLYGON: {"code": 22, "nameEn": "2D POLYGON"},
        LabelType.POLYLINE: {"code": 8, "nameEn": "2D POLYLINE"},
    }

    def __init__(self, labelset_id: str, access_key: str, gateway_url: str) -> None:
        super().__init__(access_key, gateway_url)
        self._labelset_id = labelset_id

    def get_labelset_id(self) -> str:
        """Return the id of the labelset.

        :return: The id of the labelset
        """
        return self._labelset_id

    def upload_label_table(self, label_table: Union[LabelTable, List[LabelTable]]) -> None:
        """Upload label table to the labelset.

        :param label_table: The label table to be uploaded
        """
        metadata = self.create_metadata(label_table)
        if not metadata:
            return

        post_data = {
            "labelSetId": self._labelset_id,
            "meta": metadata,
        }
        self._labelset_post("updateLableSet", post_data)

    def upload_label(
        self,
        data: Data,
        segment_name: str = "",
        sensor_name: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Upload label to the labelset.

        :param data: The Data contains the labels to be uploaded
        :param metadata: Some additional data of the label
        :param segment_name: Segment name of the Data
        :param sensor_name: Sensor name of the Data
        """
        post_data: Dict[str, Any] = {}
        post_data["ObjectPath"] = self._get_object_path(data.remote_path, segment_name, sensor_name)
        post_data["labelValues"] = data.dump_labels()
        post_data["labelSetId"] = self._labelset_id
        if metadata:
            post_data["labelMeta"] = metadata
        self._labelset_post("putLabel", post_data)

    def publish(self) -> None:
        """Publish the labelset.
        """
        post_data = {"labelSetId": self._labelset_id, "status": LabelsetClient._PUBLISH_STATUS}
        self._labelset_post("updateLabelSetStatus", post_data)

    @staticmethod
    def _get_object_path(remote_path: str, segment_name: str, sensor_name: str) -> str:
        if not segment_name:
            return str(PurePosixPath(sensor_name, remote_path))
        return str(
            PurePosixPath(
                SegmentClientBase._SEGMENT_PATH_START,
                segment_name,
                SegmentClientBase._SEGMENT_PATH_END,
                sensor_name,
                remote_path,
            )
        )

    @staticmethod
    def create_metadata(label_tables: Union[LabelTable, List[LabelTable]]) -> Dict[str, Any]:
        """Return metadata created from the label table or the list of label tables.

        :return: A dict in metadata format
        """
        if isinstance(label_tables, LabelTable):
            label_tables = [label_tables]

        task_types = []
        for label_table in label_tables:
            if not label_table.categories:
                continue
            task_type = LabelsetClient._TASK_TYPE[label_table.label_type].copy()
            task_type["is_tracking"] = label_table.is_tracking
            task_type["categories"] = [{"nameEn": category} for category in label_table.categories]
            task_types.append(task_type)

        return {"taskTypes": task_types} if task_types else {}
