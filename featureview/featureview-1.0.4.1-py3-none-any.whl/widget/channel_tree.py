# -*- coding:utf-8 -*-

import sqlite3

from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel

from .. import constant


def createTreeMode(db_pth):
    """
    create a tree model
    :param db_pth: [path]
    :return: [QStandardItemModel]
    """

    try:
        conn = sqlite3.connect(db_pth)
    except Exception:
        print('open db in createTreeModel Error')
        return False
    else:
        curs = conn.cursor()
        str1 = 'SELECT Group_ID, Group_Name FROM'
        str2 = constant.MASTER_TABLE_NAMES[0]
        str3 = 'ORDER BY Group_ID'
        sql = ' '.join((str1, str2, str3))
        curs.execute(sql)
        group_info = curs.fetchall()

        model = QStandardItemModel()
        headers = ("Group_ID", "Length/Ch_ID", "Name")
        model.setHorizontalHeaderLabels(headers)
        root_node = model.invisibleRootItem()
        for g_id, group in enumerate(group_info):
            group_id, group_name = group

            str1 = 'SELECT Channel_ID, Channel_Name FROM'
            str2 = 'group_channel AS g_ch, channels AS ch'
            str3 = 'WHERE g_ch.Group_ID = ?  AND g_ch.ch_no = ch.no ORDER BY Channel_ID'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql, (group_id,))
            channel_info = curs.fetchall()

            group_ch_length = len(channel_info)
            group_data = (group_id, group_ch_length, group_name)

            group_node = QStandardItem(f'{group_data[0]}')
            group_node.setEditable(False)
            group_node.setCheckable(True)
            group_node.setTristate(True)
            root_node.setChild(g_id, 0, group_node)
            # root_node.appendRow(group_node)

            node = QStandardItem(f'{group_data[1]}')
            node.setEditable(False)
            model.setItem(model.indexFromItem(group_node).row(), 1, node)
            node = QStandardItem(f'{group_data[2]}')
            node.setEditable(False)
            model.setItem(model.indexFromItem(group_node).row(), 2, node)

            for ch in channel_info:
                ch_ID, ch_name = ch
                ch_data = (group_id, ch_ID, ch_name)
                ch_node = QStandardItem(f'{ch_data[0]}')
                ch_node.setEditable(False)
                ch_node.setCheckable(True)
                group_node.appendRow(ch_node)
                node = QStandardItem(f'{ch_data[1]}')
                node.setEditable(False)
                group_node.setChild(ch_node.index().row(), 1, node)
                node = QStandardItem(f'{ch_data[2]}')
                node.setEditable(False)
                group_node.setChild(ch_node.index().row(), 2, node)

        return model
