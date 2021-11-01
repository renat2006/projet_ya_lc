import sys
# import time
# import comtypes.client
# import win32com
from PyQt5.QtGui import QPixmap
# from pdf2image import convert_from_path
from PyQt5 import uic
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSize, QParallelAnimationGroup, QTimer
from PyQt5.QtWidgets import *


class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()
        uic.loadUi('main_window.ui', self)

        self.pushButton.clicked.connect(self.show_window_2)

    def show_window_2(self):
        self.close()
        self.w2 = Window2()
        self.w2.show()


class Window2(QWidget):

    def __init__(self):
        self.count = 0

        super(Window2, self).__init__()

        uic.loadUi('tamplate.ui', self)
        self.pushButton.clicked.connect(self.show_window_3)
        self.objs = QFrame.findChildren(self.frame, QLabel)

        self.right_btn.clicked.connect(self.resize_anim)
        self.left_btn.clicked.connect(self.resize_anim2)

    def show_window_3(self):

        self.close()
        self.w3 = Window3()
        self.w3.show()

    def resize_anim(self):
        self.count = 0
        self.anim_group = QParallelAnimationGroup()
        self.sizes = []
        for i in self.objs:
            self.sizes.append([i.width(), i.height(), i.x(), i.y()])
        self.sizes = self.sizes[1:] + [self.sizes[0]]

        for i in self.objs:
            print(self.count)
            self.anim = QPropertyAnimation(i, b"size")

            self.anim.setEndValue(QSize(*self.sizes[self.count][:2]))
            self.anim.setDuration(1000)
            self.anim2 = QPropertyAnimation(i, b"pos")
            self.anim2.setEndValue(QPoint(*self.sizes[self.count][2:]))
            self.anim2.setDuration(1000)
            self.anim_group.addAnimation(self.anim)
            self.anim_group.addAnimation(self.anim2)
            self.count += 1
        self.anim_group.start()
        self.right_btn.setDisabled(True)
        self.left_btn.setDisabled(True)
        QTimer.singleShot(self.anim_group.duration(), self.on_close)

    def resize_anim2(self):
        self.count = 0
        self.anim_group = QParallelAnimationGroup()
        self.sizes = []
        for i in self.objs:
            self.sizes.append([i.width(), i.height(), i.x(), i.y()])

        for i in self.objs:
            print(self.count)
            self.anim = QPropertyAnimation(i, b"size")
            self.anim.setEndValue(QSize(*self.sizes[self.count - 1][:2]))
            self.anim.setDuration(1000)
            self.anim2 = QPropertyAnimation(i, b"pos")
            self.anim2.setEndValue(QPoint(*self.sizes[self.count - 1][2:]))
            self.anim2.setDuration(1000)
            self.anim_group.addAnimation(self.anim)
            self.anim_group.addAnimation(self.anim2)
            self.count += 1
        self.anim_group.start()
        self.right_btn.setDisabled(True)
        self.left_btn.setDisabled(True)
        QTimer.singleShot(self.anim_group.duration(), self.on_close)

    def on_close(self):
        self.left_btn.setDisabled(False)
        self.right_btn.setDisabled(False)

    def get_id(self):

        self.objs = QFrame.findChildren(self.frame, QLabel)
        self.biggest = self.objs[0]
        for i in self.objs:
            if i.width() > self.biggest.width():
                self.biggest = i
        return self.biggest.objectName()


class Window3(QWidget):
    # def PPTtoPDF(self, inputFileName, outputFileName, formatType=32):
    # powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    # powerpoint.Visible = 1

    # if outputFileName[-3:] != 'pdf':
    # outputFileName = outputFileName + ".pdf"
    # deck = powerpoint.Presentations.Open(inputFileName)
    # deck.SaveAs(outputFileName, formatType)
    # deck.Close()
    # powerpoint.Quit()

    def __init__(self):
        print(Window2().get_id())
        super(Window3, self).__init__()
        uic.loadUi('total.ui', self)
        pixmap = QPixmap(f'3x/{Window2().get_id()}.png')
        self.label_2.setPixmap(pixmap)
        print(f'templates/{Window2().get_id()}.pptx')
        # self.PPTtoPDF(f'{Window2().get_id()}.pptx', f'{Window2().get_id()}')


class Con_checker():
    def check(self):
        print('OK')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main_window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())