from qtpy.QtWidgets import QLabel

from qthandy import translucent


def test_translucent(qtbot):
    widget = QLabel('Test')
    qtbot.addWidget(widget)
    widget.show()

    translucent(widget)

    assert widget.graphicsEffect()
