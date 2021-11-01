import sys

import comtypes.client
from PyQt5.QtGui import QPixmap

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSize, QParallelAnimationGroup, QTimer
from PyQt5.QtWidgets import *
import os


class File_viewer():
    def count_temp(self, path, extension):
        list_dir = os.listdir(path)
        file_count = 0
        for file in list_dir:
            if file.endswith(extension):
                file_count += 1
        return file_count

    def PPTtoPDF(self, inputFileName, outputFileName, formatType=32):
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        if outputFileName[-3:] != 'pdf':
            outputFileName = outputFileName + ".pdf"
        deck = powerpoint.Presentations.Open(inputFileName)
        deck.SaveAs(outputFileName, formatType)
        deck.Close()
        powerpoint.Quit()


# print(File_viewer.count_temp(File_viewer, 'templates/', 'pptx'))


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
        # self.objs = QFrame.findChildren(self.frame, QLabel)
        self.main_layout = QGridLayout(self.widget)
        self.main_layout.setGeometry(QtCore.QRect(50, 210, 839, 201))
        min_unactive_size = [210, 110]
        min_active_size = [240, 140]
        first_pos = [60, 50]
        sizes_and_pos = []
        b_count = File_viewer.count_temp(File_viewer, 'templates/', 'pptx')
        print(3 // b_count)
        for i in range(1, b_count + 1):
            if round(b_count / 2) == i:
                first_pos[1] -= int(min_active_size[1] * (3 / b_count)) // 8
                sizes_and_pos.append(
                    [*first_pos, int(min_active_size[0] * (3 / b_count)), int(min_active_size[1] * (3 / b_count))])
                first_pos[1] = 50
                first_pos[0] += int(min_active_size[0] * (3 / b_count)) + int(30 * (3 / b_count))
            else:
                sizes_and_pos.append(
                    [*first_pos, int(min_unactive_size[0] * (3 / b_count)), int(min_unactive_size[1] * (3 / b_count))])
                first_pos[0] += int(min_unactive_size[0] * (3 / b_count)) + int(30 * (3 / b_count))

            self.p2 = QLabel(self.frame)
            self.p2.setText(str(i))
            self.p2.setGeometry(QtCore.QRect(*sizes_and_pos[i - 1]))
            self.p2.setAutoFillBackground(True)
            print(f'p{i}.pptx')
            File_viewer.PPTtoPDF(File_viewer, 'p2.pptx', f'p1')

        self.right_btn.clicked.connect(self.resize_anim)
        self.left_btn.clicked.connect(self.resize_anim2)

    def show_window_3(self):

        self.close()
        self.w3 = Window3()
        self.w3.show()

    def resize_anim(self):

        for i in self.objs:
            self.main_layout.addWidget(i)
        self.count = 0
        self.anim_group = QParallelAnimationGroup()
        self.sizes = []
        for i in self.objs:
            self.sizes.append([i.width(), i.height(), i.x(), i.y()])
        self.sizes = self.sizes[1:] + [self.sizes[0]]

        for i in self.objs:
            print(self.objs)
            widgets = self.main_layout.layout().count()
            if widgets > 1:
                for g in range(widgets):
                    widget = self.main_layout.layout().itemAt(0).widget()
                    self.main_layout.layout().removeWidget(widget)
                    widget = self.frame.layout().itemAt(0).widget()
                    self.frame.layout().removeWidget(widget)

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
        print(self.objs)
        self.biggest = self.objs[1]
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
