#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class GAS."""

from typing import Any, Dict, List, Optional, Type, Union, overload

from typing_extensions import Literal

from ..dataset import Dataset, FusionDataset
from .dataset import DatasetClient, FusionDatasetClient
from .exceptions import GASDatasetError, GASDatasetTypeError
from .requests import Client, get

DatasetClientType = Union[DatasetClient, FusionDatasetClient]


class GAS(Client):
    """This is a class defining the concept of TensorBay.
    It mainly defines some operations on datasets.

    :param access_key: user's access key
    :param url: the url of the gas website
    """

    _VERSIONS = {1: "COMMUNITY", 2: "ENTERPRISE"}

    def __init__(self, access_key: str, url: str = "https://gas.graviti.cn/") -> None:
        if url.endswith("/"):
            gateway_url = url + "gatewayv2/"
        else:
            gateway_url = url + "/gatewayv2/"

        super().__init__(access_key, gateway_url)

    def get_user_info(self) -> Dict[str, str]:
        """Get the user info corresponding to the AccessKey

        :return: A directory which contains the username and clientTag
        """
        post_data = {"token": self._access_key}
        url = self._gateway_url + "user/api/v3/token/get-user-profile"
        response = get(url, post_data)
        return {
            "username": response["userName"],
            "version": GAS._VERSIONS[response["clientTag"]],
        }

    @overload
    def create_dataset(self, name: str, is_fusion: Literal[False] = False) -> DatasetClient:
        ...

    @overload
    def create_dataset(self, name: str, is_fusion: Literal[True]) -> FusionDatasetClient:
        ...

    @overload
    def create_dataset(self, name: str, is_fusion: bool) -> DatasetClientType:
        ...

    def create_dataset(self, name: str, is_fusion: bool = False) -> DatasetClientType:
        """Create a dataset according to its name.

        :param name: dataset name, unique for a user
        :param is_fusion: if True, create a FusionDatasetClient, otherwise, create a DatasetClient
        :return: Created dataset
        """
        post_data = {
            "name": name,
            "contentSetType": int(is_fusion),  # segment: 0, fusion segment: 1
        }
        data = self._dataset_post("createContentSet", post_data)
        dataset_id = data["contentSetId"]
        ReturnType: Type[DatasetClientType] = FusionDatasetClient if is_fusion else DatasetClient
        return ReturnType(dataset_id, self._access_key, self._gateway_url)

    @overload
    def get_dataset(self, name: str, is_fusion: Literal[False] = False) -> DatasetClient:
        ...

    @overload
    def get_dataset(self, name: str, is_fusion: Literal[True]) -> FusionDatasetClient:
        ...

    @overload
    def get_dataset(self, name: str, is_fusion: bool) -> DatasetClientType:
        ...

    def get_dataset(self, name: str, is_fusion: bool = False) -> DatasetClientType:
        """Get a dataset according to its name.

        :param name: The name of the desired dataset
        :param is_fusion: if True, create a FusionDatasetClient, otherwise, create a DatasetClient
        :raises GASDatasetError: When the required dataset does not exist
        :raises GASDatasetTypeError: When required dataset type is inconsistent with actual type
        :return: The desired dataset
        """
        datasets_info = self._list_datasets_info(name)
        if not datasets_info:
            raise GASDatasetError(name)

        ReturnType: Type[DatasetClientType] = FusionDatasetClient if is_fusion else DatasetClient

        if is_fusion != datasets_info[0]["contentSetResp"]["contentSetType"]:
            raise GASDatasetTypeError(name, str(ReturnType))

        dataset_id = datasets_info[0]["contentSetResp"]["contentSetId"]
        return ReturnType(dataset_id, self._access_key, self._gateway_url)

    @overload
    def get_or_create_dataset(self, name: str, is_fusion: Literal[False] = False) -> DatasetClient:
        ...

    @overload
    def get_or_create_dataset(self, name: str, is_fusion: Literal[True]) -> FusionDatasetClient:
        ...

    @overload
    def get_or_create_dataset(self, name: str, is_fusion: bool) -> DatasetClientType:
        ...

    def get_or_create_dataset(self, name: str, is_fusion: bool = False) -> DatasetClientType:
        """Get a dataset if 'name' exists. Create one otherwise.

        :param name: The name of a dataset
        :param is_fusion: if True, create a FusionDatasetClient, otherwise, create a DatasetClient
        :return: created dataset
        """
        try:
            return self.get_dataset(name, is_fusion)
        except GASDatasetError:
            return self.create_dataset(name, is_fusion)

    @overload
    def upload_dataset_object(
        self, dataset: Dataset, *, jobs: int = 1, continues: bool = False
    ) -> DatasetClient:
        ...

    @overload
    def upload_dataset_object(
        self, dataset: FusionDataset, *, jobs: int = 1, continues: bool = False
    ) -> FusionDatasetClient:
        ...

    @overload
    def upload_dataset_object(
        self, dataset: Union[Dataset, FusionDataset], *, jobs: int = 1, continues: bool = False
    ) -> DatasetClientType:
        ...

    def upload_dataset_object(
        self, dataset: Union[Dataset, FusionDataset], *, jobs: int = 1, continues: bool = False
    ) -> DatasetClientType:
        """Upload a `Dataset` or `FusionDataset` to TensorBay,
        This function will upload all info contains in the `Dataset` or `FusionDataset` object,
        which includes:
        - Create a dataset using the name and type of input `Dataset` or `FusionDataset`,
        - Upload all `Segment` or `FusionSegment` in the dataset to TensorBay

        :param dataset: The `Dataset` or `FusionDataset` object needs to be uploaded.
        :param jobs: The number of the max workers in multithread upload
        :param continues: Breakpoint continue upload, set it to True to skip the uploaded file
        :return: The `DatasetClient` or `FusionDatasetClient` used for uploading the dataset
        """

        is_fusion = isinstance(dataset, FusionDataset)
        dataset_client = self.get_or_create_dataset(dataset.name, is_fusion)
        for segment in dataset:
            dataset_client.upload_segment_object(
                segment, jobs=jobs, continues=continues  # type: ignore[arg-type]
            )

        return dataset_client

    def list_datasets(self) -> List[str]:
        """List names of all datasets.

        :return: A list of names of all datasets
        """
        datasets_info = self._list_datasets_info()
        dataset_names: List[str] = []
        for dataset_info in datasets_info:
            dataset_name = dataset_info["contentSetResp"]["name"]
            dataset_names.append(dataset_name)
        return dataset_names

    def delete_dataset(self, name: str) -> None:
        """Delete a dataset according to its name.

        :param name: The name of the dataset to delete
        :raises GASDatasetError: When the required dataset does not exist
        """
        datasets_info = self._list_datasets_info(name)
        if not datasets_info:
            raise GASDatasetError(name)
        dataset_id = datasets_info[0]["contentSetResp"]["contentSetId"]
        post_data = {"contentSetId": dataset_id, "name": name}
        self._dataset_post("deleteContentSets", post_data)

    def _list_datasets_info(self, name: Optional[str] = None) -> List[Any]:
        """List info of all datasets.

        :param name: dataset name to list its info. If None, list info of all datasets
        :return: A list of dicts containing dataset info. If name does not exist,
            return an empty list.
        """
        post_data = {"name": name, "pageSize": -1}
        data = self._dataset_post("listContentSets", post_data)
        return data["contentSets"]  # type: ignore[no-any-return]
