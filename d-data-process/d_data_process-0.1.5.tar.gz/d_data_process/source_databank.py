# coding:utf-8
"""
Created on 2018年5月28日

@author: Damon
"""
import pandas as pd
import pymssql
import pymysql
import cx_Oracle
from sqlalchemy import create_engine
import os
import psycopg2

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class Pgsql_db:
    def __init__(self, host, port, user, password, data_base):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.data_base = data_base

    def read_pgsql(self, query):
        self.query = query
        database = psycopg2.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.data_base,
                                    port=self.port)
        cursor = database.cursor()
        data = pd.read_sql(self.query, database, )
        database.close()
        cursor.close()
        return data

    def execute_pgsql(self, query):
        self.query = query
        database = psycopg2.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.data_base,
                                    port=self.port)
        cursor = database.cursor()
        cursor.execute(self.query)
        database.commit()
        cursor.close()
        database.close()

    def insert_pgsql(self, data, table_name):
        self.data = data
        self.table_name = table_name
        database = create_engine('postgresql://' + self.user + ':' + self.password + '@' +
                                 self.host + ':' + str(self.port) + '/' + self.data_base)
        self.data.to_sql(self.table_name,
                         con=database,
                         index=False,
                         if_exists='append',
                         chunksize=10000)


# 连接mysql
class Mysql_db:
    def __init__(self, host, port, user, password, data_base):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.data_base = data_base

    def read_mysql(self, query):
        self.query = query
        database = pymysql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.data_base,
                                   port=self.port,
                                   charset='utf8')
        cursor = database.cursor()
        data = pd.read_sql(self.query, database, )
        database.close()
        cursor.close()
        return data

    def execute_mysql(self, query):
        self.query = query
        database = pymysql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   db=self.data_base,
                                   port=self.port,
                                   charset='utf8mb4')
        cursor = database.cursor()
        cursor.execute(self.query)
        database.commit()
        cursor.close()
        database.close()

    def insert_mysql(self, data, table_name):
        self.data = data
        self.table_name = table_name
        database = create_engine('mysql+pymysql://' + self.user + ':' + self.password + '@' +
                                 self.host + ':' + str(self.port) + '/' + self.data_base +
                                 '?charset=utf8mb4')
        data.to_sql(self.table_name,
                    con=database,
                    index=False,
                    if_exists='append',
                    chunksize=10000)

# 连接oracle


class Oracle_db:
    def __init__(self, host, user, password, service):
        self.host = host
        self.user = user
        self.password = password
        self.service = service

    def read_oracle(self, query):
        self.query = query
        database = cx_Oracle.connect(self.user + '/' + self.password + '@' + self.host + '/' +
                                     self.service)
        cursor = database.cursor()
        data = pd.read_sql(
            self.query,
            database,
        )
        database.close()
        cursor.close()
        return data

    def execute_oracle(self, query):
        self.query = query
        database = cx_Oracle.connect(self.user + '/' + self.password + '@' + self.host + '/' +
                                     self.service)
        cursor = database.cursor()
        cursor.execute(self.query)
        database.commit()
        cursor.close()
        database.close()

    def insert_oracle(self, data, table_name):
        self.data = data
        self.table_name = table_name
        database = create_engine('oracle://' + self.user + ':' + self.password + '@' + self.host +
                                 '/' + self.service)
        data.to_sql(self.table_name,
                    con=database,
                    index=False,
                    if_exists='append',
                    chunksize=10000)

# 连接sqlserver


class Sqlserver_db:
    def __init__(self, host, user, password, data_base):
        self.host = host
        self.user = user
        self.password = password
        self.data_base = data_base

    def read_sqlserver(self, query):
        self.query = query
        database = pymssql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.data_base,
                                   charset='utf8')
        cursor = database.cursor()
        data = pd.read_sql(
            self.query,
            database,
        )
        database.close()
        cursor.close()
        return data

    def execute_sqlserver(self, query):
        self.query = query
        database = pymssql.connect(host=self.host,
                                   user=self.user,
                                   password=self.password,
                                   database=self.data_base)
        cursor = database.cursor()
        cursor.execute(self.query)
        database.commit()
        cursor.close()
        database.close()

    def insert_sqlserver(self, data, table_name):
        self.data = data
        self.table_name = table_name
        database = create_engine('mssql+pymssql://' + self.user + ':' + self.password + '@' +
                                 self.host + '/' + self.data_base + '?charset=utf8')
        data.to_sql(self.table_name,
                    con=database,
                    index=False,
                    if_exists='append',
                    chunksize=10000)
