#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/7/25
# Desc: 


class DataBase:
    def query(self, tb, condition=None):
        raise NotImplementedError

    def insert_one(self, tb, doc):
        raise NotImplementedError

    def insert_many(self, tb, doc_list):
        raise NotImplementedError

    def update(self, tb, doc, condition):
        raise NotImplementedError
