#!/usr/bin/python3
# -*- coding:utf-8 -*-
import xmltodict
from smart_tag_tools.LinqTool import linq


class FieldHandler:
    """
    适用结构：字典列表嵌套结构
    """

    @classmethod
    def update_field_value(cls, val, **fields):
        """
        修改字段值
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[field] = v

            for key in val:
                cls.update_field_value(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_value(item, **fields)

    @classmethod
    def update_field_name(cls, val, **fields):
        """
        修改字段名
        :param val:
        :param fields:
        :return:
        """
        if isinstance(val, dict):
            for field, v in fields.items():
                if field in val:
                    val[v] = val.pop(field)

            for key in val:
                cls.update_field_name(val[key], **fields)

        if isinstance(val, list):
            for item in val:
                cls.update_field_name(item, **fields)

    @classmethod
    def remove_field(cls, val, *fields):
        """
        删除字段（递归）
        @param val:
        @param fields:
        @return:
        """
        if isinstance(val, dict):
            for field in fields:
                val.pop(field, "404")

            for key in val:
                cls.remove_field(val[key], *fields)

        if isinstance(val, list):
            for item in val:
                cls.remove_field(item, *fields)

    @classmethod
    def add_field(cls, val, **fields):
        """
        添加字段,只针对列表
        :param val:
        :param fields:
        :return:
        """

        if isinstance(val, list):
            for item in val:
                for field, v in fields.items():
                    item[field] = v


class MetadataConverter:
    """
    元数据结构字段调整
    """

    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.converts = xmltodict.parse(f.read())

    @staticmethod
    def prepare(data):
        for meta in data['metadatas']:
            if 'markmeta' in meta['type']:
                meta['type'] = 'model_sobey_object_markkeyframe'
                meta['name'] = 'model_sobey_object_markkeyframe'
                break

    def convert(self, meta, **kwargs):
        meta_type = meta['type']
        meta_type = meta_type[:-1].split('_')[-1] if meta_type.endswith('_') else meta_type.split('_')[-1]
        converter = linq(self.converts['collection']['field']).group_by('type').get(meta_type, [])
        for item in converter:
            before, after = item['before'], item['after']
            if before:
                if after:
                    FieldHandler.update_field_name(meta, before=after)
                else:
                    FieldHandler.remove_field(meta, before)
            else:
                FieldHandler.add_field(meta['metadata'], after=kwargs.get(after))
