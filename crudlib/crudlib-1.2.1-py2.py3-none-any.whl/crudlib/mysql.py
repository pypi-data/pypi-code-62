#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/7/25
# Desc: MySQL

import re

import pymysql

from crudlib.base import DataBase
from crudlib.config import DEFAULT_MYSQL_URI
from crudlib.uri import UriParser


class MySQL(DataBase):
    def __init__(self, uri=None, debug=False):
        self.uri = uri or DEFAULT_MYSQL_URI
        u = UriParser(self.uri)
        self.connection = pymysql.connect(host=u.host,
                                          port=u.port,
                                          user=u.user,
                                          password=u.password,
                                          db=u.db,
                                          charset=u.params.get('charset', 'utf8mb4'),
                                          cursorclass=pymysql.cursors.DictCursor)
        self._open = False
        self.cursor = None
        self._debug = debug

    def insert_one(self, tb, doc):
        """
        Insert a record operation
        :param tb: mysql table name
        :param doc: {"name": "Zheng", "gender":"male"}
        :return:
        """
        # build sql
        fields, values = [], []
        for field, value in doc.items():
            fields.append(f"`{field}`")
            values.append(value)

        fields_sql = ", ".join(fields)
        values_sql = ", ".join(["%s" for _ in range(len(values))])
        sql = f"INSERT INTO `{tb}` ({fields_sql}) VALUES ({values_sql});"
        return self.execute(sql, values)

    def insert_many(self, tb, doc_list):
        """
        Insert multi records operation
        :param tb: mysql table name
        :param doc_list: [{}, {}, ...]
        :return:
        """
        for doc in doc_list:
            self.insert_one(tb, doc)

    def _get_cursor(self):
        """return cursor object"""
        if not self._open and not self.cursor:
            self.cursor = self.connection.cursor()
            self._open = True
        return self.cursor

    def execute(self, sql, data=None):
        """
        execute sql operation
        :param sql: SQL statement
        :param data:
        :return:
        """
        self._debug_info(sql, data)
        cursor = self._get_cursor()
        cursor.execute(sql, data)

        # TODO fetchall fetchone fetchmany
        return cursor.fetchall()

    def create_db(self, db_name=""):
        """Create Database operation"""
        if not db_name:
            raise ValueError("db name not allowed to be empty.")

        sql = f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
        self.execute(sql)
        self._debug_info("create database: `{}` success.".format(db_name))

    def drop_db(self, db_name=""):
        """Drop database operation"""
        sql = f"DROP DATABASE IF EXISTS {db_name};"
        self.execute(sql)
        self._debug_info("drop database: `{}` success.".format(db_name))

    def create_tb(self, tb=""):
        """Create table operation"""
        sql = f"""
        CREATE TABLE IF NOT EXISTS `{tb}`(
           id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
           create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           modify_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           name VARCHAR(20) NULL,
           age TINYINT UNSIGNED NULL,
           address VARCHAR(50) NULL
        )ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;"""
        self.execute(sql)
        self._debug_info("create table: `{}` success.".format(tb))

    def drop_tb(self, tb=""):
        """Drop table operation"""
        sql = f"DROP TABLE IF EXISTS {tb};"
        self.execute(sql)
        self._debug_info("drop table: `{}` success.".format(tb))

    def query(self, tb, condition=None):
        """Select records operation"""
        condition = condition or {}
        condition_sql, values = self._where(condition)

        # TODO replace *
        sql = f"SELECT * FROM `{tb}` {condition_sql};"
        results = self.execute(sql, values)
        return results

    def update(self, tb, doc, condition):
        """
        Update records operation
        :param tb:
        :param doc: {}
        :param condition: {}
        :return:
        """
        fields, values = [], []
        for field, value in doc.items():
            fields.append(f"`{field}`=%s")
            values.append(value)

        fields_sql = ", ".join(fields)

        condition_sql, v = self._where(condition)
        sql = f"UPDATE `{tb}` SET {fields_sql} {condition_sql};"
        self.execute(sql, values + v)
        self._debug_info("update success.")

    def delete(self, tb, condition=None):
        """Delete records operation"""
        condition = condition or {}
        condition_sql, values = self._where(condition)
        sql = f"DELETE FROM `{tb}` {condition_sql};"
        self.execute(sql, values)
        self._debug_info("delete success.")

    def group_by(self):
        pass

    def having(self):
        pass

    def limit(self):
        pass

    def _where(self, condition):
        """where statement parsing"""
        values = []
        if not condition:
            return "", values

        condition_list = []

        for k, v in condition.items():
            operator, v = self._parse(str(v))
            values.append(v)
            condition_list.append(f'{k}{operator}%s')

        condition_sql = " AND ".join(condition_list)
        return f"WHERE {condition_sql}", values

    @staticmethod
    def _parse(v):
        """parse where condition parameter"""
        pattern = re.findall(r"[>=<!]=?", v)
        if not pattern:
            return "=", v

        value = v.replace(pattern[0], "")
        if value.isnumeric():
            value = int(value)
        return pattern[0], value

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            self._debug_info(e)
            self.rollback()
        else:
            self._debug_info("commit success.")

    def rollback(self):
        self.connection.rollback()

    def create_trigger(self):
        sql = "create trigger tri before update on test.student for each row set NEW.modify_time=CURRENT_TIMESTAMP;"
        self.execute(sql)

    def create_view(self, name, sql):
        sql = f"create view {name} as {sql};"
        self.execute(sql)

    def _debug_info(self, *args):
        if self._debug:
            print(args)

    def __del__(self):
        """close connection and cursor"""
        self.commit()
        self._get_cursor().close()
        self.connection.close()

    def __repr__(self):
        expression = "version()"
        sql = f"SELECT {expression};"
        version = self.execute(sql)[0].get(expression)
        return "MySQL:<{}> at {}.".format(version, self.connection.host_info)
