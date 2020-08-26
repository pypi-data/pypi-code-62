"""
define a BirdView class
"""

import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph as pg

from .. import constant


class BirdView(PlotWidget):
    """ to show the tracker dynamically
    """

    def __init__(self, *args, db_pth=None, parent=None):
        super(BirdView, self).__init__(*args, parent)
        self.db_pth = db_pth
        self.setPen()
        self.initUi()

    def setPen(self):
        """ define some pen
        """
        self.background_Pen = QtGui.QPen(QtCore.Qt.white, 0.05,
                                         QtCore.Qt.SolidLine,
                                         QtCore.Qt.SquareCap,
                                         QtCore.Qt.MiterJoin)
        self.infLine_Pen = QtGui.QPen(QtCore.Qt.white, 0.1,
                                      QtCore.Qt.SolidLine, QtCore.Qt.SquareCap,
                                      QtCore.Qt.MiterJoin)
        self.rm_Pen = QtGui.QPen(QtCore.Qt.white, 0.05, QtCore.Qt.SolidLine,
                                 QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
        self.rs_Pen = QtGui.QPen(QtCore.Qt.yellow, 0.05, QtCore.Qt.SolidLine,
                                 QtCore.Qt.SquareCap, QtCore.Qt.MiterJoin)
        self.vel_Pen = QtGui.QPen(QtCore.Qt.blue, 0.05, QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap, QtCore.Qt.MiterJoin)

    def initUi(self):
        # because the coordinate of vehicle is left-x, bottom-y
        self.plotItem.setLabel('left', 'x', units='m')
        self.plotItem.setLabel('bottom', 'y', units='m')
        self.plotItem.setXRange(-115, 115)
        self.plotItem.setYRange(-200, 200)
        self.plotItem.showGrid(x=True, y=True, alpha=0.5)
        self.plotItem.addLine(x=0, pen=self.infLine_Pen)
        self.plotItem.addLine(y=0, pen=self.infLine_Pen)

        rect = QtGui.QGraphicsRectItem(QtCore.QRectF(-2, -5, 4, 5))
        rect.setPen(self.background_Pen)
        self.plotItem.vb.addItem(rect)

        pointF_list = []
        point1 = QtCore.QPointF(QtCore.QPoint(0, 0))
        point2 = QtCore.QPointF(QtCore.QPoint(-2, -2))
        point3 = QtCore.QPointF(QtCore.QPoint(2, -2))
        pointF_list.append(point1)
        pointF_list.append(point2)
        pointF_list.append(point3)
        pointF_list.append(point1)
        pointF = QtGui.QPolygonF(pointF_list)
        triangle = QtWidgets.QGraphicsPolygonItem(pointF)
        triangle.setPen(self.background_Pen)
        self.plotItem.vb.addItem(triangle)

    def updateData(self, count):
        """ when the timer is out, operate this funciton.
        """
        dataitems = self.plotItem.listDataItems()
        for dataitem in dataitems:
            self.plotItem.removeItem(dataitem)

        try:
            conn = sqlite3.connect(self.db_pth)
            curs = conn.cursor()
        except Exception:
            print('open db error in createXYDataTables')
            return False

        for radar_loc in constant.RADAR_LOCS:
            data = []
            sql = f"SELECT PosX_Left, PosX, PosX_Right, PosY_Left, PosY, PosY_Right, velX, velY FROM tracker_{count} WHERE Radar_Loc= ?"
            curs.execute(sql, (radar_loc,))
            data_list = curs.fetchall()

            for data in data_list:
                posX = [data[0], data[1], data[2]]
                posY = [data[3], data[4], data[5]]
                # change the pos-coordiante to vehicle-coordiante
                pos_item = pg.PlotDataItem(x=posY,
                                           y=posX,
                                           pen=self.rm_Pen,
                                           symbol='+',
                                           antialias=True)
                self.plotItem.addItem(pos_item)

                # define a scale to dispaly velocity
                vel_scale = 1
                velx = data[6] / vel_scale
                vely = data[7] / vel_scale

                # append the vel-point to pos-point
                velx = [posX[1], posX[1] + velx]
                vely = [posY[1], posY[1] + vely]

                vel_item = pg.PlotCurveItem(x=vely,
                                            y=velx,
                                            pen=self.rs_Pen,
                                            antialias=True)
                self.plotItem.addItem(vel_item)

        conn.close()
