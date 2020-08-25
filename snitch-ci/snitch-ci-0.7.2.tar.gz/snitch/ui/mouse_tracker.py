from PyQt5.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QFrame, QLabel

import pyautogui


class MouseTracker(QObject):
    """ Object for tracking mouse position """
    position_changed = pyqtSignal((str,), (int, int))

    def __init__(self, parent=None):
        super().__init__(parent)

        self._mousepos_timer = QTimer(self)
        self._mousepos_timer.timeout.connect(self._update_mouse_position)
        self._mousepos_timer.start(50)

    @pyqtSlot()
    def _update_mouse_position(self):
        self.position_changed[str].emit('x={} ; y={}'.format(*pyautogui.position()))
        self.position_changed[int, int].emit(*list(pyautogui.position()))

    def get_widget(self, parent=None):
        """ Provides a QLabel connected to this object showing the mouse position """
        label = QLabel(parent)
        label.setMinimumWidth(120)
        label.setFrameShape(QFrame.Panel)
        label.setFrameShadow(QFrame.Sunken)
        label.setAlignment(Qt.AlignCenter)
        self.position_changed.connect(label.setText)
        return label
