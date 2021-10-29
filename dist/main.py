import sys
import time

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


class Window3(QWidget):

    def __init__(self):
        super(Window3, self).__init__()
        uic.loadUi('total.ui', self)


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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main_window()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
