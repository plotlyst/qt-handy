from PyQt6.QtWidgets import QLabel

from qthandy import opaque


def test_opaque(qtbot):
    widget = QLabel('Test')
    qtbot.addWidget(widget)
    widget.show()

    opaque(widget)

    assert widget.graphicsEffect()
