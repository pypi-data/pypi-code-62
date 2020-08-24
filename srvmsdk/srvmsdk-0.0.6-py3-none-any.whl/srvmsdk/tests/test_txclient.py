#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_txclient.py
# @Author: encircles
# @Date  : 8/20/2020
# @Desc  :
import json
import unittest
from unittest import TestCase
from decouple import config
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from srvmsdk.app.client import get_client

if __name__ == '__main__':
    unittest.main()


class TestTxClient(TestCase):

    def setUp(self) -> None:
        self.secret_id = config('S_ID', default=None)
        self.secret_key = config('S_KEY', default=None)
        self.region = config('REGION', default=None)

    def test_describe_regions(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        res = t.DescribeRegions()
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_zones(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        res = t.DescribeZones()
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_run_instances(self):
        tencent = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            'Placement': {
                'Zone': config('ZONE')
            },
            'ImageId': config('IMAGE_ID')
            # ...
        }
        params = json.dumps(p)

        # 修改client的profile
        http_profile = HttpProfile()
        http_profile.endpoint = 'cvm.tencentcloudapi.com'
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        tencent.client.profile = client_profile

        res = tencent.RunInstances(params)
        # print(res.get('msg'))
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_run_instances(self):
        tencent = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            'Placement': {
                'Zone': config('ZONE')
            },
            'ImageId': config('IMAGE_ID')
            # ...
        }
        params = json.dumps(p)

        res = tencent.InquiryPriceRunInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_start_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceIds": [
                config('INSTANCE_ID')
            ]
        }
        params = json.dumps(p)

        print(params)

        res = t.StartInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_stop_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceIds": [
                config('INSTANCE_ID')
            ]
        }
        params = json.dumps(p)

        res = t.StopInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_reboot_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceIds": [
                config('INSTANCE_ID')
            ]
        }
        params = json.dumps(p)

        res = t.RebootInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_reset_instance(self):
        # TODO 未测试
        self.fail()

    def test_inquiry_price_reset_instance(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceId": config('INSTANCE_ID')
        }
        params = json.dumps(p)

        res = t.InquiryPriceResetInstance(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_reset_instances_password(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceIds": [config('INSTANCE_ID')],
            # "Password": "testpassword",
        }
        params = json.dumps(p)

        res = t.ResetInstancesPassword(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_terminate_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {
            "InstanceIds": [config('INSTANCE_ID') + '123123'],
        }
        params = json.dumps(p)

        res = t.TerminateInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instances_status(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstancesStatus(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_instances_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyInstancesAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_instances_project(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyInstancesProject(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_reset_instances_type(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ResetInstancesType(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_reset_instances_type(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.InquiryPriceResetInstancesType(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_resize_instance_disks(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ResizeInstanceDisks(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_resize_instance_disks(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.InquiryPriceResizeInstanceDisks(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instance_family_configs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstanceFamilyConfigs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instance_type_configs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstanceTypeConfigs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_renew_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.RenewInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_renew_instances(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.InquiryPriceRenewInstances(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_instances_renew_flag(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyInstancesRenewFlag(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_zone_instance_config_infos(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeZoneInstanceConfigInfos(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instance_vnc_url(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstanceVncUrl(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instances_operation_limit(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstancesOperationLimit(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_modify_instances_charge_type(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.InquiryPriceModifyInstancesChargeType(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_instances_charge_type(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyInstancesChargeType(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_create_image(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.CreateImage(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_delete_images(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DeleteImages(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_image_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyImageAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_images(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeImages(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_import_image(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ImportImage(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_import_image_os(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeImportImageOs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_image_share_permission(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeImageSharePermission(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_image_share_permission(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyImageSharePermission(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_sync_images(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.SyncImages(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_image_quota(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeImageQuota(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_create_key_pair(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.CreateKeyPair(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_delete_key_pairs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DeleteKeyPairs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_key_pair_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyKeyPairAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_associate_instances_key_pairs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.AssociateInstancesKeyPairs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_disassociate_instances_key_pairs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DisassociateInstancesKeyPairs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_key_pairs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeKeyPairs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_import_key_pair(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ImportKeyPair(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_allocate_hosts(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.AllocateHosts(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_hosts(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeHosts(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_hosts_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyHostsAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_renew_hosts(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.RenewHosts(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_associate_security_groups(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.AssociateSecurityGroups(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_disassociate_security_groups(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DisassociateSecurityGroups(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_instance_internet_bandwidth_configs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInstanceInternetBandwidthConfigs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_internet_charge_type_configs(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeInternetChargeTypeConfigs(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_inquiry_price_reset_instances_internet_max_bandwidth(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.InquiryPriceResetInstancesInternetMaxBandwidth(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_instances_vpc_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyInstancesVpcAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_reset_instances_internet_max_bandwidth(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ResetInstancesInternetMaxBandwidth(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_create_disaster_recover_group(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.CreateDisasterRecoverGroup(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_delete_disaster_recover_groups(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DeleteDisasterRecoverGroups(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_disaster_recover_group_quota(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeDisasterRecoverGroupQuota(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_describe_disaster_recover_groups(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.DescribeDisasterRecoverGroups(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))

    def test_modify_disaster_recover_group_attribute(self):
        t = get_client('tencent', secret_id=self.secret_id, secret_key=self.secret_key, region=self.region)

        p = {}
        params = json.dumps(p)

        res = t.ModifyDisasterRecoverGroupAttribute(params)
        self.assertEqual(res.get('code'), 0, res.get('msg'))
