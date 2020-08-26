# -*- coding: utf-8 -*-

"""
Demonstrates use of PlotWidget class. This is little more than a 
GraphicsView with a PlotItem placed in its center.
"""

import sqlite3

import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import QtSql
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
import pyqtgraph as pg

from ..ui.ui_xy import Ui_xy
from ..ui import resource_rc

from .. import constant


class XY_Oszi(Ui_xy, QtWidgets.QWidget):
    def __init__(self, db_pth=None, parent=None):
        """
        :param db_pth:
        :param parent:
        """
        super(XY_Oszi, self).__init__(parent)
        self.setupUi(self)

        self.db_pth = db_pth

        self._initUI()
        self._initVars()
        self._getVBData()

        self.onPause()

    def onPlay(self):
        # True means in play-status
        self.b_play = True
        self.b_pause = False

        self._updateBtns()
        self._play()

    def onPause(self):
        # True means current is pause-status
        self.b_pause = True
        self.b_play = False
        self.b_cycle = False

        self._updateBtns()
        self._updateSlider()
        self._updateTreeData()
        self._updateVB()

    def onCycle(self):
        self.b_cycle = True
        self.onPlay()

    def _initVars(self):
        # get timestamp
        self._getTS()

        self.i_current_frame_num = 0

        self.slider.setMaximum(self.ts_len)
        self.slider.setValue(0)

        self.sBox_current_frame_num.setMaximum(self.ts_len)

        checked_row_id = self._checkAllAttrCheckedItem()
        self.checked_attr_list = [self.attr_result[row_id] for row_id in checked_row_id]
        self._updateTreeView()

        self.all_items_need_to_remove = []

    def _initUI(self):
        self._setPen()
        # create vb to show data
        self._createVB()
        self.vbox_bd.addWidget(self.bd)

        # define btns
        iconsize = QtCore.QSize(30, 30)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/cycle.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.cycle_btn = QtWidgets.QToolButton()
        self.cycle_btn.setIcon(icon)
        self.cycle_btn.setIconSize(iconsize)
        self.cycle_btn.setAutoRaise(True)
        self.cycle_btn.setToolTip('Play cycle')
        self.cycle_btn.clicked.connect(self.onCycle)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/play.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.play_btn = QtWidgets.QToolButton()
        self.play_btn.setIcon(icon)
        self.play_btn.setIconSize(iconsize)
        self.play_btn.setAutoRaise(True)
        self.play_btn.setToolTip('Play')
        self.play_btn.clicked.connect(self.onPlay)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/pause.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.pause_btn = QtWidgets.QToolButton()
        self.pause_btn.setIcon(icon)
        self.pause_btn.setIconSize(iconsize)
        self.pause_btn.setAutoRaise(True)
        self.pause_btn.setToolTip('Pause')
        self.pause_btn.setVisible(False)
        self.pause_btn.clicked.connect(self.onPause)

        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/pho/single.png"), QtGui.QIcon.Normal,
        #                QtGui.QIcon.Off)
        # self.single_btn = QtWidgets.QToolButton()
        # self.single_btn.setIcon(icon)
        # self.single_btn.setIconSize(iconsize)
        # self.single_btn.setAutoRaise(True)
        # self.single_btn.setToolTip('Single')
        # self.single_btn.clicked.connect(self.onSingle)

        # define slider
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._updateFromSliderValueChange)

        # define spin to show current frame
        self.sBox_current_frame_num = QtWidgets.QSpinBox()
        self.sBox_current_frame_num.setMinimum(0)
        self.sBox_current_frame_num.setSingleStep(1)
        self.sBox_current_frame_num.valueChanged.connect(self._updateSliderFromSBox)

        # define the media-grid-layout which defined in map.ui
        self.media_grid.addWidget(self.cycle_btn, 0, 0)
        self.media_grid.addWidget(self.play_btn, 0, 1)
        self.media_grid.addWidget(self.pause_btn, 0, 1)
        # self.media_grid.addWidget(self.single_btn, 0, 2)
        self.media_grid.addWidget(self.slider, 0, 2)
        self.media_grid.addWidget(self.sBox_current_frame_num, 0, 3)

        # set col stretch
        for i in range(4):
            self.media_grid.setColumnMinimumWidth(i, 0)
            self.media_grid.setColumnStretch(i, 1)

        self.media_grid.setColumnStretch(2, 100)
        self.media_grid.setColumnStretch(3, 1)

        # set line-edit and btn
        self.lEdit_points.setPlaceholderText('Pls input like that: posx1, posy1, posx2, posy2.')
        self.btn_add.clicked.connect(self.onBtnAddClicked)

        # create attr-table
        self._createCheckAttrModel()

    def _createCheckAttrModel(self):
        # create checked-model
        FixedColNum = 2
        self.check_attr_model = QStandardItemModel(0, FixedColNum)
        headers = ("Attr_ID", "Name")
        self.check_attr_model.setHorizontalHeaderLabels(headers)
        # get the info
        try:
            db_pth = constant.DB_FILES[0]
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('Error in fun: data_process->transformCoordinate, connect db_pth error')
            return False
        else:
            curs = conn.cursor()
            sql = 'SELECT Attr_ID, Attribute_Name ' \
                  'FROM tracker_attr AS a, attribute AS b ' \
                  'WHERE tracker_no=0 AND b.no=a.Attr_ID ' \
                  'ORDER BY Attr_ID'
            curs.execute(sql)
            self.attr_result = curs.fetchall()

            for row_index, row in enumerate(self.attr_result):
                attr_no, attr_name = row
                # set the attr-no item
                attr_no_item = QStandardItem(f'{attr_no}')
                attr_no_item.setCheckable(True)
                attr_no_item.setCheckState(QtCore.Qt.Unchecked)
                self.check_attr_model.setItem(row_index, 0, attr_no_item)

                # set the attr-name item
                attr_name_item = QStandardItem(attr_name)
                self.check_attr_model.setItem(row_index, 1, attr_name_item)

            self.tView_attr.setModel(self.check_attr_model)
            self.check_attr_model.itemChanged.connect(self._checkAttrItemChanged)
            self.attr_selection = QtCore.QItemSelectionModel(self.check_attr_model)
            self.tView_attr.setSelectionModel(self.attr_selection)
            self.attr_selection.currentChanged.connect(self._checkAttrChanged)
            # set multi-select
            self.tView_attr.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
            # set select one item
            self.tView_attr.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            # set forbid edit
            self.tView_attr.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            # set the last col of header
            header = self.tView_attr.horizontalHeader()
            header.setStretchLastSection(True)

    def _checkAllAttrCheckedItem(self):
        all_row_num = self.check_attr_model.rowCount()
        checked_item_list = []
        for i in range(all_row_num):
            iter_item = self.check_attr_model.item(i, 0)
            state = iter_item.checkState()
            if state == QtCore.Qt.Checked:
                checked_item_list.append(iter_item.row())
        return checked_item_list

    def _checkAttrItemChanged(self, item):
        if item is None:
            print('No item changed')
            return True
        else:
            if item.isCheckable():
                checked_row_id = self._checkAllAttrCheckedItem()
                self.checked_attr_list = [self.attr_result[row_id] for row_id in checked_row_id]
                self._updateTreeView()

    def _checkAttrChanged(self, current_index):
        item = self.check_attr_model.item(current_index.row(), 0)
        checked_status = item.checkState()
        if checked_status == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def onBtnAddClicked(self):
        """
        add the polygon to the vb
        :return:
        """
        lEdit_text = self.lEdit_points.text()
        lEdit_text = lEdit_text.strip()
        lEdit_text = lEdit_text.strip('.')
        lEdit_text = lEdit_text.strip(',')
        text_list = lEdit_text.split(',')
        if len(text_list) % 2 != 0:
            msg = QtWidgets.QMessageBox.warning(self, 'Warning',
                                                'Pls input like that: posx1, posy1, pox2, poy2, posx3, posy3...')
            return True
        else:
            points_len = len(text_list) // 2
            i_text_list = [int(i) for i in text_list]
            pointF_list = []
            for point_index in range(points_len):
                index = point_index * 2
                point = QtCore.QPointF(QtCore.QPoint(i_text_list[index], i_text_list[index + 1]))
                pointF_list.append(point)
            pointF_list.append(pointF_list[0])
            pointF = QtGui.QPolygonF(pointF_list)
            polygon = QtWidgets.QGraphicsPolygonItem(pointF)
            polygon.setPen(self.polygon_Pen)
            self.vb.addItem(polygon)

    def _getTS(self):
        """
        get the timestamp
        :return:
        """
        try:
            conn = sqlite3.connect(self.db_pth)
        except Exception:
            print('Error in xy.py->getVehStatic')
            return False
        else:
            curs = conn.cursor()
            sql = 'SELECT * FROM timestamp WHERE no=5'
            curs.execute(sql)
            result = curs.fetchall()
            self.ts_period = result[0][1]
            self.ts_len = result[0][3]

    def _setPen(self):
        """ define some pen
        """
        self.background_Pen = QtGui.QPen(QtCore.Qt.white, 0.05,
                                         QtCore.Qt.SolidLine,
                                         QtCore.Qt.SquareCap,
                                         QtCore.Qt.MiterJoin)
        self.infLine_Pen = QtGui.QPen(QtCore.Qt.white, 0.1,
                                      QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                      QtCore.Qt.MiterJoin)
        self.rm_color = (255, 0, 0)
        self.rm_Pen = QtGui.QPen(QtCore.Qt.red, 0.1, QtCore.Qt.SolidLine,
                                 QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
        self.rs_color = (255, 255, 0)
        self.rs_Pen = QtGui.QPen(QtCore.Qt.yellow, 0.1, QtCore.Qt.SolidLine,
                                 QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
        self.vel_Pen = QtGui.QPen(QtCore.Qt.blue, 0.05, QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)
        self.polygon_Pen = QtGui.QPen(QtCore.Qt.yellow, 0.05, QtCore.Qt.SolidLine,
                                      QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)

    def _getVehStatic(self):
        try:
            conn = sqlite3.connect(self.db_pth)
        except Exception:
            print('Error in xy.py->getVehStatic')
            return False
        else:
            curs = conn.cursor()
            str1 = 'SELECT Value FROM'
            str2 = constant.VEH_STATIC_TABLE_NAMES[0]
            str3 = 'WHERE no BETWEEN 0 AND 5 ORDER BY no'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            result = curs.fetchall()
            veh_static = [i[0] for i in result]
            return veh_static

    def _createVB(self):
        """
        create a vb to show xy-view
        :return:
        """
        self.bd = pg.GraphicsLayoutWidget()

        # set left-axis
        left_axis = pg.AxisItem(orientation='left', pen=(255, 255, 255))
        left_axis.setLabel(text='X', units='m')
        left_axis.enableAutoSIPrefix(False)
        self.bd.ci.addItem(left_axis, 0, 0)

        # set vb
        self.vb = pg.ViewBox(name='Birdview')
        self.bd.ci.addItem(self.vb, 0, 1)

        # set bottom-axis
        bottom_axis = pg.AxisItem(orientation='bottom', pen=(255, 255, 255))
        bottom_axis.setLabel(text='Y', units='m')
        bottom_axis.enableAutoSIPrefix(False)
        self.bd.ci.addItem(bottom_axis, 1, 1)

        # set stretch
        layout = self.bd.ci.layout
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setHorizontalSpacing(0)
        layout.setVerticalSpacing(0)

        for i in range(2):
            layout.setRowPreferredHeight(i, 0)
            layout.setRowMinimumHeight(i, 0)
            layout.setRowSpacing(i, 10)
            layout.setRowStretchFactor(i, 1000)
        layout.setRowStretchFactor(1, 1)

        for i in range(2):
            layout.setColumnPreferredWidth(i, 0)
            layout.setColumnMinimumWidth(i, 0)
            layout.setColumnSpacing(i, 0)
            layout.setColumnStretchFactor(i, 1)
        layout.setColumnStretchFactor(1, 1000)

        # linx axis
        left_axis.linkToView(self.vb)
        bottom_axis.linkToView(self.vb)

        # invert left-axis
        self.vb.invertY()

        # set the default range
        self.vb.setXRange(-200, 200)
        self.vb.setYRange(0, 200)

        # add grid
        grid = pg.GridItem()
        self.vb.addItem(grid)

        # add inf-line
        h_line = pg.InfiniteLine(pos=(0, 0), angle=0, pen=self.background_Pen)
        v_line = pg.InfiniteLine(pos=(0, 0), angle=90, pen=self.background_Pen)
        self.vb.addItem(h_line)
        self.vb.addItem(v_line)

        # add vehicle
        veh_static_list = self._getVehStatic()
        veh_length = veh_static_list[0]
        veh_width = veh_static_list[1]
        rect = QtWidgets.QGraphicsRectItem(QtCore.QRectF(-0.5 * veh_width, 0, veh_width, veh_length))
        rect.setPen(self.background_Pen)
        self.vb.addItem(rect)

        pointF_list = []
        point1 = QtCore.QPointF(QtCore.QPoint(0, 0))
        point2 = QtCore.QPointF(QtCore.QPoint(-1, 0.5 * veh_length))
        point3 = QtCore.QPointF(QtCore.QPoint(1, 0.5 * veh_length))
        pointF_list.append(point1)
        pointF_list.append(point2)
        pointF_list.append(point3)
        pointF_list.append(point1)
        pointF = QtGui.QPolygonF(pointF_list)
        triangle = QtWidgets.QGraphicsPolygonItem(pointF)
        triangle.setPen(self.background_Pen)
        self.vb.addItem(triangle)

        # add FOV
        rm_posX = veh_static_list[2] + veh_length
        rm_poxY = veh_static_list[3]
        rs_posX = veh_static_list[4] + veh_length
        rs_poxY = veh_static_list[5]
        angle1 = np.radians(23)
        angle2 = np.radians(27)
        line_len = 200
        line_list = []
        # add rm-fov
        rm_point1 = (rm_poxY, rm_posX)
        rm_point2 = (
            rm_poxY + line_len * np.cos(angle1),
            rm_posX - line_len * np.sin(angle1))
        rm_point3 = (
            rm_poxY - line_len * np.sin(angle2),
            rm_posX + line_len * np.cos(angle2))
        rm_line1 = QtWidgets.QGraphicsLineItem(rm_point1[0], rm_point1[1], rm_point2[0], rm_point2[1])
        rm_line2 = QtWidgets.QGraphicsLineItem(rm_point1[0], rm_point1[1], rm_point3[0], rm_point3[1])
        line_list.append(rm_line1)
        line_list.append(rm_line2)
        # add rs-fov
        rs_point1 = (rs_poxY, rs_posX)
        rs_point2 = (
            rs_poxY - line_len * np.cos(angle1),
            rs_posX - line_len * np.sin(angle1))
        rs_point3 = (
            rs_poxY + line_len * np.sin(angle2),
            rs_posX + line_len * np.cos(angle2))
        rs_line1 = QtWidgets.QGraphicsLineItem(rs_point1[0], rs_point1[1], rs_point2[0], rs_point2[1])
        rs_line2 = QtWidgets.QGraphicsLineItem(rs_point1[0], rs_point1[1], rs_point3[0], rs_point3[1])
        line_list.append(rs_line1)
        line_list.append(rs_line2)

        for line in line_list:
            line.setPen(self.background_Pen)
            self.vb.addItem(line)

    def _getAttrData(self):
        db_pth = constant.DB_FILES[0]
        try:
            conn = sqlite3.connect(db_pth)
        except Exception:
            print('open db in xy.py->_getAttrData Error')
            return False
        else:
            curs = conn.cursor()

            # get all the tracker-set
            str1 = 'SELECT tracker_no FROM'
            str2 = constant.OBJLIST_TABLE_NAMES[4]
            str3 = 'GROUP BY tracker_no'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            tracker_no_result = curs.fetchall()

            all_attr_info = {'RM': [], 'RS': []}
            for tracker_no in tracker_no_result:
                # get tracker-id
                sql = 'SELECT Tracker_ID FROM tracker WHERE no=?'
                curs.execute(sql, tracker_no)
                tracker_id_result = curs.fetchall()
                tracker_id = tracker_id_result[0][0]

                checked_ch_name_value_list = []
                for attr_info in self.checked_attr_list:
                    # get ch-no in tracker-attr
                    sql = 'SELECT ch_no ' \
                          'FROM tracker_attr ' \
                          'WHERE tracker_no=? AND Attr_ID=?'
                    tracker_no_ = tracker_no[0]
                    attr_no = attr_info[0]
                    curs.execute(sql, (tracker_no_, attr_no))
                    ch_no_result = curs.fetchall()
                    ch_no = ch_no_result[0]

                    # get ch-name
                    sql = 'SELECT Channel_Name FROM channels WHERE no=?'
                    curs.execute(sql, ch_no)
                    ch_id_name_result = curs.fetchall()
                    ch_name = ch_id_name_result[0][0]

                    # get the ch-data
                    sql = 'SELECT Value_after_CoordTransform ' \
                          'FROM data_no_resample AS a, channel_data_no_resample AS b ' \
                          'WHERE ch_no=? AND a.no=b.data_no ' \
                          'ORDER BY TimeStamp_ID'
                    curs.execute(sql, ch_no)
                    value_result = curs.fetchall()
                    ch_value = [i[0] for i in value_result]
                    checked_ch_name_value_list.append((ch_name, ch_value))

                attr_info_value_list = (tracker_id, checked_ch_name_value_list)
                # get radar-loc
                sql = 'SELECT Radar_Name From radar_tracker AS a, radar_loc AS b ' \
                      'WHERE tracker_no=? AND a.Radar_ID=b.Radar_ID'
                curs.execute(sql, tracker_no)
                radar_loc = curs.fetchall()
                radar_loc = radar_loc[0][0]
                if radar_loc == 'RM':
                    all_attr_info['RM'].append(attr_info_value_list)
                elif radar_loc == 'RS':
                    all_attr_info['RS'].append(attr_info_value_list)
                else:
                    print('Error in xy.py->_getAttrData')

            return all_attr_info

    def _updateTreeData(self):
        for radar in ('RM', 'RS'):
            info = self.attr_data[radar]
            for tracker_info in info:
                ch_name_values = tracker_info[1]
                for row in ch_name_values:
                    ch_name = row[0]
                    if ch_name in self.ch_name_to_item_index_dir.keys():
                        current_value = row[1][self.i_current_frame_num]
                        tree_item_index = self.ch_name_to_item_index_dir[ch_name]
                        this_tree_item = self.attr_model.itemFromIndex(tree_item_index)
                        this_tree_item.setText(f'{current_value:.2f}')

    def _updateTreeView(self):
        """
        When the frame changed, update the tView-data
        :return:
        """
        # create a dir to store the index of ch
        self.ch_name_to_item_index_dir = {}

        # get checked-attr-data
        self.attr_data = self._getAttrData()

        self.attr_model = QStandardItemModel()
        headers = ("Radar", "Value")
        self.attr_model.setHorizontalHeaderLabels(headers)
        root_item = self.attr_model.invisibleRootItem()
        for i, radar in enumerate(('RM', 'RS')):
            radar_node = QStandardItem(f'{radar}')
            radar_node.setEditable(False)
            root_item.setChild(i, 0, radar_node)
            # self.attr_model.setItem(i, 0, radar_node)

            info = self.attr_data[radar]
            for j, row_tracker in enumerate(info):
                tracker_id, ch_info = row_tracker
                tracker_node = QStandardItem(f'Tracker-{tracker_id}')
                tracker_node.setEditable(False)
                radar_node.setChild(j, 0, tracker_node)

                for k, row_ch in enumerate(ch_info):
                    ch_name, ch_value = row_ch
                    ch_node = QStandardItem(f'{ch_name}')
                    ch_node.setEditable(False)
                    tracker_node.setChild(k, 0, ch_node)
                    # tracker_node.appendRow(ch_node)

                    value_node = QStandardItem()
                    value_node.setEditable(False)
                    tracker_node.setChild(ch_node.index().row(), 1, value_node)
                    self.ch_name_to_item_index_dir[ch_name] = value_node.index()
        self.treeView_top.setModel(self.attr_model)
        self._updateTreeData()

    def _updateVB(self):

        """
        When the current-value changed, update the vb.
        """
        if self.i_current_frame_num == self.ts_len:
            pass
        else:
            # clear the previous data-item
            for item in self.all_items_need_to_remove:
                self.vb.removeItem(item)
            # for item in self.vb.addedItems:
            #     if isinstance(item, pg.PlotDataItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.PlotCurveItem):
            #         self.vb.removeItem(item)
            #     elif isinstance(item, pg.CurvePoint):
            #         self.vb.removeItem(item)

            self.all_items_need_to_remove = []
            # plot
            for info in self.vb_info:
                radar_loc, tracker_id, values = info
                current_value = values[self.i_current_frame_num, :]
                # add pos
                current_posX = current_value[0:3]
                current_posY = current_value[3:6]
                current_pen = self.rm_Pen if radar_loc == 'RM' else self.rs_Pen
                color = self.rm_color if radar_loc == 'RM' else self.rs_color
                pos_curve = pg.PlotDataItem(x=current_posY,
                                            y=current_posX,
                                            pen=current_pen,
                                            symbolBrush=color,
                                            symbolPen='w',
                                            symbol='o',
                                            symbolSize=10)
                # set ZValue will show in the front of scene
                pos_curve.setZValue(100)
                self.vb.addItem(pos_curve, ignoreBounds=False)
                self.all_items_need_to_remove.append(pos_curve)

                # add vel
                current_velX = current_value[6]
                current_velY = current_value[7]
                complex_vel = complex(current_velX, current_velY)
                vel = np.abs(complex_vel)
                angle_radian = np.angle(complex_vel)
                angle = np.angle(complex_vel, deg=True)
                # define a scale-factor to scale the vel
                scale_factor = 10
                vel_after_scale = vel / scale_factor
                current_velX_after_scale = vel_after_scale * np.cos(angle_radian)
                current_velY_after_scale = vel_after_scale * np.sin(angle_radian)

                current_velX_list = [current_posX[1], current_posX[1] + current_velX_after_scale]
                current_velY_list = [current_posY[1], current_posY[1] + current_velY_after_scale]
                vel_line = pg.PlotCurveItem(x=current_velY_list,
                                            y=current_velX_list,
                                            pen=self.vel_Pen,
                                            antialias=True)
                self.vb.addItem(vel_line, ignoreBounds=False)
                self.all_items_need_to_remove.append(vel_line)
                # add info-text
                info_curve_point = pg.CurvePoint(pos_curve, index=1)
                self.vb.addItem(info_curve_point, ignoreBounds=False)
                self.all_items_need_to_remove.append(info_curve_point)
                anchor_ = (-0.2, 0) if radar_loc == 'RM' else (0.8, 0)
                info_text = pg.TextItem(f"{radar_loc}\nTracker_ID:{tracker_id}\nVel:{vel:.2f}\nAngle:{angle:.2f}",
                                        anchor=anchor_)
                info_text.setParentItem(info_curve_point)

    def _updateSlider(self):
        has_frame = self.i_current_frame_num >= 0
        if has_frame:
            self.slider.setValue(self.i_current_frame_num)
        else:
            self.slider.setMaximum(0)

    def _updateBtns(self):
        """ update the btn-state
        """
        if self.b_pause:  # pause-status
            # set play-btn
            self.play_btn.setVisible(True)
            self.play_btn.setEnabled(True)
            self.play_btn.setCheckable(True)
            # set pause-btn
            self.pause_btn.setVisible(False)
            self.pause_btn.setEnabled(False)
            self.pause_btn.setCheckable(False)
            # set cycle-btn
            self.cycle_btn.setEnabled(True)
            self.cycle_btn.setCheckable(True)
            # set slider
            self.slider.setEnabled(True)
            # set sbox
            self.sBox_current_frame_num.setEnabled(True)
        else:  # play-status
            # set play-btn
            self.play_btn.setVisible(False)
            self.play_btn.setEnabled(False)
            self.play_btn.setCheckable(False)
            # set pause-btn
            self.pause_btn.setVisible(True)
            self.pause_btn.setEnabled(True)
            self.pause_btn.setCheckable(True)
            # set cycle-btn
            self.cycle_btn.setEnabled(False)
            self.cycle_btn.setCheckable(False)
            # set slider
            self.slider.setEnabled(False)
            # set sbox
            self.sBox_current_frame_num.setEnabled(False)

    def _updateFromSliderValueChange(self, i_current_slider_num):
        # update current-frame-num
        self.i_current_frame_num = i_current_slider_num
        # update spin-box
        self.sBox_current_frame_num.setValue(i_current_slider_num)
        # update vb
        self._updateVB()
        # update tView
        self._updateTreeData()

    def _updateSliderFromSBox(self, i_current_sbox_num):
        self.slider.setValue(i_current_sbox_num)

    def _getVBData(self):
        try:
            conn = sqlite3.connect(self.db_pth)
        except Exception:
            print('Error in xy.py->_getVBData')
            return False
        else:
            curs = conn.cursor()
            # get all the tracker-set
            str1 = 'SELECT tracker_no FROM'
            str2 = constant.OBJLIST_TABLE_NAMES[4]
            str3 = 'GROUP BY tracker_no'
            sql = ' '.join((str1, str2, str3))
            curs.execute(sql)
            tracker_no_result = curs.fetchall()

            self.vb_info = []
            for tracker_no in tracker_no_result:
                # get ch-no in tracker-attr
                sql = 'SELECT ch_no ' \
                      'FROM tracker_attr ' \
                      'WHERE tracker_no=? AND Attr_ID BETWEEN 0 AND 7 ' \
                      'ORDER BY Attr_ID'
                curs.execute(sql, tracker_no)
                pos_ch_no_result = curs.fetchall()

                vb_value_list = []
                for ch_no in pos_ch_no_result:
                    sql = 'SELECT Value_after_CoordTransform ' \
                          'FROM data_no_resample AS a, channel_data_no_resample AS b ' \
                          'WHERE ch_no=? AND a.no=b.data_no ' \
                          'ORDER BY TimeStamp_ID'
                    curs.execute(sql, ch_no)
                    value_result = curs.fetchall()
                    value_list = [i[0] for i in value_result]
                    vb_value_list.append(value_list)

                vb_value_ndarray = np.vstack(vb_value_list)
                vb_value_ndarray = vb_value_ndarray.transpose()

                # get radar-loc
                sql = 'SELECT Radar_Name From radar_tracker AS a, radar_loc AS b ' \
                      'WHERE tracker_no=? AND a.Radar_ID=b.Radar_ID'
                curs.execute(sql, tracker_no)
                radar_loc = curs.fetchall()
                radar_loc = radar_loc[0][0]

                # get tracker-id
                sql = 'SELECT Tracker_ID FROM tracker WHERE no=?'
                curs.execute(sql, tracker_no)
                tracker_id_result = curs.fetchall()
                tracker_id = tracker_id_result[0][0]

                self.vb_info.append((radar_loc, tracker_id, vb_value_ndarray))

    def _play(self):
        if self.b_play:
            if self.i_current_frame_num == self.ts_len:  # arrive to end
                if self.b_cycle:  # in cycle-status
                    self.i_current_frame_num = 0
                    self._play()
                else:  # in end-status
                    self.onPause()
            else:  # play-status
                self._updateVB()
                self._updateTreeData()
                self._updateSlider()

                self.timer = QtCore.QTimer()
                # self.timer.setInterval(self.ts_period)
                self.timer.setSingleShot(True)
                self.timer.start(self.ts_period)
                self.timer.timeout.connect(self._updateFrameNum)

    def _updateFrameNum(self):
        self.i_current_frame_num += 1
        self._play()
