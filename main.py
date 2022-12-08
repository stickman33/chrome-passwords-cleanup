import asyncio
import os
import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget, QFileDialog, qApp, \
    QTextBrowser, QPushButton, QDialog, QCheckBox, QLabel, QGridLayout, \
    QVBoxLayout, QProgressBar

import processing


class Thread(QThread):
    _signal = pyqtSignal(int)

    def __init__(self):
        super(Thread, self).__init__()

    # def __del__(self):
    #     self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)


def resource_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.statusBar()
        menubar = self.menuBar()

        folder_icon = QIcon(resource_path("icons/open-file-folder-icon.png"))
        openFile = QAction(folder_icon, 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.show_file_dialog)

        exit_icon = QIcon(resource_path("icons/red-round-close-x-icon.png"))
        exitAction = QAction(exit_icon, '&Exit', self)
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

        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.pbar.setGeometry(10, 250, 200, 30)
        self.pbar.hide()

        self.text_browser.append('Hello!')
        # self.signal_accept(98)

        self.thread = Thread()
        # self.thread._signal.connect(self.signal_accept)
        self.thread.start()

        self.resize(750, 450)
        self.center()
        self.setWindowTitle('Chrome passwords cleanup')

        self.show()

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def center_pos(self):
        qr = QMainWindow.window(self).frameGeometry()
        x = (qr.width() - self.width()) / 2
        y = (qr.height() - self.height()) / 2
        self.move(x, y)

    def show_file_dialog(self):
        global path_to_csv
        file_dialog = QFileDialog()
        path_to_csv = file_dialog.getOpenFileName(self, 'Open file', '')[0]
        if path_to_csv:
            self.text_browser.append(f'Chosen file: {path_to_csv}')
            self.do_action(ex)
        else:
            file_dialog.close()
        # run(ex)

    def create_checkboxes(self, list_of_sites, bad_urls_list):
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
        self.buttonOk.clicked.connect(self.checkbox_changed)

        grid.addWidget(self.buttonOk, len(list_of_sites) + 10, 0, 1, 2)

        self.confirm.setLayout(grid)

    def checkbox_changed(self):
        for i, v in enumerate(self.listCheckBox):
            doc = QtGui.QTextDocument()
            doc.setHtml(self.listLabel[i].text())
            text = doc.toRawText()
            if v.checkState():
                self.resultList.append(text)
        self.confirm.close()
        processing.remove_invalid_sites(self.resultList, path_to_csv)
        self.text_browser.append('Cleaned password file has been stored in the same location as input one')
        self.text_browser.append('Done!')

    def do_action(self, window):
        bad_sites = {}
        csv_list = processing.csv_list(path_to_csv)
        length = len(csv_list)
        self.worker = MainBackgroundThread(csv_list, window, bad_sites, length)
        self.pbar.show()
        self.worker.finished.connect(self.input_dialog)
        self.worker.start()

    def input_dialog(self):
        self.confirm = QDialog()
        self.confirm.setWindowTitle('Check the following web-sites')
        self.confirm.resize(200, 100)
        list_to_check, bad_urls_list = processing.get_list_of_check_sites(self.worker.bad_sites)
        self.create_checkboxes(list_to_check, bad_urls_list)
        self.confirm.show()


class MainBackgroundThread(QThread):
    def __init__(self, csv_list, window, bad_sites, length):
        QThread.__init__(self)
        self.csv_list, self.window, self.bad_sites, self.length = csv_list, window, bad_sites, length

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(processing.multiprocessing_func(self.csv_list, self.window,
                                                                self.bad_sites, self.length))
        loop.run_until_complete(asyncio.sleep(0.250))
        loop.close()

        def task_result(tasks):
            res = []
            for t in tasks:
                try:
                    r = t.result()
                except BaseException as e:
                    res.append(e)
                    continue
                res.append(r)

            print(res)


# if QtCore.QT_VERSION >= 0x50501:
#     def excepthook(type_, value, traceback_):
#         traceback.print_exception(type_, value, traceback_)
#         QtCore.qFatal('')
# sys.excepthook = excepthook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
