# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.


class BaseMiniType(models.Model):
    class Meta:
        abstract = True

    # 属性清单 :: 在所有对象中，必须包含 [type, sequence, is_enabled]
    type = models.CharField(u'Type', max_length=20, default='BMTO', editable=False)

    created_at = models.DateTimeField(u'Created At', auto_now_add=True)
    updated_at = models.DateTimeField(u'Updated At', auto_now=True)
    comments = models.CharField(u'Comments', max_length=512, default='', blank=True, null=True)


class BaseType(BaseMiniType):
    class Meta:
        abstract = True

    # 属性清单 :: 在所有对象中，必须包含 [type, sequence, is_enabled]
    type = models.CharField(u'Type', max_length=20, default='BAMO', editable=False)

    # 属性清单 :: 在所有对象中，必须包含 [type, sequence, is_enabled]
    sequence = models.IntegerField(u'Sequence', default=0)
    is_enabled = models.BooleanField(u'Is Enabled', default=True)
    user_id = models.CharField(u'User ID', max_length=128, default='', blank=True, null=True, editable=False)
    user_name = models.CharField(u'User Name', max_length=128, default='', blank=True, null=True, editable=False)
    comments = models.CharField(u'Comments', max_length=512, default='', blank=True, null=True)


class BaseDocumentType(models.Model):
    class Meta:
        abstract = True

    # 属性清单 :: 在所有对象中，必须包含 [type, sequence, is_enabled]
    type = models.CharField(u'Type', max_length=20, default='BDOC', editable=False)

    # 属性清单 :: 在所有对象中，必须包含 [type, sequence, is_enabled]
    base_entity = models.IntegerField(u'Sequence', default=0)
    base_type = models.CharField(u'Base Type', max_length=20, default='', editable=False)
    status = models.CharField(u'Status', max_length=128, default='', blank=True, null=True, editable=False)


class ResponseBody:
    code = 0
    message = ""
    data = None

    def __init__(self, code=0, message="", data=None):
        self.code = code
        self.message = message
        self.data = data
