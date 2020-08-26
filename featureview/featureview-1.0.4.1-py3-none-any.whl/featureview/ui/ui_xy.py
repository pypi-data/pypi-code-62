# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xy.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_xy(object):
    def setupUi(self, xy):
        xy.setObjectName("xy")
        xy.resize(840, 625)
        self.horizontalLayout = QtWidgets.QHBoxLayout(xy)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter_2 = QtWidgets.QSplitter(xy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setHandleWidth(1)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.vbox_left = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.vbox_left.setContentsMargins(0, 0, 0, 0)
        self.vbox_left.setSpacing(0)
        self.vbox_left.setObjectName("vbox_left")
        self.vbox_bd = QtWidgets.QVBoxLayout()
        self.vbox_bd.setObjectName("vbox_bd")
        self.vbox_left.addLayout(self.vbox_bd)
        self.hbox_btn_slider = QtWidgets.QHBoxLayout()
        self.hbox_btn_slider.setSpacing(5)
        self.hbox_btn_slider.setObjectName("hbox_btn_slider")
        self.media_grid = QtWidgets.QGridLayout()
        self.media_grid.setSpacing(0)
        self.media_grid.setObjectName("media_grid")
        self.hbox_btn_slider.addLayout(self.media_grid)
        self.vbox_left.addLayout(self.hbox_btn_slider)
        self.vbox_left.setStretch(0, 50)
        self.vbox_left.setStretch(1, 1)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(1)
        self.splitter.setObjectName("splitter")
        self.treeView_top = QtWidgets.QTreeView(self.splitter)
        self.treeView_top.setObjectName("treeView_top")
        self.gBox_attr = QtWidgets.QGroupBox(self.splitter)
        self.gBox_attr.setAlignment(QtCore.Qt.AlignCenter)
        self.gBox_attr.setObjectName("gBox_attr")
        self.vBox_right = QtWidgets.QVBoxLayout(self.gBox_attr)
        self.vBox_right.setContentsMargins(0, 0, 0, 0)
        self.vBox_right.setSpacing(0)
        self.vBox_right.setObjectName("vBox_right")
        self.hBox_add_attr = QtWidgets.QHBoxLayout()
        self.hBox_add_attr.setObjectName("hBox_add_attr")
        self.lEdit_points = QtWidgets.QLineEdit(self.gBox_attr)
        self.lEdit_points.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lEdit_points.setFont(font)
        self.lEdit_points.setPlaceholderText("")
        self.lEdit_points.setClearButtonEnabled(True)
        self.lEdit_points.setObjectName("lEdit_points")
        self.hBox_add_attr.addWidget(self.lEdit_points)
        self.btn_add = QtWidgets.QPushButton(self.gBox_attr)
        self.btn_add.setMinimumSize(QtCore.QSize(0, 30))
        self.btn_add.setObjectName("btn_add")
        self.hBox_add_attr.addWidget(self.btn_add)
        self.hBox_add_attr.setStretch(0, 10)
        self.hBox_add_attr.setStretch(1, 1)
        self.vBox_right.addLayout(self.hBox_add_attr)
        self.tView_attr = QtWidgets.QTableView(self.gBox_attr)
        self.tView_attr.setObjectName("tView_attr")
        self.vBox_right.addWidget(self.tView_attr)
        self.vBox_right.setStretch(0, 1)
        self.vBox_right.setStretch(1, 10)
        self.horizontalLayout.addWidget(self.splitter_2)

        self.retranslateUi(xy)
        QtCore.QMetaObject.connectSlotsByName(xy)

    def retranslateUi(self, xy):
        _translate = QtCore.QCoreApplication.translate
        xy.setWindowTitle(_translate("xy", "Form"))
        self.gBox_attr.setTitle(_translate("xy", "Attribute"))
        self.btn_add.setText(_translate("xy", "Add"))
from . import resource_rc
