import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, QFileDialog, qApp, \
    QTextEdit


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusBar()
        menubar = self.menuBar()

        openFile = QAction(QIcon("icons/62917-open-file-folder-icon.png"), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        exitAction = QAction(QIcon("icons/png-red-round-close-x-icon-31631915146jpppmdzihs.png")
                             , '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)

        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setGeometry(10, 25, 700, 100)

        self.textbox.append('Hello!')

        self.resize(750, 450)
        self.center()
        self.setWindowTitle('Parse alive sites')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.textbox.append(fname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
