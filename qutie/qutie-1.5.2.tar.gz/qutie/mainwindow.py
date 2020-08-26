import weakref

from .qt import QtCore
from .qt import QtWidgets
from .qt import bind

from .action import Action
from .menu import Menu
from .menubar import MenuBar
from .toolbar import ToolBar
from .widget import BaseWidget

__all__ = ['MainWindow']

@bind(QtWidgets.QStatusBar)
class StatusBar(BaseWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append(self, widget):
        self.qt.addPermanentWidget(widget.qt)
        return widget

@bind(QtWidgets.QMainWindow)
class MainWindow(BaseWidget):

    class ToolBars:

        def __init__(self, qt):
            self.__qt = qt
            self.__toolbars = set()

        def clear(self):
            for item in self.__toolbars:
                self.__qt.removeToolBar(item.qt)
            self.__toolbars.clear()

        def add(self, item):
            if isinstance(item, str):
                item = ToolBar(title=item)
            self.__qt.addToolBar(item.qt)
            self.__toolbars.add(item)
            return item

        def remove(self, item):
            if item in self.__toolbars:
                self.__qt.removeToolBar(item.qt)
                self.__toolbars.remove(item)

        def __iter__(self):
            return iter(self.__toolbars)

        def __len__(self):
            return len(self.__toolbars)

    def __init__(self, *, layout=None, **kwargs):
        super().__init__(**kwargs)
        self.qt.setMenuBar(MenuBar().qt)
        self.qt.setStatusBar(StatusBar().qt)
        self.layout = layout
        self.__toolbars = self.ToolBars(self.qt)

    @property
    def layout(self):
        widget = self.qt.centralWidget()
        if widget is not None:
            return widget.property(self.QtPropertyKey)
        return None

    @layout.setter
    def layout(self, value):
        if value is None:
            self.qt.setCentralWidget(None)
        else:
            if not isinstance(value, BaseWidget):
                raise ValueError(value)
            self.qt.setCentralWidget(value.qt)

    @property
    def menubar(self):
        return self.qt.menuBar().property(self.QtPropertyKey)

    @property
    def statusbar(self):
        return self.qt.statusBar().property(self.QtPropertyKey)

    @property
    def toolbars(self):
        return self.__toolbars
