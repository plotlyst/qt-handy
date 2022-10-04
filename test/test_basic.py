import sys

import pytest
from qtpy.QtWidgets import QLabel, QWidget, QPushButton, QApplication, QToolButton, QMessageBox

from qthandy import translucent, hbox, retain_when_hidden, spacer, transparent, busy, btn_popup, ask_confirmation
from test.common import is_darwin, is_pyqt6


def test_translucent(qtbot):
    widget = QLabel('Test')
    qtbot.addWidget(widget)
    widget.show()

    translucent(widget)

    assert widget.graphicsEffect()


def test_retain_when_hidden(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent)
    stretched_btn = QPushButton('Stretched')
    btn = QPushButton()
    btn.setFixedWidth(100)
    parent.layout().addWidget(stretched_btn)
    parent.layout().addWidget(btn)

    qtbot.addWidget(parent)
    parent.show()

    prev_btn_size = stretched_btn.width()
    retain_when_hidden(btn)
    btn.setHidden(True)
    qtbot.wait(5)
    assert prev_btn_size == stretched_btn.width()


def test_spacer(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent)

    btn = QPushButton('Button')
    btn.setMinimumWidth(100)

    parent.layout().addWidget(spacer())
    parent.layout().addWidget(btn)
    qtbot.addWidget(parent)
    parent.show()

    assert btn.width() == 100


def test_spacer_with_max_stretch(qtbot):
    parent = QWidget()
    parent.setFixedWidth(300)
    hbox(parent, 0, 0)

    btn = QPushButton('Button')
    btn.setMinimumWidth(100)

    parent.layout().addWidget(spacer(max_stretch=150))
    parent.layout().addWidget(btn)
    qtbot.addWidget(parent)
    parent.show()

    if is_darwin():
        assert btn.width() == 150 if is_pyqt6() else 156
    else:
        assert btn.width() == 150


def test_transparent_label(qtbot):
    lbl = QLabel('Test')
    transparent(lbl)


@pytest.mark.skipif('PySide6' in sys.modules, reason="Cannot set override cursor with PySide6")
def test_busy(qtbot):
    @busy
    def busy_func():
        assert QApplication.overrideCursor()

    assert not QApplication.overrideCursor()
    busy_func()
    assert not QApplication.overrideCursor()


def test_btn_popup(qtbot):
    btn = QToolButton()
    qtbot.addWidget(btn)
    btn.show()

    lbl = QLabel('Test')
    btn_popup(btn, lbl)

    assert btn.menu()
    assert btn.popupMode() == QToolButton.ToolButtonPopupMode.InstantPopup


def test_confirmation(qtbot, monkeypatch):
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)  # confirm
    confirmed = ask_confirmation('Confirmation')
    assert confirmed

    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)  # confirm
    confirmed = ask_confirmation('Confirmation')
    assert not confirmed
