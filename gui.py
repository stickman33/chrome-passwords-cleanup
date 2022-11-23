import asyncio
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
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

        self.text_browser = QTextBrowser(self)
        self.text_browser.setReadOnly(True)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setGeometry(10, 25, 730, 200)
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
        path_to_csv = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.text_browser.append(path_to_csv)
        run(ex, path_to_csv)

    def createCheckBoxes(self, list_of_sites):
        self.listCheckBox = [''] * len(list_of_sites)
        self.listLabel = list_of_sites
        self.title = QLabel()
        self.title.setText('Select not working sites:')
        grid = QGridLayout()

        for i, v in enumerate(self.listLabel):
            self.listCheckBox[i] = QCheckBox()

            self.listLabel[i] = QLabel()
            self.listLabel[i].setOpenExternalLinks(True)
            self.listLabel[i].setText(f'<a href=\'{v}\'>{v}</a>')

            grid.addWidget(self.title, 0, 0)
            grid.addWidget(self.listCheckBox[i], i + 1, 0)
            grid.addWidget(self.listLabel[i], i + 1, 1)

        # self.button = QPushButton("Check CheckBox")
        # self.button.clicked.connect(self.checkboxChanged)
        # self.labelResult = QLabel()

        # grid.addWidget(self.button, 10, 0, 1, 2)
        # grid.addWidget(self.labelResult, 11, 0, 1, 2)
        self.confirm.setLayout(grid)


    def showInputDialog(self, list_of_urls):
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
        self.confirm.resize(300, 300)

        self.createCheckBoxes(list_of_urls)

        # self.confirm.setGeometry(300, 300, 290, 150)

        self.confirm.show()


def run(exm, path):
    bad_sites = {}
    csv_list = main.csv_list(path)
    length = len(csv_list)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main.multiprocessing_func(csv_list, exm, bad_sites, length))
    except KeyboardInterrupt:
        pass
    list_to_check, bad_urls_list = main.get_list_of_check_sites(bad_sites)

    # if list_to_check is not None:
    #     print('Check the following web-sites manually and input not working ones by their indexes:')
    #     exm.text_browser.append('')
    #     exm.text_browser.append('Check the following web-sites manually and input not working ones by their indexes:')
    #
    # for index_of_site, site_url in list_to_check.items():
    #     print(f'{index_of_site}. {site_url}')
    #     exm.text_browser.append(f'{index_of_site}. <a href=\'{site_url}\'>{site_url}</a>')

    exm.showInputDialog(list_to_check)
    # print(list_to_check)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
