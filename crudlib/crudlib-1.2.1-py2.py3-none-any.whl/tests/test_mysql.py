#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/7/26
# Desc: 

from crudlib import MySQL

uri = "mysql+pymysql://root:root@localhost:3306/mysql?charset=utf8mb4"
my = MySQL(uri, debug=True)
my.create_db("test")
my.connection.db = "test"
test_table = "developers"
test_data = {"name": "zxyle", "age": 25, "address": "Hangzhou"}


def test_insert():
    my.drop_tb(test_table)
    my.create_tb(test_table)
    assert my.insert_one(test_table, test_data) is not None


def test_query():
    rows = my.query(test_table)
    row = rows[0]
    row.pop("id")
    row.pop("create_time")
    row.pop("modify_time")
    assert row == test_data


def test_update():
    update_data = {"age": 20}
    condition = {}
    my.update(test_table, update_data, condition)
    my.commit()

    rows = my.query(test_table)
    assert rows[0].get("age") == update_data.get("age")


def test_delete():
    condition = {}
    my.delete(test_table, condition)

    rows = my.query(test_table)
    assert rows == tuple()


def test_insert_many():
    pass


def test_rollback():
    my.insert_one(test_table, {"name": "zheng"})
    my.rollback()
    assert my.query(test_table, {"name": "zheng"}) == tuple()
