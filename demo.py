import sys

from PyQt6.QtWidgets import QLabel
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget

from qthandy import underline, bold, vbox


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.lbl = QLabel('Underline Text')
        underline(self.lbl)
        bold(self.lbl)

        vbox(self.widget)
        self.widget.layout().addWidget(self.lbl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
