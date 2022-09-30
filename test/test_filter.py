import platform
from unittest.mock import create_autospec

import pytest
from qtpy.QtCore import Qt, QEvent, QTimer
from qtpy.QtWidgets import QPushButton, QLabel

from qthandy.filter import InstantTooltipEventFilter, DragEventFilter


@pytest.mark.skipif(platform.system() == 'Darwin', reason="Cannot run on Darwin")
def test_instant_tooltip(qtbot):
    btn = QPushButton('Button')
    qtbot.addWidget(btn)
    btn.show()

    btn.setToolTip('Test button')
    btn.installEventFilter(InstantTooltipEventFilter(btn))
    qtbot.wait(50)
    qtbot.mouseMove(btn)


def drop(qtbot, wdg):
    qtbot.mouseRelease(wdg, Qt.LeftButton, delay=30)


def test_drag(qtbot):
    label = QLabel('Test label')
    filter = DragEventFilter(label, 'application/text', lambda x: 'data')
    label.installEventFilter(filter)
    qtbot.addWidget(label)
    label.show()

    qtbot.wait(50)

    with qtbot.waitSignals([filter.dragStarted, filter.dragFinished]):
        qtbot.mouseMove(label)
        qtbot.mousePress(label, Qt.LeftButton, delay=30)

        event = create_autospec(QEvent)
        event.type = lambda: QEvent.MouseMove
        event.pos = lambda: label.rect().center()
        QTimer.singleShot(100, lambda: drop(qtbot, label))
        try:
            filter.eventFilter(label, event)
        except TypeError:  # coming from super
            pass
