#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : client.py
# @Author: encircles
# @Date  : 8/19/2020
# @Desc  :
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cvm.v20170312 import models

from srvmsdk.common.tencent.txbase import TxCommonBase
from srvmsdk.utils import ret_msg


class TxClient(TxCommonBase):
    # region 地域相关
    def DescribeRegions(self):
        """
        {
          "code": 0,
          "msg": null,
          "result": {
            "TotalCount": 20,
            "RegionSet": [
              {
                "Region": "ap-bangkok",
                "RegionName": "亚太地区(曼谷)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-beijing",
                "RegionName": "华北地区(北京)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-chengdu",
                "RegionName": "西南地区(成都)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-chongqing",
                "RegionName": "西南地区(重庆)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-guangzhou",
                "RegionName": "华南地区(广州)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-guangzhou-open",
                "RegionName": "华南地区(广州Open)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-hongkong",
                "RegionName": "港澳台地区(中国香港)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-mumbai",
                "RegionName": "亚太地区(孟买)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-nanjing",
                "RegionName": "华东地区(南京)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-seoul",
                "RegionName": "亚太地区(首尔)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-shanghai",
                "RegionName": "华东地区(上海)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-shanghai-fsi",
                "RegionName": "华东地区(上海金融)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-shenzhen-fsi",
                "RegionName": "华南地区(深圳金融)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-singapore",
                "RegionName": "东南亚地区(新加坡)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "ap-tokyo",
                "RegionName": "亚太地区(东京)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "eu-frankfurt",
                "RegionName": "欧洲地区(法兰克福)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "eu-moscow",
                "RegionName": "欧洲地区(莫斯科)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "na-ashburn",
                "RegionName": "美国东部(弗吉尼亚)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "na-siliconvalley",
                "RegionName": "美国西部(硅谷)",
                "RegionState": "AVAILABLE"
              },
              {
                "Region": "na-toronto",
                "RegionName": "北美地区(多伦多)",
                "RegionState": "AVAILABLE"
              }
            ],
            "RequestId": "0e01d885-f666-405d-9411-eb93c64049d2"
          }
        }

        查询地域列表
        :return:
        """
        try:

            # 实例化一个请求对象
            req = models.DescribeRegionsRequest()

            # 通过 client 对象调用想要访问的接口，需要传入请求对象
            resp = self.client.DescribeRegions(req)
            # 输出 json 格式的字符串回包
            # print(resp.to_json_string())
            return ret_msg(result=resp.to_json_string())

        except TencentCloudSDKException as err:
            # print(err)
            return ret_msg(err.code, err.message)

    def DescribeZones(self):
        """
        {
          "code": 0,
          "msg": null,
          "result": {
            "TotalCount": 2,
            "ZoneSet": [
              {
                "Zone": "ap-chengdu-1",
                "ZoneName": "成都一区",
                "ZoneId": "160001",
                "ZoneState": "AVAILABLE"
              },
              {
                "Zone": "ap-chengdu-2",
                "ZoneName": "成都二区",
                "ZoneId": "160002",
                "ZoneState": "AVAILABLE"
              }
            ],
            "RequestId": "6ed9c9e2-36b2-4688-a52a-396677b52586"
          }
        }
        查询可用区列表
        :return:
        """
        try:

            # 实例化一个请求对象
            req = models.DescribeZonesRequest()

            # 通过 client 对象调用想要访问的接口，需要传入请求对象
            resp = self.client.DescribeZones(req)
            # 输出 json 格式的字符串回包
            # print(resp.to_json_string())
            return ret_msg(result=resp.to_json_string())

        except TencentCloudSDKException as err:
            # print(err)
            return ret_msg(err.code, err.message)

    # endregion

    # region 实例相关
    def RunInstances(self, params_json_str) -> dict:
        """
        创建实例
        https://cloud.tencent.com/document/api/213/15730
        :param params_json_str:
        :return:
        """
        try:
            req = models.RunInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.RunInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceRunInstances(self, params_json_str) -> dict:
        """
        创建实例询价
        https://cloud.tencent.com/document/api/213/15726
        :return:
        """
        try:

            req = models.InquiryPriceRunInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceRunInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def StartInstances(self, params_json_str) -> dict:
        """
        启动实例
        https://cloud.tencent.com/document/api/213/15735
        :return:
        """
        try:
            req = models.StartInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.StartInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def StopInstances(self, params_json_str) -> dict:
        """
        关闭实例
        https://cloud.tencent.com/document/api/213/15743
        :return:
        """
        try:
            req = models.StopInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.StopInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def RebootInstances(self, params_json_str) -> dict:
        """
        重启实例
        https://cloud.tencent.com/document/api/213/15742
        :return:
        """
        try:
            req = models.RebootInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.RebootInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ResetInstance(self, params_json_str) -> dict:
        """
        重装实例
        https://cloud.tencent.com/document/api/213/15724
        :return:
        """
        try:
            req = models.ResetInstanceRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ResetInstance(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceResetInstance(self, params_json_str) -> dict:
        """
        NAME:重装实例询价
        LINK:https://cloud.tencent.com/document/api/213/15747
        :return:
        """
        try:
            req = models.InquiryPriceResetInstanceRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceResetInstance(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ResetInstancesPassword(self, params_json_str) -> dict:
        """
        NAME:重置实例密码
        LINK:https://cloud.tencent.com/document/api/213/15736
        :return:
        """
        try:
            req = models.ResetInstancesPasswordRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ResetInstancesPassword(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def TerminateInstances(self, params_json_str) -> dict:
        """
        NAME:退还实例
        LINK:https://cloud.tencent.com/document/api/213/15723
        :return:
        """
        try:
            req = models.TerminateInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.TerminateInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstances(self, params_json_str) -> dict:
        """
        NAME:查看实例列表
        LINK:https://cloud.tencent.com/document/api/213/15728
        :return:
        """
        try:
            req = models.DescribeInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstancesStatus(self, params_json_str) -> dict:
        """
        NAME:查看实例状态列表
        LINK:https://cloud.tencent.com/document/api/213/15738
        :return:
        """
        try:
            req = models.DescribeInstancesStatusRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstancesStatus(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyInstancesAttribute(self, params_json_str) -> dict:
        """
        NAME:修改实例的属性
        LINK:https://cloud.tencent.com/document/api/213/15739
        :return:
        """
        try:
            req = models.ModifyInstancesAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyInstancesAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyInstancesProject(self, params_json_str) -> dict:
        """
        NAME:修改实例所属项目
        LINK:https://cloud.tencent.com/document/api/213/15746
        :return:
        """
        try:
            req = models.ModifyInstancesProjectRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyInstancesProject(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ResetInstancesType(self, params_json_str) -> dict:
        """
        NAME:调整实例配置
        LINK:https://cloud.tencent.com/document/api/213/15744
        :return:
        """
        try:
            req = models.ResetInstancesTypeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ResetInstancesType(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceResetInstancesType(self, params_json_str) -> dict:
        """
        NAME:调整实例配置询价
        LINK:https://cloud.tencent.com/document/api/213/15733
        :return:
        """
        try:
            req = models.InquiryPriceResetInstancesTypeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceResetInstancesType(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ResizeInstanceDisks(self, params_json_str) -> dict:
        """
        NAME:扩容实例磁盘
        LINK:https://cloud.tencent.com/document/api/213/15731
        :return:
        """
        try:
            req = models.ResizeInstanceDisksRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ResizeInstanceDisks(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceResizeInstanceDisks(self, params_json_str) -> dict:
        """
        NAME:扩容实例磁盘询价
        LINK:https://cloud.tencent.com/document/api/213/15751
        :return:
        """
        try:
            req = models.InquiryPriceResizeInstanceDisksRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceResizeInstanceDisks(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstanceFamilyConfigs(self, params_json_str) -> dict:
        """
        NAME:查询所支持的实例机型族信息
        LINK:https://cloud.tencent.com/document/api/213/15748
        :return:
        """
        try:
            req = models.DescribeInstanceFamilyConfigsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstanceFamilyConfigs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstanceTypeConfigs(self, params_json_str) -> dict:
        """
        NAME:查询实例机型列表
        LINK:https://cloud.tencent.com/document/api/213/15749
        :return:
        """
        try:
            req = models.DescribeInstanceTypeConfigsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstanceTypeConfigs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def RenewInstances(self, params_json_str) -> dict:
        """
        NAME:续费实例
        LINK:https://cloud.tencent.com/document/api/213/15740
        :return:
        """
        try:
            req = models.RenewInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.RenewInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceRenewInstances(self, params_json_str) -> dict:
        """
        NAME:续费实例询价
        LINK:https://cloud.tencent.com/document/api/213/15725
        :return:
        """
        try:
            req = models.InquiryPriceRenewInstancesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceRenewInstances(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyInstancesRenewFlag(self, params_json_str) -> dict:
        """
        NAME:修改实例续费标识
        LINK:https://cloud.tencent.com/document/api/213/15752
        :return:
        """
        try:
            req = models.ModifyInstancesRenewFlagRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyInstancesRenewFlag(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeZoneInstanceConfigInfos(self, params_json_str) -> dict:
        """
        NAME:获取可用区机型配置信息
        LINK:https://cloud.tencent.com/document/api/213/17378
        :return:
        """
        try:
            req = models.DescribeZoneInstanceConfigInfosRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeZoneInstanceConfigInfos(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstanceVncUrl(self, params_json_str) -> dict:
        """
        NAME:查询实例管理终端地址
        LINK:https://cloud.tencent.com/document/api/213/18150
        :return:
        """
        try:
            req = models.DescribeInstanceVncUrlRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstanceVncUrl(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInstancesOperationLimit(self, params_json_str) -> dict:
        """
        NAME:查询实例操作限制
        LINK:https://cloud.tencent.com/document/api/213/34316
        :return:
        """
        try:
            req = models.DescribeInstancesOperationLimitRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstancesOperationLimit(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceModifyInstancesChargeType(self, params_json_str) -> dict:
        """
        NAME:修改实例计费模式询价
        LINK:https://cloud.tencent.com/document/api/213/17965
        :return:
        """
        try:
            req = models.InquiryPriceModifyInstancesChargeTypeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceModifyInstancesChargeType(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyInstancesChargeType(self, params_json_str) -> dict:
        """
        NAME:修改实例计费模式
        LINK:https://cloud.tencent.com/document/api/213/17964
        :return:
        """
        try:
            req = models.ModifyInstancesChargeTypeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyInstancesChargeType(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 镜像相关
    def CreateImage(self, params_json_str) -> dict:
        """
        NAME:创建镜像
        LINK:https://cloud.tencent.com/document/api/213/16726
        :return:
        """
        try:
            req = models.CreateImageRequest()
            req.from_json_string(params_json_str)

            resp = self.client.CreateImage(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DeleteImages(self, params_json_str) -> dict:
        """
        NAME:删除镜像
        LINK:https://cloud.tencent.com/document/api/213/15716
        :return:
        """
        try:
            req = models.DeleteImagesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DeleteImages(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyImageAttribute(self, params_json_str) -> dict:
        """
        NAME:修改镜像属性
        LINK:https://cloud.tencent.com/document/api/213/15713
        :return:
        """
        try:
            req = models.ModifyImageAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyImageAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeImages(self, params_json_str) -> dict:
        """
        NAME:查看镜像列表
        LINK:https://cloud.tencent.com/document/api/213/15715
        :return:
        """
        try:
            req = models.DescribeImagesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeImages(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ImportImage(self, params_json_str) -> dict:
        """
        NAME:外部镜像导入
        LINK:https://cloud.tencent.com/document/api/213/15717
        :return:
        """
        try:
            req = models.ImportImageRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ImportImage(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeImportImageOs(self, params_json_str) -> dict:
        """
        NAME:查询外部导入镜像支持的OS列表
        LINK:https://cloud.tencent.com/document/api/213/15718
        :return:
        """
        try:
            req = models.DescribeImportImageOsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeImportImageOs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeImageSharePermission(self, params_json_str) -> dict:
        """
        NAME:查看镜像分享信息
        LINK:https://cloud.tencent.com/document/api/213/15712
        :return:
        """
        try:
            req = models.DescribeImageSharePermissionRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeImageSharePermission(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyImageSharePermission(self, params_json_str) -> dict:
        """
        NAME:修改镜像分享信息
        LINK:https://cloud.tencent.com/document/api/213/15710
        :return:
        """
        try:
            req = models.ModifyImageSharePermissionRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyImageSharePermission(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def SyncImages(self, params_json_str) -> dict:
        """
        NAME:同步镜像
        LINK:https://cloud.tencent.com/document/api/213/15711
        :return:
        """
        try:
            req = models.SyncImagesRequest()
            req.from_json_string(params_json_str)

            resp = self.client.SyncImages(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeImageQuota(self, params_json_str) -> dict:
        """
        NAME:查询镜像配额上限
        LINK:https://cloud.tencent.com/document/api/213/15719
        :return:
        """
        try:
            req = models.DescribeImageQuotaRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeImageQuota(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 密钥相关
    def CreateKeyPair(self, params_json_str) -> dict:
        """
        NAME:创建密钥对
        LINK:https://cloud.tencent.com/document/api/213/15702
        :return:
        """
        try:
            req = models.CreateKeyPairRequest()
            req.from_json_string(params_json_str)

            resp = self.client.CreateKeyPair(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DeleteKeyPairs(self, params_json_str) -> dict:
        """
        NAME:删除密钥对
        LINK:https://cloud.tencent.com/document/api/213/15700
        :return:
        """
        try:
            req = models.DeleteKeyPairsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DeleteKeyPairs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyKeyPairAttribute(self, params_json_str) -> dict:
        """
        NAME:修改密钥对属性
        LINK:https://cloud.tencent.com/document/api/213/15701
        :return:
        """
        try:
            req = models.ModifyKeyPairAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyKeyPairAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def AssociateInstancesKeyPairs(self, params_json_str) -> dict:
        """
        NAME:绑定密钥对
        LINK:https://cloud.tencent.com/document/api/213/15698
        :return:
        """
        try:
            req = models.AssociateInstancesKeyPairsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.AssociateInstancesKeyPairs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DisassociateInstancesKeyPairs(self, params_json_str) -> dict:
        """
        NAME:解绑密钥对
        LINK:https://cloud.tencent.com/document/api/213/15697
        :return:
        """
        try:
            req = models.DisassociateInstancesKeyPairsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DisassociateInstancesKeyPairs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeKeyPairs(self, params_json_str) -> dict:
        """
        NAME:查询密钥对列表
        LINK:https://cloud.tencent.com/document/api/213/15699
        :return:
        """
        try:
            req = models.DescribeKeyPairsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeKeyPairs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ImportKeyPair(self, params_json_str) -> dict:
        """
        NAME:导入密钥对
        LINK:https://cloud.tencent.com/document/api/213/15703
        :return:
        """
        try:
            req = models.ImportKeyPairRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ImportKeyPair(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 专用宿主机相关
    def AllocateHosts(self, params_json_str) -> dict:
        """
        NAME:创建CDH实例
        LINK:https://cloud.tencent.com/document/api/213/16473
        :return:
        """
        try:
            req = models.AllocateHostsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.AllocateHosts(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeHosts(self, params_json_str) -> dict:
        """
        NAME:查看CDH实例列表
        LINK:https://cloud.tencent.com/document/api/213/16474
        :return:
        """
        try:
            req = models.DescribeHostsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeHosts(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyHostsAttribute(self, params_json_str) -> dict:
        """
        NAME:修改CDH实例的属性
        LINK:https://cloud.tencent.com/document/api/213/16475
        :return:
        """
        try:
            req = models.ModifyHostsAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyHostsAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def RenewHosts(self, params_json_str) -> dict:
        """
        NAME:续费CDH实例
        LINK:https://cloud.tencent.com/document/api/213/16476
        :return:
        """
        try:
            req = models.RenewHostsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.RenewHosts(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 安全组相关接口
    def AssociateSecurityGroups(self, params_json_str) -> dict:
        """
        NAME:绑定安全组
        LINK:https://cloud.tencent.com/document/api/213/31282
        :return:
        """
        try:
            req = models.AssociateSecurityGroupsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.AssociateSecurityGroups(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DisassociateSecurityGroups(self, params_json_str) -> dict:
        """
        NAME:解绑安全组
        LINK:https://cloud.tencent.com/document/api/213/31281
        :return:
        """
        try:
            req = models.DisassociateSecurityGroupsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DisassociateSecurityGroups(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 网络相关接口
    def DescribeInstanceInternetBandwidthConfigs(self, params_json_str) -> dict:
        """
        NAME:查询实例带宽配置
        LINK:https://cloud.tencent.com/document/api/213/15734
        :return:
        """
        try:
            req = models.DescribeInstanceInternetBandwidthConfigsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInstanceInternetBandwidthConfigs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeInternetChargeTypeConfigs(self, params_json_str) -> dict:
        """
        NAME:查询网络计费类型
        LINK:https://cloud.tencent.com/document/api/213/15729
        :return:
        """
        try:
            req = models.DescribeInternetChargeTypeConfigsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeInternetChargeTypeConfigs(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def InquiryPriceResetInstancesInternetMaxBandwidth(self, params_json_str) -> dict:
        """
        NAME:调整实例带宽上限询价
        LINK:https://cloud.tencent.com/document/api/213/15732
        :return:
        """
        try:
            req = models.InquiryPriceResetInstancesInternetMaxBandwidthRequest()
            req.from_json_string(params_json_str)

            resp = self.client.InquiryPriceResetInstancesInternetMaxBandwidth(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyInstancesVpcAttribute(self, params_json_str) -> dict:
        """
        NAME:修改实例vpc属性
        LINK:https://cloud.tencent.com/document/api/213/15750
        :return:
        """
        try:
            req = models.ModifyInstancesVpcAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyInstancesVpcAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ResetInstancesInternetMaxBandwidth(self, params_json_str) -> dict:
        """
        NAME:调整实例带宽上限
        LINK:https://cloud.tencent.com/document/api/213/15721
        :return:
        """
        try:
            req = models.ResetInstancesInternetMaxBandwidthRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ResetInstancesInternetMaxBandwidth(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion

    # region 置放群组相关接口
    def CreateDisasterRecoverGroup(self, params_json_str) -> dict:
        """
        NAME:创建分散置放群组
        LINK:https://cloud.tencent.com/document/api/213/17813
        :return:
        """
        try:
            req = models.CreateDisasterRecoverGroupRequest()
            req.from_json_string(params_json_str)

            resp = self.client.CreateDisasterRecoverGroup(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DeleteDisasterRecoverGroups(self, params_json_str) -> dict:
        """
        NAME:删除分散置放群组
        LINK:https://cloud.tencent.com/document/api/213/17812
        :return:
        """
        try:
            req = models.DeleteDisasterRecoverGroupsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DeleteDisasterRecoverGroups(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeDisasterRecoverGroupQuota(self, params_json_str) -> dict:
        """
        NAME:查询置放群组配额
        LINK:https://cloud.tencent.com/document/api/213/17811
        :return:
        """
        try:
            req = models.DescribeDisasterRecoverGroupQuotaRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeDisasterRecoverGroupQuota(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def DescribeDisasterRecoverGroups(self, params_json_str) -> dict:
        """
        NAME:查询分散置放群组信息
        LINK:https://cloud.tencent.com/document/api/213/17810
        :return:
        """
        try:
            req = models.DescribeDisasterRecoverGroupsRequest()
            req.from_json_string(params_json_str)

            resp = self.client.DescribeDisasterRecoverGroups(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    def ModifyDisasterRecoverGroupAttribute(self, params_json_str) -> dict:
        """
        NAME:修改分散置放群组属性
        LINK:https://cloud.tencent.com/document/api/213/17809
        :return:
        """
        try:
            req = models.ModifyDisasterRecoverGroupAttributeRequest()
            req.from_json_string(params_json_str)

            resp = self.client.ModifyDisasterRecoverGroupAttribute(req)

            return ret_msg(result=resp.to_json_string())
        except TencentCloudSDKException as err:
            return ret_msg(err.code, err.message)

    # endregion
