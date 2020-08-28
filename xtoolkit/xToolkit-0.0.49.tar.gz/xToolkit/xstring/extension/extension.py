#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/13 9:59
# @Author  : 熊利宏
# @project : xToolkit 字符串
# @Email   : xionglihong@163.com
# @File    : extension.py
# @IDE     : PyCharm
# @REMARKS : 字符串扩展功能

import emoji


# 字符串高级处理
class Extension(object):
    # emoji表情处理
    class EmojiAnalysis(object):
        """
        进行emoji表情处理
        """

        # 字符串转emoji表情
        @staticmethod
        def string_to_emoji(*args, **kwargs):
            """
            字符串转emoji表情
            """
            target = args[0]

            # 效验数据
            if target:
                raise ValueError("转换的字符串不能为空")

            return emoji.emojize(target)

        # emoji表情转字符串
        @staticmethod
        def emoji_to_string(*args, **kwargs):
            """
            字符串转emoji表情
            """
            target = args[0]

            # 效验数据
            if target:
                raise ValueError("转换的字符串不能为空")

            return emoji.demojize(target)

    # 中文分词
    class JiebaAnalysis(object):
        """
        进行中文分词
        """

        # 默认分词
        def jieba(self):
            pass
