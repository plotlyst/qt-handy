from qtpy.QtCore import Qt, QTimer, QEvent
from qtpy.QtGui import QMoveEvent, QEnterEvent
from qtpy.QtWidgets import QPushButton, QLabel, QApplication, QWidget

from qthandy import vbox, btn_popup
from qthandy.filter import InstantTooltipEventFilter, DragEventFilter, DisabledClickEventFilter, \
    VisibilityToggleEventFilter


class FakeMouseMove(QMoveEvent):
    def __init__(self, pos, old_pos):
        super(FakeMouseMove, self).__init__(pos, old_pos)

    def type(self) -> 'QEvent.Type':
        return QEvent.MouseMove


class FakeEnterEvent(QEnterEvent):
    def __init__(self, pos):
        super(FakeEnterEvent, self).__init__(pos, pos, pos)

    def type(self) -> 'QEvent.Type':
        return QEvent.Enter


class FakeLeaveEvent(QEnterEvent):
    def __init__(self, pos):
        super(FakeLeaveEvent, self).__init__(pos, pos, pos)

    def type(self) -> 'QEvent.Type':
        return QEvent.Leave


def test_instant_tooltip(qtbot):
    btn = QPushButton('Button')
    qtbot.addWidget(btn)
    btn.show()

    btn.setToolTip('Test button')
    btn.installEventFilter(InstantTooltipEventFilter(btn))


def drop(qtbot, wdg):
    qtbot.mouseRelease(wdg, Qt.LeftButton, delay=30)


def test_drag(qtbot):
    label = QLabel('Test label')
    filter = DragEventFilter(label, 'application/text', lambda x: 'data')
    label.installEventFilter(filter)
    qtbot.addWidget(label)
    label.show()

    qtbot.wait(50)

    with qtbot.waitSignals([filter.dragStarted, filter.dragFinished], timeout=1000):
        qtbot.mouseMove(label)
        qtbot.mousePress(label, Qt.LeftButton, delay=30)

        QTimer.singleShot(100, lambda: drop(qtbot, label))
        event = FakeMouseMove(label.rect().bottomLeft(), label.rect().center())
        QApplication.sendEvent(label, event)


def test_disabled_click(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)
    btn.show()

    filter = DisabledClickEventFilter(btn, slot=lambda: 'test')
    btn.installEventFilter(filter)
    btn.setDisabled(True)

    with qtbot.waitSignal(filter.clicked, timeout=1000):
        qtbot.mouseClick(btn, Qt.LeftButton)


def test_visibility_toggle(qtbot):
    parent = QWidget()
    vbox(parent, margin=10)

    btn = QPushButton('Test')
    btn_popup(btn, QLabel('Test'))
    parent.layout().addWidget(btn)

    qtbot.addWidget(parent)
    parent.show()

    parent.installEventFilter(VisibilityToggleEventFilter(btn, parent))
    assert btn.isHidden()

    event = FakeEnterEvent(parent.rect().center())
    QApplication.sendEvent(parent, event)
    assert btn.isVisible()

    event = FakeLeaveEvent(parent.rect().center())
    QApplication.sendEvent(parent, event)
    assert btn.isHidden()
