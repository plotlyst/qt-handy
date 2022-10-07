import pickle

from qtpy import PYSIDE2
from qtpy.QtCore import QObject, QEvent, Signal, QMimeData, QByteArray
from qtpy.QtGui import QCursor, QDrag
from qtpy.QtWidgets import QWidget, QToolTip, QPushButton, QToolButton


class InstantTooltipEventFilter(QObject):
    def __init__(self, parent=None):
        super(InstantTooltipEventFilter, self).__init__(parent)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() == QEvent.Enter:
            QToolTip.showText(QCursor.pos(), watched.toolTip())
        elif event.type() == QEvent.Leave:
            QToolTip.hideText()

        return super(InstantTooltipEventFilter, self).eventFilter(watched, event)


class DragEventFilter(QObject):
    dragStarted = Signal()
    dragFinished = Signal()

    def __init__(self, watched, mimeType: str, dataFunc, grabbed=None):
        super(DragEventFilter, self).__init__(watched)
        self._pressed: bool = False
        self._mimeType = mimeType
        self._dataFunc = dataFunc
        self._grabbed = grabbed

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            self._pressed = True
        elif event.type() == QEvent.MouseButtonRelease:
            self._pressed = False
        elif event.type() == QEvent.MouseMove and self._pressed:
            drag = QDrag(watched)
            if self._grabbed:
                pix = self._grabbed.grab()
            else:
                pix = watched.grab()
            mimedata = QMimeData()
            mimedata.setData(self._mimeType, QByteArray(pickle.dumps(self._dataFunc(watched))))
            drag.setMimeData(mimedata)
            drag.setPixmap(pix)
            drag.setHotSpot(event.pos())
            drag.destroyed.connect(self.dragFinished.emit)
            self.dragStarted.emit()
            if PYSIDE2:
                drag.exec_()
            else:
                drag.exec()
        return super(DragEventFilter, self).eventFilter(watched, event)


class DisabledClickEventFilter(QObject):
    clicked = Signal()

    def __init__(self, watched, slot=None):
        super(DisabledClickEventFilter, self).__init__(watched)
        self._slot = slot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() == QEvent.MouseButtonRelease and not watched.isEnabled():
            self.clicked.emit()
            if self._slot:
                self._slot()

        return super(DisabledClickEventFilter, self).eventFilter(watched, event)


class VisibilityToggleEventFilter(QObject):

    def __init__(self, target: QWidget, watched: QWidget, freezeForMenu: bool = True):
        super(VisibilityToggleEventFilter, self).__init__(watched)
        self.target = target
        self.target.setHidden(True)
        self._frozen: bool = False

        if freezeForMenu and isinstance(self.target, (QPushButton, QToolButton)) and self.target.menu():
            self.target.menu().aboutToShow.connect(self.freeze)
            self.target.menu().aboutToHide.connect(self.resume)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self._frozen:
            return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)
        if event.type() == QEvent.Enter:
            self.target.setVisible(True)
        elif event.type() == QEvent.Leave:
            self.target.setHidden(True)

        return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)

    def freeze(self):
        self._frozen = True

    def resume(self):
        self._frozen = False
        self.target.setHidden(True)
