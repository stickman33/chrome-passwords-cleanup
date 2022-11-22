import asyncio
import sys

from PyQt5.QtCore import QEventLoop
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, QFileDialog, qApp, \
    QTextEdit, QTextBrowser, QVBoxLayout, QCheckBox, QGridLayout, QWidget

import main


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


        layout1 = QGridLayout()
        self.setLayout(layout1)
        cbutton = QCheckBox("I have a Cat")
        cbutton.a = "Cat"
        layout1.addWidget(cbutton, 900, 900)

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



        self.text_browser = QTextBrowser(self)
        self.text_browser.setReadOnly(True)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setGeometry(10, 25, 700, 200)
        self.text_browser.append('Hello!')



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
        path_to_csv = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.text_browser.append(path_to_csv)
        run(ex, path_to_csv)




def run(exm, path):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main.multiprocessing_func(main.csv_list(), exm))
    bad_sites = {}
    csv_list = main.csv_list(path)


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main.multiprocessing_func(csv_list, exm, bad_sites))
    except KeyboardInterrupt:
        pass

    main.get_list_of_check_sites(bad_sites)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
