#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/8/8
# Desc: 


from crudlib.mysql import MySQL


class MariaDB(MySQL):
    def __init__(self):
        super(MariaDB, self).__init__()
        print("a")

    def __repr__(self):
        return "MariaDB:xxx"


if __name__ == '__main__':
    ma = MariaDB()
    print(dir(ma))
    # ma.execute()
