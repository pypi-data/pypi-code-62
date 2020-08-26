# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchWidget(object):
    def setupUi(self, SearchWidget):
        SearchWidget.setObjectName("SearchWidget")
        SearchWidget.resize(312, 29)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SearchWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SearchWidget)
        self.label.setMinimumSize(QtCore.QSize(80, 30))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.search = QtWidgets.QLineEdit(SearchWidget)
        self.search.setMinimumSize(QtCore.QSize(0, 30))
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.down_btn = QtWidgets.QPushButton(SearchWidget)
        self.down_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pho/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/pho/up.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.down_btn.setIcon(icon)
        self.down_btn.setObjectName("down_btn")
        self.horizontalLayout.addWidget(self.down_btn)
        self.up_btn = QtWidgets.QPushButton(SearchWidget)
        self.up_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pho/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/pho/down.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.up_btn.setIcon(icon1)
        self.up_btn.setObjectName("up_btn")
        self.horizontalLayout.addWidget(self.up_btn)
        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(SearchWidget)
        QtCore.QMetaObject.connectSlotsByName(SearchWidget)

    def retranslateUi(self, SearchWidget):
        _translate = QtCore.QCoreApplication.translate
        SearchWidget.setWindowTitle(_translate("SearchWidget", "Form"))
        self.label.setText(_translate("SearchWidget", "No match"))
from . import resource_rc
