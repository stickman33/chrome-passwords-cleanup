import asyncio
import os
import sys
import traceback

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, QFileDialog, qApp, \
    QTextBrowser, QInputDialog, QLineEdit, QPushButton, QDialog, QMessageBox, QCheckBox, QLabel, QGridLayout, \
    QVBoxLayout, QWidget

import main

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
        openFile.triggered.connect(self.showFileDialog)

        exitAction = QAction(QIcon("icons/png-red-round-close-x-icon-31631915146jpppmdzihs.png")
                             , '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)

        font = QFont('Times', 12)

        self.text_browser = QTextBrowser(self)
        self.text_browser.setReadOnly(True)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setGeometry(10, 25, 730, 200)
        self.text_browser.setFont(font)

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

    def centerPos(self):
        qr = QMainWindow.window(self).frameGeometry()
        x = (qr.width() - self.width()) / 2
        y = (qr.height() - self.height()) / 2
        self.move(x, y)

    def showFileDialog(self):
        global path_to_csv
        path_to_csv = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.text_browser.append(path_to_csv)
        self.doAction(ex)
        # run(ex)


    def createCheckBoxes(self, list_of_sites, bad_urls_list):
        self.resultList = bad_urls_list

        self.listCheckBox = [''] * len(list_of_sites)
        self.listLabel = list_of_sites

        self.title = QLabel()
        self.title.setText('Select not working sites:')

        grid = QGridLayout()
        grid.addWidget(self.title, 0, 0, 1, 40)

        for i, v in enumerate(self.listLabel):
            self.listCheckBox[i] = QCheckBox()

            self.listLabel[i] = QLabel()
            self.listLabel[i].setOpenExternalLinks(True)
            self.listLabel[i].setText(f'<a href=\'{v}\'>{v}</a>')


            grid.addWidget(self.listCheckBox[i], i + 1, 1)
            grid.addWidget(self.listLabel[i], i + 1, 2)

        self.buttonOk = QPushButton("OK")
        self.buttonOk.clicked.connect(self.checkboxChanged)

        grid.addWidget(self.buttonOk, len(list_of_sites) + 10, 0, 1, 2)

        # self.button = QPushButton("Check CheckBox")
        # self.button.clicked.connect(self.checkboxChanged)
        # self.labelResult = QLabel()

        # grid.addWidget(self.button, 10, 0, 1, 2)
        # grid.addWidget(self.labelResult, 11, 0, 1, 2)

        self.confirm.setLayout(grid)

    def checkboxChanged(self):
        for i, v in enumerate(self.listCheckBox):
            doc = QtGui.QTextDocument()
            doc.setHtml(self.listLabel[i].text())
            text = doc.toRawText()
            if v.checkState():
                self.resultList.append(text)
        self.confirm.close()
        main.remove_invalid_sites(self.resultList, path_to_csv)
        self.text_browser.append('Done!')



    def showInputDialog(self, list_of_urls, bad_urls_list):
        # self.setGeometry(300, 300, 290, 150)
        # self.resize(750, 450)
        # self.center()
        #
        # text, ok = QInputDialog.getText(self, 'Input Dialog', 'Input indexes:')
        #
        # if ok:
        #     print(str(text))
        # else:
        #     confirm = QMessageBox.question(self, 'Abort', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        #     if confirm == QMessageBox.No:
        #         self.showInputDialog()

        self.confirm = QDialog()
        self.confirm.setWindowTitle('Check the following web-sites')
        self.confirm.resize(200, 100)

        self.createCheckBoxes(list_of_urls, bad_urls_list)

        # self.confirm.setGeometry(300, 300, 290, 150)

        self.confirm.show()

    def doAction(self, window):
        bad_sites = {}
        csv_list = main.csv_list(path_to_csv)
        length = len(csv_list)
        self.worker = MainBackgroundThread(csv_list, window, bad_sites, length)
        self.worker.start()

        list_to_check, bad_urls_list = main.get_list_of_check_sites(bad_sites)

        self.showInputDialog(list_to_check, bad_urls_list)

# def run(window):
    # bad_sites = {}
    # csv_list = main.csv_list(path_to_csv)
    # length = len(csv_list)

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # try:
    #     loop.run_until_complete(main.multiprocessing_func(csv_list, window, bad_sites, length))
    # except KeyboardInterrupt:
    #     pass

    # window.doAction(csv_list, window, bad_sites, length)
    #
    # list_to_check, bad_urls_list = main.get_list_of_check_sites(bad_sites)
    #
    # window.showInputDialog(list_to_check, bad_urls_list)


class MainBackgroundThread(QThread):
    def __init__(self, csv_list, window, bad_sites, length):
        QThread.__init__(self)
        self.csv_list, self.window, self.bad_sites, self.length = csv_list, window, bad_sites, length
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(main.multiprocessing_func(self.csv_list, self.window, self.bad_sites, self.length))
        except Exception as exc:
            print(exc)


if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


