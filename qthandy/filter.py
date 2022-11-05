import pickle
from typing import List

from qtpy import PYSIDE2
from qtpy.QtCore import QObject, QEvent, Signal, QMimeData, QByteArray
from qtpy.QtGui import QCursor, QDrag
from qtpy.QtWidgets import QWidget, QToolTip, QPushButton, QToolButton, QAbstractButton

from qthandy import translucent


class InstantTooltipEventFilter(QObject):
    def __init__(self, parent):
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

    def __init__(self, target, mimeType: str, dataFunc, grabbed=None, hideTarget: bool = False):
        super(DragEventFilter, self).__init__(target)
        self._target = target
        self._pressed: bool = False
        self._hideTarget = hideTarget
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
            self.dragStarted.emit()
            if self._hideTarget:
                self._target.setHidden(True)
            if PYSIDE2:
                drag.exec_()
            else:
                drag.exec()
            self.dragFinished.emit()
            if self._hideTarget:
                self._target.setVisible(True)
        return super(DragEventFilter, self).eventFilter(watched, event)


class DropEventFilter(QObject):
    dropped = Signal(QMimeData)

    def __init__(self, parent, mimeTypes: List[str], slot=None):
        super(DropEventFilter, self).__init__(parent)
        self._mimeTypes = mimeTypes
        self._slot = slot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.DragEnter:
            for mime in self._mimeTypes:
                if event.mimeData().hasFormat(mime):
                    event.accept()
        elif event.type() == QEvent.Drop:
            self.dropped.emit(event.mimeData())
            if self._slot:
                self._slot()
            event.accept()

        return super(DropEventFilter, self).eventFilter(watched, event)


class DisabledClickEventFilter(QObject):
    clicked = Signal()

    def __init__(self, parent, slot=None):
        super(DisabledClickEventFilter, self).__init__(parent)
        self._slot = slot

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, QWidget) and event.type() == QEvent.MouseButtonRelease and not watched.isEnabled():
            self.clicked.emit()
            if self._slot:
                self._slot()

        return super(DisabledClickEventFilter, self).eventFilter(watched, event)


class VisibilityToggleEventFilter(QObject):

    def __init__(self, target: QWidget, parent: QWidget, freezeForMenu: bool = True):
        super(VisibilityToggleEventFilter, self).__init__(parent)
        self.target = target
        self.target.setHidden(True)
        self._frozen: bool = False

        if freezeForMenu and isinstance(self.target, (QPushButton, QToolButton)) and self.target.menu():
            self.target.menu().aboutToShow.connect(self._freeze)
            self.target.menu().aboutToHide.connect(self._resume)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self._frozen:
            return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)
        if event.type() == QEvent.Enter:
            self.target.setVisible(True)
        elif event.type() == QEvent.Leave:
            self.target.setHidden(True)

        return super(VisibilityToggleEventFilter, self).eventFilter(watched, event)

    def _freeze(self):
        self._frozen = True

    def _resume(self):
        self._frozen = False
        self.target.setHidden(True)


class OpacityEventFilter(QObject):

    def __init__(self, parent, enterOpacity: float = 1.0, leaveOpacity: float = 0.4,
                 ignoreCheckedButton: bool = False):
        super(OpacityEventFilter, self).__init__(parent)
        self._enterOpacity = enterOpacity
        self._leaveOpacity = leaveOpacity
        self._ignoreCheckedButton = ignoreCheckedButton
        self._parent = parent
        if not ignoreCheckedButton or not self._checkedButton(parent):
            translucent(parent, leaveOpacity)
        if parent and isinstance(parent, QAbstractButton):
            parent.toggled.connect(self._btnToggled)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if self._ignoreCheckedButton and self._checkedButton(watched) or not watched.isEnabled():
            return super(OpacityEventFilter, self).eventFilter(watched, event)
        if event.type() == QEvent.Type.Enter:
            translucent(watched, self._enterOpacity)
        elif event.type() == QEvent.Type.Leave:
            translucent(watched, self._leaveOpacity)

        return super(OpacityEventFilter, self).eventFilter(watched, event)

    def _checkedButton(self, obj: QObject) -> bool:
        return isinstance(obj, QAbstractButton) and obj.isChecked()

    def _btnToggled(self, toggled: bool):
        if toggled:
            translucent(self._parent, self._enterOpacity)
        else:
            translucent(self._parent, self._leaveOpacity)
