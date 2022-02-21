from qtpy.QtCore import QObject, QEvent
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget, QToolTip


class InstantTooltipEventFilter(QObject):
    def __init__(self, parent=None):
        super(InstantTooltipEventFilter, self).__init__(parent)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        print('event')
        if isinstance(watched, QWidget) and event.type() == QEvent.Enter:
            print('show')
            QToolTip.showText(QCursor.pos(), watched.toolTip())
        elif event.type() == QEvent.Leave:
            QToolTip.hideText()

        return super(InstantTooltipEventFilter, self).eventFilter(watched, event)
