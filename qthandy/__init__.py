import functools
from typing import Optional, Union

from qtpy.QtCore import Qt, QObject
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget, QApplication, QMessageBox, QSizePolicy, QFrame, QMenu, QLabel, QWidgetAction, \
    QPushButton, QToolButton, QVBoxLayout, QHBoxLayout, QLayout


def ask_confirmation(message: str, parent: Optional[QWidget] = None) -> bool:
    """Raise a confirmation dialog. Return True if the user clicked Yes, False otherwise."""
    QApplication.setOverrideCursor(QCursor(Qt.CursorShape.ArrowCursor))
    status: int = QMessageBox.question(parent, 'Confirmation', message)
    QApplication.restoreOverrideCursor()
    if status & QMessageBox.Yes:
        return True
    return False


def spacer(max_stretch: Optional[int] = None, vertical: bool = False) -> QWidget:
    spacer_ = QWidget()
    if vertical:
        spacer_.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        if max_stretch:
            spacer_.setMaximumHeight(max_stretch)
    else:
        spacer_.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        if max_stretch:
            spacer_.setMaximumWidth(max_stretch)

    return spacer_


def vspacer(max_height: Optional[int] = None) -> QWidget:
    return spacer(max_height, vertical=True)


def hspacer(max_width: Optional[int] = None) -> QWidget:
    return spacer(max_width)


def line(vertical: bool = False, parent: Optional[QWidget] = None) -> QFrame:
    line_ = QFrame(parent)
    if vertical:
        line_.setFrameShape(QFrame.VLine)
    else:
        line_.setFrameShape(QFrame.HLine)
    line_.setFrameShadow(QFrame.Sunken)

    return line_


def vline(parent: Optional[QWidget] = None) -> QFrame:
    return line(vertical=True, parent=parent)


def hline(parent: Optional[QWidget] = None) -> QFrame:
    return line(parent=parent)


def busy(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BusyCursor))
        try:
            return func(*args, **kwargs)
        finally:
            QApplication.restoreOverrideCursor()

    return wrapper_timer


def retain_when_hidden(widget: QWidget):
    policy = widget.sizePolicy()
    policy.setRetainSizeWhenHidden(True)
    widget.setSizePolicy(policy)


def transparent(widget: QWidget):
    if isinstance(widget, QLabel):
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    else:
        widget.setStyleSheet(f'{widget.__class__.__name__} {{border: 0px; background-color: rgba(0, 0, 0, 0);}}')


def incr_font(widget: QWidget, step: int = 1):
    font = widget.font()
    font.setPointSize(font.pointSize() + 1 * step)
    widget.setFont(font)


def decr_font(widget: QWidget, step: int = 1):
    font = widget.font()
    font.setPointSize(font.pointSize() - 1 * step)
    widget.setFont(font)


def bold(widget: QWidget, enabled: bool = True):
    font = widget.font()
    font.setBold(enabled)
    widget.setFont(font)


def italic(widget: QWidget, enabled: bool = True):
    font = widget.font()
    font.setItalic(enabled)
    widget.setFont(font)


def gc(object: QObject):
    object.setParent(None)
    object.deleteLater()


def btn_popup(btn: Union[QPushButton, QToolButton], popup: QWidget, showMenuIcon: bool = True):
    menu = QMenu(btn)
    action = QWidgetAction(menu)
    action.setDefaultWidget(popup)
    menu.addAction(action)
    if isinstance(btn, QToolButton):
        btn.setPopupMode(QToolButton.InstantPopup)
    if not showMenuIcon:
        btn.setStyleSheet(f'{btn.styleSheet()}\n{btn.__class__.__name__}::menu-indicator {{width:0px;}}')
    btn.setMenu(menu)


def clear_layout(target: Union[QWidget, QLayout]):
    if isinstance(target, QWidget):
        layout_: QLayout = target.layout()
    else:
        layout_ = target
    if layout_ is None:
        return

    while layout_.count():
        item = layout_.takeAt(0)
        if item.widget():
            gc(item.widget())


def hbox(widget: QWidget, margin: int = 2, spacing: int = 3) -> QHBoxLayout:
    _layout = QHBoxLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout


def vbox(widget: QWidget, margin: int = 2, spacing: int = 3) -> QVBoxLayout:
    _layout = QVBoxLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout
