# coding: utf-8
"""
Created on 2018年5月28日

@author: Damon
"""

import pandas as pd
import chardet
from datetime import datetime
import xlrd


def mkdir(path):  # 判断目录是否存在，不存在则创建
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        #print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print(path + ' 目录已存在')
        return False


def check_coding(char_data):  # 判断字符编码类型
    if isinstance(char_data, bytes):
        pass
    else:
        char_data = char_data.encode()
    f_encoding = chardet.detect(char_data)
    return f_encoding['encoding']


class Excel_file:
    def f_read_excel(self, path, sheet_name=0, header=0):
        self.path = path
        self.sheet_name = sheet_name
        self.header = header
        data = pd.read_excel(
            self.path, sheet_name=self.sheet_name, header=self.header)
        return data

    def f_writer_excel(self, path, data, sheet_name):
        self.path = path
        self.data = data
        self.sheet_name = sheet_name
        mkdir(self.path)
        writer = pd.ExcelWriter(self.path)
        df1 = pd.DataFrame(data=self.data)
        df1.to_excel(writer, self.sheet_name, index=False, encoding='utf-8')
        writer.save()


# csv

class Csv_file:
    def f_read_csv(self, path):
        self.path = path
        f = open(self.path)
        try:
            data = pd.read_csv(f, low_memory=False)
        except:
            f2 = open(self.path, "rb")
            d = f2.read()
            f_encoding = check_coding(d)
            f = open(self.path, encoding=f_encoding)
            data = pd.read_csv(f, low_memory=False)
        return data

    def f_writer_csv(self, path, data):
        self.path = path
        self.data = data
        data.to_csv(self.path, index=False, encoding='ANSI')
