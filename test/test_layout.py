from qtpy.QtWidgets import QWidget, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout

from qthandy import vbox, clear_layout, hbox


def test_clear_layout(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = vbox(widget)
    layout.addWidget(QPushButton('Btn1', widget))
    layout.addWidget(QPushButton('Btn2', widget))
    layout.addSpacerItem(QSpacerItem(50, 50, vPolicy=QSizePolicy.Expanding))

    clear_layout(widget)
    assert layout.count() == 0


def test_hbox(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = hbox(widget)

    assert widget.layout() is not None
    assert widget.layout() is layout
    assert isinstance(widget.layout(), QHBoxLayout)


def test_vbox(qtbot):
    widget = QWidget()
    qtbot.addWidget(widget)
    widget.show()

    layout = vbox(widget)

    assert widget.layout() is not None
    assert widget.layout() is layout
    assert isinstance(widget.layout(), QVBoxLayout)
