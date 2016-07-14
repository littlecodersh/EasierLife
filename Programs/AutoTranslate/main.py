#!python3
import sys, threading
import traceback

from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
        QPushButton, QTextEdit)
from PyQt5.QtCore import pyqtSignal, QObject, Qt

from models.TranslateClient import TranslateClient

PORT = 1080
RETRY = 3

class Clipboard(object):
    def __init__(self, clipboard):
        self.clipboard = clipboard
        self.lock = False
        self.contentThread = self._content_thread()
    def _content_thread(self):
        def __clipboard_set(msg):
            self.lock = True
            def fn(): self.lock = False
            self.clipboard.setText(msg)
            threading.Timer(.1, fn).start()
        while 1:
            __clipboard_set((yield))
    def set(self, msg):
        self.contentThread.send(None)
        self.contentThread.send(msg)
    def get(self):
        data = self.clipboard.mimeData()
        if not data.hasText(): return ''
        return data.text()
class Communication(QObject):
    translateFinish = pyqtSignal()
class MainWindow(QMainWindow):
    text = ''
    def __init__(self, app):
        super().__init__(None, Qt.WindowStaysOnTopHint)
        self.init_ui()
        self.set_communication()
        self.set_clipboard(app)
        self.set_translation()
        self.show_info('准备好了')
    def init_ui(self):
        self.setWindowOpacity(.7)
        self.setWindowTitle('翻译小能手')
        self.resize(200, 100)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
    def set_communication(self):
        self.communication = Communication()
        self.communication.translateFinish.connect(self.update_main_window)
    def set_clipboard(self, app):
        clipboard = app.clipboard()
        clipboard.dataChanged.connect(self.clipboard_changed)
        self.clipboard = Clipboard(clipboard)
    def set_translation(self):
        self.tc = TranslateClient()
        self.tc.set_proxies({})
    def update_main_window(self, finish = True):
        if self.text:
            self.show_text(self.text)
            self.show_info('翻译成功' if finish else '翻译中')
            # set function should be run in main thread
            if finish: self.clipboard.set(self.text)
        else:
            self.show_info('翻译失败')
    def clipboard_changed(self):
        if self.clipboard.lock: return
        text = self.clipboard.get()
        if text == '': return
        self.text = text
        self.update_main_window(False)
        translateThread = threading.Thread(target = self._translate, args = (text, ))
        translateThread.setDaemon(True)
        translateThread.start()
    def _translate(self, text):
        for i in range(RETRY): # set retry
            try:
                text = self.tc.get(text)
            except:
                if i == 2:
                    traceback.print_exc()
                    self.text = ''
                    break
        else:
            self.text = text
        self.communication.translateFinish.emit()
    def show_text(self, msg):
        self.textEdit.setText(msg)
    def show_info(self, msg):
        self.statusBar().showMessage(msg)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow(app)
    mainWindow.show()
    mainWindow.show_text('测试')
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
