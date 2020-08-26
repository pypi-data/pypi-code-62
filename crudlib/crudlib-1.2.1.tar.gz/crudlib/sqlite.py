#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Zheng <zxyful@gmail.com>
# Date: 2019/8/8
# Desc: 

import sqlite3

from crudlib.mysql import MySQL


class SQLite(MySQL):
    def __init__(self):
        super(SQLite).__init__()
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE stocks
                     (date text, trans text, symbol text, qty real, price real)''')

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


if __name__ == '__main__':
    s = SQLite()
    print(s)
