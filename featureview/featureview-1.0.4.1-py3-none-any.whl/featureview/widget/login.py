# -*- coding: utf-8 -*-
"""
The main ui
"""

import threading
import sys
from functools import partial
from pathlib import Path
import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import QtSql

from .search import SearchWidget
from ..ui.ui_login import Ui_Login
from ..data import data_process
from . import channel_tree
from .xy import XY_Oszi
from .yt import YT_Oszi
from ..ui import resource_rc

from .. import constant


class Window(Ui_Login, QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.db_pth = None
        self.checked_channel = None
        self.thread_list = []
        b_resample_status = self.cBox_resample.isChecked()

    @QtCore.pyqtSlot(int)
    def on_cBox_mode_currentIndexChanged(self, current_index):
        """ relate the cBox-index with stack-page-index

        :param current_index: the current index
        :return: None
        """
        self.stackedWidget.setCurrentIndex(current_index)

    @QtCore.pyqtSlot()
    def on_btn_mf4_clicked(self):
        """ show the file name in lab_mf4_file

        :return: None
        """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select measurement file",
            "",
            "MDF v4(*.mf4)")

        if file_name is not None:
            file_pth = Path(file_name)
            self.lab_mf4_file.setText(file_pth.name)

            processed_status = None
            if file_pth.suffix.lower() == ".mf4":
                status, processed_status = data_process.parseMf4File(file_pth=file_pth)
                if not status:
                    print('Parse MF4 file Error in fun:data_process.parseMf4File')
                    return False

            db_pth = constant.DB_FILES[0]

            self._createTreeModel(db_pth)
            self._createSearch()

            if not processed_status:
                data_process.extractObjlist()
                data_process.organizeData()

            self._showVehStatic()

    @QtCore.pyqtSlot()
    def on_btn_clear_all_clicked(self):
        self._setCheckOrClearAll(status=False)

    @QtCore.pyqtSlot()
    def on_btn_check_all_clicked(self):
        # self._setCheckOrClearAll(status=True)
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('open db in fun: login.pyt->_createSearch Error')
            return False
        else:
            curs = conn.cursor()
            sql = 'SELECT Group_ID, Channel_ID FROM group_channel AS a, channels AS b WHERE a.ch_no=b.no'
            curs.execute(sql)

            result = curs.fetchall()
            for row in result:
                g_id, ch_id = row
                g_node = self.ch_tree_model.item(g_id)
                this_node = g_node.child(ch_id)
                this_node.setCheckState(QtCore.Qt.Checked)

            conn.close()

    @QtCore.pyqtSlot()
    def on_btn_load_clicked(self):
        """
        get the saved-channel txt-file
        :return:
        """
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select channel file",
            "",
            "Text File(*.txt)")
        loaded_ch_names = []
        with open(filename, mode='r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                loaded_ch_names.append(line)

        for ch in loaded_ch_names:
            if ch in loaded_ch_names:
                info = self.all_ch_names_dir[ch]
                g_id, ch_id = info
                g_node = self.ch_tree_model.item(g_id)
                this_node = g_node.child(ch_id)
                this_node.setCheckState(QtCore.Qt.Checked)
            else:
                print(f'{ch} is not in this channel-tree')

    @QtCore.pyqtSlot()
    def on_btn_save_clicked(self):
        """
        save the already checked channels
        :return:
        """
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'save file', '', 'Text File(*.txt)')

        if filename is not None:
            db_pth = constant.DB_FILES[0]
            try:
                conn = sqlite3.connect(db_pth)
            except Exception:
                print('open db in fun: login.pyt->on_btn_save_clicked Error')
                return False
            else:
                curs = conn.cursor()
                sql = 'SELECT Channel_Name FROM channels AS a, group_channel AS b ' \
                      'WHERE a.no=b.ch_no AND Group_ID=? AND Channel_ID=?'

                checked_ch_names = []
                for row in self.checked_channel:
                    g_id, ch_id = row
                    curs.execute(sql, (g_id, ch_id))
                    result = curs.fetchall()
                    ch_name = result[0][0]
                    checked_ch_names.append(ch_name)

                savedStdout = sys.stdout
                with open(filename[0], mode='w', encoding='utf-8') as f:
                    sys.stdout = f
                    for ch in checked_ch_names:
                        print(ch)
                sys.stdout = savedStdout

    @QtCore.pyqtSlot()
    def on_btn_num_clicked(self):
        """
        show the selected channel info in the right-ui
        :return:
        """
        self._updateCheckedTables()

    @QtCore.pyqtSlot()
    def on_btn_birdview_clicked(self):
        self._updateCheckedTables()

        db_pth_ = constant.DB_FILES[0]
        self.tab_BD = QtWidgets.QWidget()
        self.tab_BD.setObjectName("tab_BD")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tab_BD)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_BD = XY_Oszi(db_pth=db_pth_, parent=self.tab_BD)
        self.widget_BD.setObjectName("widget_BD")
        self.horizontalLayout_7.addWidget(self.widget_BD)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/birdview.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.tabWidget.addTab(self.tab_BD, icon, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.widget_BD.show()
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    @QtCore.pyqtSlot()
    def on_btn_yt_clicked(self):
        """
        define the slot-fun for btn-yt
        :return:
        """
        self._updateCheckedTables()

        db_pth_ = constant.DB_FILES[0]
        self.tab_YT = QtWidgets.QWidget()
        self.tab_YT.setObjectName("tab_YT")
        self.hbox_yt = QtWidgets.QHBoxLayout(self.tab_YT)
        self.hbox_yt.setObjectName("hbox_yt")
        self.widget_YT = YT_Oszi(db_pth=db_pth_, parent=self.tab_YT)
        self.widget_YT.setObjectName("widget_YT")
        self.hbox_yt.addWidget(self.widget_YT)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/yt.png"), QtGui.QIcon.Active, QtGui.QIcon.On)

        self.tabWidget.addTab(self.tab_YT, icon, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.widget_YT.show()
        self.tabWidget.setCurrentIndex(self.tabWidget.count() - 1)

    @QtCore.pyqtSlot(int)
    def on_tabWidget_tabCloseRequested(self, index):
        self.tabWidget.removeTab(index)

    @QtCore.pyqtSlot()
    def on_btn_a2l_clicked(self):
        """ show the file name in lab_mf4_file

        :return: None
        """
        pass

    def _createSearch(self):
        self.all_ch_names = []
        self.all_ch_names_dir = {}
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('open db in fun: login.pyt->_createSearch Error')
            return False
        else:
            curs = conn.cursor()
            str1 = 'SELECT Group_ID, Channel_ID, Channel_Name FROM'
            str2 = 'channels AS ch, group_channel AS g_ch'
            str3 = 'WHERE g_ch.ch_no = ch.no ORDER BY Group_ID, Channel_ID ASC'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            ch_info = curs.fetchall()
            for row in ch_info:
                self.all_ch_names.append(row[-1])
                self.all_ch_names_dir[row[-1]] = (row[0], row[1])

        self.search_widget = SearchWidget(sorted_keys=self.all_ch_names, channels_db=self.all_ch_names_dir)
        self.search_widget.selectionChanged.connect(
            partial(
                self._updateSearchResult,
                tree_model=self.ch_tree_model,
                tree_view=self.tView_channel,
                search=self.search_widget,

            ))
        self.hbox_search.addWidget(self.search_widget)

    def _createTreeModel(self, db_pth):
        self.ch_tree_model = channel_tree.createTreeMode(db_pth)
        self.tView_channel.setModel(self.ch_tree_model)
        self.tView_channel.setWindowTitle('Info')
        self.ch_tree_model.itemChanged.connect(self._treeItemChanged)

    def _updateSearchResult(self, tree_model, tree_view, search):
        group_index, channel_index = search.entries

        g_node = tree_model.item(group_index)
        this_node = g_node.child(channel_index)

        this_node.setCheckState(QtCore.Qt.Checked)
        tree_view.scrollTo(this_node.index())

    def _showCheckChInfo(self):
        if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
            self.DB = QtSql.QSqlDatabase.database("qt_sql_default_connection")
        else:
            self.DB = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_pth = constant.DB_FILES[0]
        self.DB.setDatabaseName(db_pth)
        if self.DB.open():
            self.ch_info_model = QtSql.QSqlQueryModel()
            self.ch_info_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Group_ID')
            self.ch_info_model.setHeaderData(1, QtCore.Qt.Horizontal, 'Channel_ID')
            self.ch_info_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Channel_Name')

            self.ch_info_model.setQuery('SELECT * FROM checked_ch_info')
            if self.ch_info_model.lastError().isValid():
                print('Query Error in btn-num-clicked')
                return False

            self.tView_ch_info.setModel(self.ch_info_model)
            header = self.tView_ch_info.horizontalHeader()
            header.setStretchLastSection(True)
            self.tView_ch_info.show()

            self.DB.close()
        else:
            print('open database Error')
            return False

    def _treeItem_checkAllChild_recursion(self, node, check):
        if node is None:
            return
        rowCount = node.rowCount()
        for j in range(rowCount):
            child_node = node.child(j)
            self._treeItem_checkAllChild_recursion(child_node, check)
        if node.isCheckable():
            check = QtCore.Qt.Checked if check else QtCore.Qt.Unchecked
            node.setCheckState(check)

    def _treeItem_checkAllChild(self, item, state=None):
        """
        when check the group-node, than select all child-nodes
        :param item_: [QStandardItem]
        :param check: [bool]
        :return:
        """
        if item is None:
            return
        rowCount = item.rowCount()

        for i in range(rowCount):
            childItem = item.child(i)
            self.checked_channel.append((item.row(), childItem.row()))
            self._treeItem_checkAllChild_recursion(childItem, state)
        if item.isCheckable():
            state = QtCore.Qt.Checked if state else QtCore.Qt.Unchecked
            item.setCheckState(state)

    def _checkSibling(self, node=None):
        parent = node.parent()
        if parent is None:
            return node.checkState()
        brotherCount = parent.rowCount()
        checkCount = 0
        unCheckCount = 0
        for i in range(brotherCount):
            siblingNode = parent.child(i)
            state = siblingNode.checkState()
            if state == QtCore.Qt.PartiallyChecked:
                return QtCore.Qt.PartiallyChecked
            elif state == QtCore.Qt.Unchecked:
                unCheckCount += 1
            else:
                checkCount += 1
                self.checked_channel.append((parent.row(), siblingNode.row()))

        if (checkCount > 0) and (unCheckCount > 0):
            return QtCore.Qt.PartiallyChecked
        if unCheckCount > 0:
            return QtCore.Qt.Unchecked
        return QtCore.Qt.Checked

    def _treeItem_checkChildChanged(self, item):
        """
        when check the child-nodes, than change the state of parent-node
        :param item: [QStandardItem]
        :return:
        """
        if item is None:
            return

        siblingState = self._checkSibling(node=item)
        parentItem = item.parent()
        if parentItem is None:
            return
        if siblingState == QtCore.Qt.PartiallyChecked:
            if parentItem.isCheckable() and parentItem.isTristate():
                parentItem.setCheckState(QtCore.Qt.PartiallyChecked)
        elif siblingState == QtCore.Qt.Checked:
            if parentItem.isCheckable():
                parentItem.setCheckState(QtCore.Qt.Checked)
        else:
            if parentItem.isCheckable():
                parentItem.setCheckState(QtCore.Qt.Unchecked)
        self._treeItem_checkChildChanged(parentItem)

    def _treeItemChanged(self, item):
        """
        when every change in model is changed, the model will send a signal:
            void QStandardItemModel::itemChanged(QStandardItem * item)
        :param item:[QStandardItem]
        :return:
        """
        # define the auto-connection of parent-child node
        if item is None:
            return
        if item.isCheckable():
            # the type of state is Qt.CheckState
            state = item.checkState()
            if item.isTristate():
                if state != QtCore.Qt.PartiallyChecked:
                    self.checked_channel = []
                    self._treeItem_checkAllChild(item, state=True if state == QtCore.Qt.Checked else False)
                else:
                    pass
            else:
                self.checked_channel = []
                self._treeItem_checkChildChanged(item)

    def _setCheckOrClearAll(self, status):
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('open db in fun: login.pyt->_createSearch Error')
            return False
        else:
            curs = conn.cursor()
            str1 = 'SELECT MAX(Group_ID) FROM'
            str2 = constant.MASTER_TABLE_NAMES[0]
            sql = ' '.join((str1, str2))
            curs.execute(sql)

            result = curs.fetchall()
            g_count = result[0][0] + 1

            for g_id in range(g_count):
                this_g_node = self.ch_tree_model.item(g_id)
                if status:
                    this_g_node.setCheckState(QtCore.Qt.Checked)
                else:
                    this_g_node.setCheckState(QtCore.Qt.Unchecked)

    def _showVehStatic(self):
        if QtSql.QSqlDatabase.contains("qt_sql_default_connection"):
            self.DB = QtSql.QSqlDatabase.database("qt_sql_default_connection")
        else:
            self.DB = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db_pth = constant.DB_FILES[0]
        self.DB.setDatabaseName(db_pth)
        if self.DB.open():
            self.veh_static_model = QtSql.QSqlQueryModel()
            self.veh_static_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Name')
            self.veh_static_model.setHeaderData(1, QtCore.Qt.Horizontal, 'Value')

            self.veh_static_model.setQuery('SELECT * FROM veh_static')
            if self.veh_static_model.lastError().isValid():
                print('Query Error in btn-num-clicked')
                return False

            self.tView_veh_static.setModel(self.veh_static_model)
            header = self.tView_veh_static.horizontalHeader()
            header.setStretchLastSection(True)
            self.tView_veh_static.show()

            self.DB.close()
        else:
            print('open database Error')
            return False

    def _updateCheckedTables(self):
        db_pth_ = constant.DB_FILES[0]
        if self.checked_channel is not None:
            data_process.create_select_table(db_pth=db_pth_, checked_channel=self.checked_channel)
            self._showCheckChInfo()
