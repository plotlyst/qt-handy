from qtpy.QtWidgets import QWidget

from qthandy import hline, vbox, vline


def test_line(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    vbox(widget)
    widget.layout().addWidget(hline())
    widget.layout().addWidget(vline())

    assert widget.layout().count() == 2
