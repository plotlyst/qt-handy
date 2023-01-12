import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel, QPushButton
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget

from qthandy import underline, bold, vbox, flow, btn_popup
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
        self.lbl.installEventFilter(DragEventFilter(self.lbl, 'application/text', lambda x: 'test', hideTarget=True))

        self.btnWithMenu = QPushButton('Btn with menu')
        self.btnWithMenu.setToolTip('Test tooltip')
        self.btnWithMenu.installEventFilter(InstantTooltipEventFilter(self.btnWithMenu))
        self.btnWithMenu.setAcceptDrops(True)
        self.btnWithMenu.installEventFilter(
            DropEventFilter(self.btnWithMenu, ['application/text'], motionDetection=Qt.Orientation.Horizontal,
                            droppedSlot=lambda mimeData: print('dropped')))

        widget = QWidget(self)
        btn = QPushButton('test', self.btnWithMenu)
        vbox(widget).addWidget(btn)
        btn.clicked.connect(lambda: widget.layout().addWidget(QLabel('another')))
        btn_popup(self.btnWithMenu, widget)

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
