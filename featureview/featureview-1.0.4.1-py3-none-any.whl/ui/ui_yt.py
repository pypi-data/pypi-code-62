# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yt.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_yt(object):
    def setupUi(self, yt):
        yt.setObjectName("yt")
        yt.resize(840, 625)
        self.horizontalLayout = QtWidgets.QHBoxLayout(yt)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(yt)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(3)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hbox_select_ts = QtWidgets.QHBoxLayout()
        self.hbox_select_ts.setSpacing(0)
        self.hbox_select_ts.setObjectName("hbox_select_ts")
        self.cBox_ts = QtWidgets.QComboBox(self.layoutWidget)
        self.cBox_ts.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cBox_ts.setFont(font)
        self.cBox_ts.setObjectName("cBox_ts")
        self.hbox_select_ts.addWidget(self.cBox_ts)
        self.lab_ts = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lab_ts.setFont(font)
        self.lab_ts.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_ts.setObjectName("lab_ts")
        self.hbox_select_ts.addWidget(self.lab_ts)
        self.hbox_select_ts.setStretch(0, 1)
        self.hbox_select_ts.setStretch(1, 6)
        self.verticalLayout.addLayout(self.hbox_select_ts)
        self.tView_checked_ch = QtWidgets.QTableView(self.layoutWidget)
        self.tView_checked_ch.setMaximumSize(QtCore.QSize(160000, 16777215))
        self.tView_checked_ch.setObjectName("tView_checked_ch")
        self.verticalLayout.addWidget(self.tView_checked_ch)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vBox_checked_ch = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.vBox_checked_ch.setContentsMargins(0, 0, 0, 0)
        self.vBox_checked_ch.setObjectName("vBox_checked_ch")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(yt)
        QtCore.QMetaObject.connectSlotsByName(yt)

    def retranslateUi(self, yt):
        _translate = QtCore.QCoreApplication.translate
        yt.setWindowTitle(_translate("yt", "Form"))
        self.lab_ts.setText(_translate("yt", "Select TimeStamp Group"))
from . import resource_rc
