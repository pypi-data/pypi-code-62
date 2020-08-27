#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DataSetBase, DataSet, FusionDataSet."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union

from ..dataset import FusionSegment, Segment
from ..label import LabelTable
from .exceptions import GASSegmentError
from .labelset import LabelsetClient
from .requests import Client, cancel_all_tasks_when_first_exception
from .segment import FusionSegmentClient, SegmentClient


class DatasetClientBase(Client):
    """This class defines the concept of a dataset and some operations on it.

    :param dataset_id: Dataset id
    :param gateway_url: The url of the gas website
    :param access_key: User's access key
    """

    _PUBLISH_STATUS = 7

    def __init__(self, dataset_id: str, access_key: str, gateway_url: str) -> None:
        super().__init__(access_key, gateway_url)
        self._dataset_id = dataset_id

    def upload_description(
        self,
        description: Optional[str] = None,
        collection_time: Optional[str] = None,
        collection_location: Optional[str] = None,
    ) -> None:
        """Upload description of the dataset.

        :param description: description of the dataset to upload
        :param collection_time: collected time of the dataset to upload
        :param collection_location: collected location of the dataset to upload
        """
        post_data = {}
        if description:
            post_data["desc"] = description
        if collection_time:
            post_data["collectedAt"] = collection_time
        if collection_location:
            post_data["collectedLocation"] = collection_location

        if not post_data:
            return

        post_data["contentSetId"] = self._dataset_id
        self._dataset_post("updateContentSet", post_data)

    def get_dataset_id(self) -> str:
        """Get the id of this dataset."""
        return self._dataset_id

    def create_labelset(
        self,
        label_table: Union[LabelTable, List[LabelTable]],
        remote_paths: Optional[List[str]] = None,
        labelset_type: int = LabelsetClient.TYPE_GROUND_TRUTH,
    ) -> LabelsetClient:
        """Create a labelset.

        :param label_table: A LabelTable or a list of LabelTables covers all labels of the labelset
        :param remote_paths: A list of remote paths
        :param labelset_type: the type of the labelset to be created
        :return: Created labelset
        """
        post_data = {
            "contentSetId": self._dataset_id,
            "type": labelset_type,
            "version": "v1.0.2",
        }
        metadata = LabelsetClient.create_metadata(label_table)
        if metadata:
            post_data["meta"] = metadata
        if remote_paths:
            post_data["objectPaths"] = remote_paths

        data = self._labelset_post("createLabelSet", post_data)
        labelset_id = data["labelSetId"]
        return LabelsetClient(labelset_id, self._access_key, self._gateway_url)

    def delete_labelset(self, labelset_id: str) -> None:
        """Delete a labelset according to a labelset id.

        :param labelset_id: The id of the labelset to be deleted
        """
        post_data = {"labelSetId": labelset_id}
        self._labelset_post("deleteLabelSet", post_data)

    def list_labelsets(self) -> List[str]:
        """List ids of all labelsets of the dataset.

        :return: A list of labelsets ids
        """
        labelset_ids = []
        for summary in self._list_labelset_summaries():
            labelset_ids.append(summary["id"])
        return labelset_ids

    def publish(self) -> None:
        """Publish a dataset."""
        post_data = {"contentSetId": self._dataset_id, "status": DatasetClientBase._PUBLISH_STATUS}
        self._dataset_post("updateContentSet", post_data)

    def is_published(self) -> bool:
        """Gheck whether the dataset is published.

        :return: Return true if the dataset is publish, viceversa.
        """
        post_data = {"contentSetId": self._dataset_id}
        data = self._dataset_post("listContentSets", post_data)
        return (  # type: ignore[no-any-return]
            data["contentSets"][0]["contentSetResp"]["status"] == DatasetClientBase._PUBLISH_STATUS
        )

    def list_segments(self) -> List[str]:
        """List all segment names in a dataset.

        :return: A list of segment names
        """
        return self._list_segments()

    def _list_segments(self, segment_names: Optional[List[str]] = None) -> List[str]:
        post_data: Dict[str, Any] = {"contentSetId": self._dataset_id, "pageSize": -1}
        if segment_names:
            post_data["names"] = segment_names
        data = self._dataset_post("listSegments", post_data)
        return [segment_info["name"] for segment_info in data["segments"]]

    def delete_segments(
        self, segment_names: Union[str, List[str]], force_delete: bool = False
    ) -> None:
        """Delete segments according to the name list.

        :param name: A single segment Name or a list of the segment names, if empty, the default
        segment will be deleted, if you want to delete all segment, "_all" should be submitted.
        :param force_delete: By default, only segment with no sensor can be deleted.
        If force_delete is true, then sensor and its objects will also be deleted
        """
        if not isinstance(segment_names, list):
            segment_names = [segment_names]
        post_data = {
            "contentSetId": self._dataset_id,
            "names": segment_names,
            "forceDelete": force_delete,
        }
        self._dataset_post("deleteSegments", post_data)

    def _list_labelset_summaries(self) -> List[Any]:
        """List summaries of all labelsets.

        :return: A list of dictionaries containing all the labelset summaries.
        """
        post_data = {"contentSetId": self._dataset_id}
        data = self._labelset_post("listLabelSetSummaries", post_data)
        return data["labelSetSummaries"]  # type: ignore[no-any-return]


