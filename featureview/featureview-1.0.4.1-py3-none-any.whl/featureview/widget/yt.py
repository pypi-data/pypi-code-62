# -*- coding: utf-8 -*-

import sqlite3

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
import pyqtgraph as pg

from ..ui.ui_yt import Ui_yt

from .. import constant


class YT_Oszi(Ui_yt, QtWidgets.QWidget):
    def __init__(self, db_pth=None, parent=None):
        super(YT_Oszi, self).__init__()
        self.setupUi(self)

        db_pth = constant.DB_FILES[0]
        self.info = self._getCheckedData(db_pth_=db_pth)

        self._initUi(data=self.info)
        self.cBox_ts.setCurrentIndex(0)

        checked_row_list = self._checkAllCheckedItem()
        self._updateGraphics(checked_row_list)

    def _initUi(self, data=None):
        if data is not None:
            g_len = len(data)
            for i in range(g_len):
                self.cBox_ts.addItem(f'Group-{i}')

    @QtCore.pyqtSlot(int)
    def on_cBox_ts_currentIndexChanged(self, current_index):
        """ relate the cBox-index with stack-page-index

        :param current_index: the current index
        :return: None
        """
        current_ts_info = self.info[current_index][0]
        ts_period = current_ts_info[0]
        ts_unit = current_ts_info[1]
        ts_len = current_ts_info[2]

        self.lab_ts.setText(f'SamplePeriod:{ts_period}, Unit:{ts_unit}, Length:{ts_len}')

        # create checked-model
        FixedColNum = 5
        self.check_model = QStandardItemModel(0, FixedColNum)
        headers = ("Check", "ch_no", "Name", "Value", "Unit")
        self.check_model.setHorizontalHeaderLabels(headers)
        root_item = self.check_model.invisibleRootItem()
        ch_info = self.info[current_index][1]
        for row_index, row in enumerate(ch_info):
            ch_no, ch_name, ch_unit, ch_value = row
            # set the check-item
            check_item = QStandardItem()
            check_item.setCheckable(True)
            check_item.setCheckState(QtCore.Qt.Checked)
            self.check_model.setItem(row_index, 0, check_item)

            # set the ch-no item
            ch_no_item = QStandardItem(f'{ch_no}')
            self.check_model.setItem(row_index, 1, ch_no_item)

            # set the ch-name item
            ch_name_item = QStandardItem(ch_name)
            self.check_model.setItem(row_index, 2, ch_name_item)

            # set the value item
            value_item = QStandardItem()
            self.check_model.setItem(row_index, 3, value_item)

            # set ch-unit item
            ch_unit_item = QStandardItem(f'{ch_unit}')
            self.check_model.setItem(row_index, 4, ch_unit_item)

        self.tView_checked_ch.setModel(self.check_model)
        header = self.tView_checked_ch.horizontalHeader()
        header.setStretchLastSection(True)
        self.check_model.itemChanged.connect(self.checkItemChanged)
        self.selection = QtCore.QItemSelectionModel(self.check_model)
        self.tView_checked_ch.setSelectionModel(self.selection)
        self.selection.currentChanged.connect(self.checkChanged)
        # set multi-select
        self.tView_checked_ch.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        # set select one item
        self.tView_checked_ch.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # set forbid edit
        self.tView_checked_ch.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.win = pg.GraphicsLayoutWidget()
        self.vBox_checked_ch.addWidget(self.win)

    def _checkAllCheckedItem(self):
        """
        when check the child-nodes, than change the state of parent-node
        :param item: [QStandardItem]
        :return:
        """
        all_row_num = self.check_model.rowCount()
        checked_item_list = []
        for i in range(all_row_num):
            iter_item = self.check_model.item(i, 0)
            state = iter_item.checkState()
            if state == QtCore.Qt.Checked:
                checked_item_list.append(iter_item.row())
        return checked_item_list

    def checkItemChanged(self, item):
        if item is None:
            print('No item changed')
            return True
        else:
            if item.isCheckable():
                checked_row_id = self._checkAllCheckedItem()
                self._updateGraphics(checked_row_id)

    def checkChanged(self, current_index):
        """

        :param current_index: [QModelIndex]
        :return:
        """
        item = self.check_model.item(current_index.row(), 0)
        checked_status = item.checkState()
        if checked_status == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def _getCheckedData(self, db_pth_=None):
        """
        get the data for plot
        :param db_pth_: [srt]
        :return: all_checked_data: [
                                    (ts_value,
                                        [   (ch_no, ch_name, ch_data_unit, ch_value),
                                            (ch_no, ch_name, ch_data_unit, ch_value), ...
                                        ]
                                    ),
                                    (...),
                                   ]
        """
        if db_pth_ is None:
            print('no input db-path in yt._getCheckedData')
            return
        try:
            conn = sqlite3.connect(db_pth_)
            curs = conn.cursor()
        except Exception:
            print('create selected-ch-view error in yt->getCheckedData')
            return False

        sql = 'SELECT Group_ID FROM checked_ch_info GROUP BY Group_ID'
        curs.execute(sql)
        checked_g_id = curs.fetchall()

        data = []
        all_checked_data = []
        for g_id_count in checked_g_id:
            sql = 'SELECT Sample_Period, Sample_Unit, Sample_Length ' \
                  'FROM timestamp AS a, group_ts AS b ' \
                  'WHERE a.no=b.ts_no AND Group_ID=?'
            curs.execute(sql, g_id_count)
            ts_result_list = curs.fetchall()
            ts_info = ts_result_list[0]

            sql = 'SELECT ch_no, Channel_Name, Ch_Data_Unit FROM checked_ch_info WHERE Group_ID=?'
            curs.execute(sql, g_id_count)
            ch_info_list = curs.fetchall()

            for ch_info in ch_info_list:
                ch_no, ch_name, ch_unit = ch_info
                sql = 'SELECT Value_after_CoordTransform FROM ' \
                      'channel_data_no_resample AS a, ' \
                      'data_no_resample AS b ' \
                      'WHERE ch_no=? AND a.data_no = b.no ' \
                      'ORDER BY TimeStamp_ID'
                curs.execute(sql, (ch_no,))

                ch_value = []
                m = curs.fetchall()
                for i in m:
                    ch_value.append(i[0])
                data.append((ch_no, ch_name, ch_unit, ch_value))
            all_checked_data.append((ts_info, data))

        return all_checked_data

    def _updateGraphics(self, row_id_list=None):
        """ add the data to scene.
        """
        self.win.ci.clear()

        # set the layout
        row_len = len(row_id_list)
        layout = self.win.ci.layout
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        for i in range(row_len):
            layout.setRowPreferredHeight(i, 0)
            layout.setRowMinimumHeight(i, 0)
            layout.setRowSpacing(i, 10)
            layout.setRowStretchFactor(i, 1000)

        for i in range(2):
            layout.setColumnPreferredWidth(i, 0)
            layout.setColumnMinimumWidth(i, 0)
            layout.setColumnSpacing(i, 0)
            layout.setColumnStretchFactor(i, 1)

        layout.setRowStretchFactor(row_len, 1)
        layout.setColumnStretchFactor(1, 1000)

        g_id = self.cBox_ts.currentIndex()

        # get time-stamp
        current_ts_info = self.info[g_id][0]
        ts_period = current_ts_info[0]
        ts_unit = current_ts_info[1]
        ts_len = current_ts_info[2]
        ts_value = list(range(ts_len))

        ch_info = self.info[g_id][1]
        self.vb_list = []
        self.bottom_axis_list = []
        for current_index, row_index in enumerate(row_id_list):
            ch_no, ch_name, ch_unit, ch_value = ch_info[row_index]

            # set left-axis
            left_axis = pg.AxisItem(orientation='left', pen=(255, 255, 255))
            left_axis.setLabel(text=f'{ch_no}', units=ch_unit)
            left_axis.enableAutoSIPrefix(False)
            self.win.ci.addItem(left_axis, current_index, 0)

            # set vb
            vb = pg.ViewBox(name=ch_name)
            vb.setXRange(0, ts_len)
            curve_data = pg.PlotDataItem(x=ts_value, y=ch_value, name=ch_name,
                                         pen=(195, 46, 212), symbolBrush=(195, 46, 212),
                                         symbolPen='w', symbol='t2', symbolSize=7, )
            vb.addItem(curve_data, ignoreBounds=False)

            # add ch-name
            ch_name_text = pg.TextItem(f"{ch_name}", anchor=(0, 0))
            # set the pos in partent-item
            ch_name_text.setPos(ts_len / 2, np.max(curve_data.yData))
            vb.addItem(ch_name_text, ignoreBounds=False)

            self.vb_list.append((row_index, vb))
            # sigPointsClicked(self, points)
            # Emitted when a plot point is clicked Sends the list of points under the mouse.
            curve_data.sigPointsClicked.connect(self._clickDataPoint)
            self.win.ci.addItem(vb, current_index, 1)

            left_axis.linkToView(view=vb)

        # set bottom-axis
        bottom_axis = pg.AxisItem(orientation='bottom', pen=(255, 255, 255))
        bottom_axis.setLabel(text=f'Time-Stamp:{ts_period}/dec', units=ts_unit)
        bottom_axis.enableAutoSIPrefix(False)
        bottom_axis.linkToView(self.vb_list[0][1])
        self.win.ci.addItem(bottom_axis, row_len, 1)

        # link x-axis in all item together
        for i, item in enumerate(self.vb_list):
            if i > 0:
                item[1].setXLink(self.vb_list[0][1])

    def _clickDataPoint(self, current_item, points):
        """
        When the use click the point in the data, signal(sigPointsClicked) -emit() -> this fun
        :param current_item : [PlotDataItem] the sender item
        :param points: [list] the clicked points. every item in list is SpotItem
        :return:
        """
        # Because we only have one point, so choose 0
        point = points[0].pos()
        x, y = point.x(), point.y()
        current_t_index = np.argwhere(current_item.xData == x)[0][0]

        ch_name_list = []
        y_data_list = []
        for row in self.vb_list:
            row_index, vb = row
            # get the plot_item name
            ch_name = vb.name
            ch_name_list.append(ch_name)

            # update the curvePoint
            data_item = []
            point_item_list = []
            # vb.addedItems'type is lit
            for item in vb.addedItems:
                if isinstance(item, pg.PlotDataItem):
                    data_item.append(item)
                elif isinstance(item, pg.CurvePoint):
                    vb.removeItem(item)
                else:
                    pass

            curve = data_item[0]

            t = curve.xData[current_t_index]
            y = curve.yData[current_t_index]

            y_data_list.append(y)

            curve_point = pg.CurvePoint(curve, index=current_t_index)
            vb.addItem(curve_point, ignoreBounds=False)
            text = pg.TextItem(f"{t}, {y}", anchor=(0.5, -1.0))
            text.setParentItem(curve_point)
            arrow = pg.ArrowItem(angle=90)
            arrow.setParentItem(curve_point)

            # update the table-view
            value_item = self.check_model.item(row_index, 3)
            value_item.setText(f"{t}, {y}")