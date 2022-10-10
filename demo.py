import sys

from qtpy.QtWidgets import QLabel, QPushButton, QMenu
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget

from qthandy import underline, bold, vbox, btn_popup_menu, ask_confirmation, flow
from qthandy.filter import InstantTooltipEventFilter, DragEventFilter, DropEventFilter


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        vbox(self.widget)

        self.lbl = QLabel('Underline Text')
        underline(self.lbl)
        bold(self.lbl)
        self.lbl.installEventFilter(DragEventFilter(self.lbl, 'application/text', lambda x: 'test', hideParent=True))

        self.btnWithMenu = QPushButton('Btn with menu')
        self.btnWithMenu.setToolTip('Test tooltip')
        self.btnWithMenu.installEventFilter(InstantTooltipEventFilter(self.btnWithMenu))
        self.btnWithMenu.setAcceptDrops(True)
        self.btnWithMenu.installEventFilter(
            DropEventFilter(self.btnWithMenu, ['application/text'], slot=lambda: print('dropped')))

        menu = QMenu(self.btnWithMenu)
        menu.addAction('Test', lambda: ask_confirmation('Test'))
        btn_popup_menu(self.btnWithMenu, menu)

        self.wdgFlow = QWidget()
        flow(self.wdgFlow)

        for i in range(15):
            self.wdgFlow.layout().addWidget(QLabel(f'Label {i + 1}'))

        self.widget.layout().addWidget(self.lbl)
        self.widget.layout().addWidget(self.btnWithMenu)
        self.widget.layout().addWidget(self.wdgFlow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
