import sys

from qtpy.QtWidgets import QLabel, QPushButton, QMenu
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget

from qthandy import underline, bold, vbox, btn_popup_menu


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        vbox(self.widget)

        self.lbl = QLabel('Underline Text')
        underline(self.lbl)
        bold(self.lbl)

        self.btnWithMenu = QPushButton('Btn with menu')

        menu = QMenu(self.btnWithMenu)
        menu.addAction('Test')
        btn_popup_menu(self.btnWithMenu, menu)
        self.widget.layout().addWidget(self.lbl)
        self.widget.layout().addWidget(self.btnWithMenu)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
