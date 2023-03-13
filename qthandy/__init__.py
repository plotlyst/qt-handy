import functools
from typing import Optional, Union

from qtpy.QtCore import Qt, QObject, QSize
from qtpy.QtGui import QCursor
from qtpy.QtWidgets import QWidget, QApplication, QMessageBox, QSizePolicy, QFrame, QMenu, QLabel, QWidgetAction, \
    QPushButton, QToolButton, QVBoxLayout, QHBoxLayout, QLayout, QGraphicsOpacityEffect, QGridLayout

from qthandy.layout import FlowLayout, CurvedFlowLayout


def ask_confirmation(message: str, parent=None) -> bool:
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


def line(vertical: bool = False, parent=None, color=None) -> QFrame:
    line_ = QFrame(parent)
    if vertical:
        line_.setFrameShape(QFrame.VLine)
    else:
        line_.setFrameShape(QFrame.HLine)
    line_.setFrameShadow(QFrame.Sunken)
    if color:
        line_.setStyleSheet(f'background-color: {color}; border: 1px solid {color};')

    return line_


def vline(parent=None, color=None) -> QFrame:
    return line(vertical=True, parent=parent, color=color)


def busy(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BusyCursor))
        try:
            return func(*args, **kwargs)
        finally:
            QApplication.restoreOverrideCursor()

    return wrapper_timer


def pointy(widget):
    widget.setCursor(Qt.CursorShape.PointingHandCursor)


def retain_when_hidden(widget):
    policy = widget.sizePolicy()
    policy.setRetainSizeWhenHidden(True)
    widget.setSizePolicy(policy)


def transparent(widget):
    if isinstance(widget, QLabel):
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    else:
        widget.setStyleSheet(f'{widget.__class__.__name__} {{border: 0px; background-color: rgba(0, 0, 0, 0);}}')


def incr_font(widget, step: int = 1):
    font = widget.font()
    font.setPointSize(font.pointSize() + 1 * step)
    widget.setFont(font)


def decr_font(widget, step: int = 1):
    font = widget.font()
    font.setPointSize(font.pointSize() - 1 * step)
    widget.setFont(font)


def bold(widget, enabled: bool = True):
    font = widget.font()
    font.setBold(enabled)
    widget.setFont(font)


def italic(widget, enabled: bool = True):
    font = widget.font()
    font.setItalic(enabled)
    widget.setFont(font)


def underline(widget, enabled: bool = True):
    font = widget.font()
    font.setUnderline(enabled)
    widget.setFont(font)


def translucent(wdg, opacity: float = 0.5):
    op = QGraphicsOpacityEffect(wdg)
    op.setOpacity(opacity)
    wdg.setGraphicsEffect(op)


def gc(obj: QObject):
    obj.setParent(None)
    obj.deleteLater()


def btn_popup(btn: Union[QPushButton, QToolButton], popup_widget, show_menu_icon: bool = False) -> QMenu:
    menu = _PopupMenu(popup_widget, btn)
    btn_popup_menu(btn, menu, show_menu_icon)
    return menu


class _PopupMenu(QMenu):

    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self._widget = widget
        action = QWidgetAction(self)
        action.setDefaultWidget(self._widget)
        self.addAction(action)

    def sizeHint(self) -> QSize:
        return self._widget.sizeHint()


def btn_popup_menu(btn: Union[QPushButton, QToolButton], menu: QMenu, show_menu_icon: bool = False):
    if isinstance(btn, QToolButton):
        btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
    if not show_menu_icon:
        btn.setStyleSheet(f'{btn.styleSheet()}\n{btn.__class__.__name__}::menu-indicator {{width:0px;}}')
    btn.setMenu(menu)


def clear_layout(target: Union[QWidget, QLayout], auto_delete: bool = True):
    if isinstance(target, QWidget):
        layout_: QLayout = target.layout()
    else:
        layout_ = target
    if layout_ is None:
        return

    while layout_.count():
        item = layout_.takeAt(0)
        if item.widget():
            if auto_delete:
                gc(item.widget())
            else:
                item.widget().setParent(None)


def hbox(widget, margin: int = 2, spacing: int = 3) -> QHBoxLayout:
    _layout = QHBoxLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout


def vbox(widget, margin: int = 2, spacing: int = 3) -> QVBoxLayout:
    _layout = QVBoxLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout


def grid(widget, margin: int = 2, h_spacing: int = 3, v_spacing: int = 3) -> QGridLayout:
    _layout = QGridLayout()
    _layout.setHorizontalSpacing(h_spacing)
    _layout.setVerticalSpacing(v_spacing)
    _layout.setContentsMargins(margin, margin, margin, margin)
    widget.setLayout(_layout)

    return _layout


def flow(widget, margin: int = 2, spacing: int = 3) -> FlowLayout:
    _layout = FlowLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout


def curved_flow(widget, margin: int = 2, spacing: int = 3) -> FlowLayout:
    _layout = CurvedFlowLayout()
    widget.setLayout(_layout)
    widget.layout().setContentsMargins(margin, margin, margin, margin)
    widget.layout().setSpacing(spacing)

    return _layout


def margins(widget, left=None, top=None, right=None, bottom=None):
    if widget.layout() is None:
        raise ValueError('Widget does not have a layout. Set a layout first to change the margins.')
    margins_ = widget.layout().contentsMargins()
    if left is not None:
        margins_.setLeft(left)
    if top is not None:
        margins_.setTop(top)
    if right is not None:
        margins_.setRight(right)
    if bottom is not None:
        margins_.setBottom(bottom)

    widget.layout().setContentsMargins(margins_)