class DatasetClient(DatasetClientBase):
    """dataset has only one sensor, supporting create segment."""

    def get_or_create_segment(self, name: str) -> SegmentClient:
        """Create a segment set according to its name.

        :param name: Segment name, can be neither "_all" nor ""
        :return: Created segment
        """
        if not self._list_segments([name]):
            post_data = {"contentSetId": self._dataset_id, "name": name}
            self._dataset_post("createOrUpdateSegment", post_data)
        return SegmentClient(name, self._dataset_id, self._access_key, self._gateway_url)

    def get_segment(self, name: str) -> SegmentClient:
        """Get a segment according to its name.

        :param name: The name of the desired segment
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment
        """
        if not self._list_segments([name]):
            raise GASSegmentError(name)
        return SegmentClient(name, self._dataset_id, self._access_key, self._gateway_url)

    def upload_segment_object(
        self, segment: Segment, *, jobs: int = 1, continues: bool = False
    ) -> SegmentClient:
        """Upload a `Segment` to the dataset,
        This function will upload all info contains in the input `Segment` object,
        which includes:
        - Create a segment using the name of input `Segment`
        - Upload all `Data` in the Segment to the dataset

        :param segment: The `Segment` object contains the information needs to be upload
        :param jobs: The number of the max workers in multithread upload
        :param continues: Breakpoint continue upload, set it to True to skip the uploaded file
        :return: The `SegmentClient` used for uploading the data in the `Segment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        if continues:
            done_set = set(segment_client.list_data())

        with ThreadPoolExecutor(jobs) as executor:
            futures = []
            for data in segment:
                if continues and data.remote_path in done_set:
                    continue

                futures.append(executor.submit(segment_client.upload_data_object, data))

            cancel_all_tasks_when_first_exception(futures)

        return segment_client


class FusionDatasetClient(DatasetClientBase):
    """Client for fusion dataset which has multiple sensors,
    supporting create fusion segment.
    """

    def get_or_create_segment(self, name: str) -> FusionSegmentClient:
        """Create a fusion segment set according to the given name.

        :param name: Segment name, can be neither "_all" nor ""
        :return: Created fusion segment
        """
        if not self._list_segments([name]):
            post_data = {"contentSetId": self._dataset_id, "name": name}
            self._dataset_post("createOrUpdateSegment", post_data)
        return FusionSegmentClient(name, self._dataset_id, self._access_key, self._gateway_url)

    def get_segment(self, name: str) -> FusionSegmentClient:
        """Get a fusion segment according to its name.

        :param name: The name of the desired fusion segment
        :raises GASSegmentError: When the required fusion segment does not exist
        :return: The desired fusion segment
        """
        if self._list_segments([name]):
            return FusionSegmentClient(name, self._dataset_id, self._access_key, self._gateway_url)
        raise GASSegmentError(name)

    def upload_segment_object(
        self, segment: FusionSegment, *, jobs: int = 1, continues: bool = False
    ) -> FusionSegmentClient:
        """Upload a `FusionSegment` to the dataset,
        This function will upload all info contains in the input `FusionSegment` object,
        which includes:
        - Create a segment using the name of input `FusionSegment`
        - Upload all `Sensor` in the segment to the dataset
        - Upload all `Frame` in the segment to the dataset

        :param segment: The `Segment` object needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :param continues: Breakpoint continue upload, set it to True to skip the uploaded file
        :return: The `FusionSegmentClient` used for uploading the data in the `FusionSegment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        sensors = segment.get_sensors()
        for sensor in sensors.values():
            segment_client.upload_sensor_object(sensor)

        if continues:
            done_frame_dict = (
                segment_client._list_frame_objects_dict()  # pylint: disable=protected-access
            )

        with ThreadPoolExecutor(jobs) as executor:
            futures = []
            for i, frame in enumerate(segment):
                if continues and i in done_frame_dict:
                    remote_frame, frame_id = done_frame_dict[i]
                    if len(remote_frame) == len(frame):
                        continue

                    segment_client._delete_frames(frame_id)  # pylint: disable=protected-access

                futures.append(executor.submit(segment_client.upload_frame_object, frame, i))

            cancel_all_tasks_when_first_exception(futures)

        return segment_client
