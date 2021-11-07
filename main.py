import os

import db
import loading

os.system('pip install -r requirements/requirements.txt')
import math
import sys
import time
import os.path

import comtypes.client
from PyQt5.QtGui import QPixmap, QIcon

import dialog
import variables
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QPropertyAnimation, QPoint, QSize, QParallelAnimationGroup, QTimer
from PyQt5.QtWidgets import *

from PyQt5.uic.properties import QtGui

import generator


class File_viewer():
    def count_temp(self, path, extension):
        list_dir = os.listdir(path)
        file_count = 0
        for file in list_dir:
            if file.endswith(extension):
                file_count += 1
        return file_count

    def PPTtoPNG(self, inputFileName):

        from comtypes import client

        f = os.path.abspath(inputFileName)
        if not os.path.exists(f):
            print("No such file!")

        powerpoint = client.CreateObject('Powerpoint.Application')
        powerpoint.Presentations.Open(f)
        powerpoint.ActivePresentation.Export(f, 'png')
        powerpoint.ActivePresentation.Close()
        powerpoint.Quit()


# print(File_viewer.count_temp(File_viewer, 'templates/', 'pptx'))


class Tem_view(QWidget):

    def __init__(self):
        super(Tem_view, self).__init__()
        self.del_rows = 0
        uic.loadUi('temp.ui', self)
        for i in db.select_table('templates', 'direc', 'is_del'):
            if i != () and i[1] != 1:
                print(i)
                self.tm_view_widget.addItem(i[0])
        self.del_btn.clicked.connect(self.del_item)
        self.new_btn.clicked.connect(self.insert_new)

    def del_item(self):
        print(self.tm_view_widget.currentItem().text())
        db.update('templates', 'is_del', 1, 'id',
                  f'{self.tm_view_widget.row(self.tm_view_widget.currentItem()) + self.del_rows}')
        self.tm_view_widget.takeItem(self.tm_view_widget.row(self.tm_view_widget.currentItem()))
        self.del_rows += 1

    def insert_new(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите шаблон", "",
                                                   "PPTX(*.pptx)")

        if file_path == "":
            return

        db.insert('templates', 'direc', str(file_path))
        self.tm_view_widget.addItem(file_path)


class Main_window(QWidget):
    def __init__(self):
        super(Main_window, self).__init__()
        uic.loadUi('main_window.ui', self)
        self.setWindowTitle('Настройки')
        self.setWindowIcon(QIcon('ico/1.png'))
        self.progressBar.setVisible(False)
        self.pushButton.clicked.connect(self.show_window_2_4)
        self.menu.clicked.connect(self.show_menu)

    def show_window_2_4(self):

        variables.theme = self.theme_input.text()
        self.progressBar.setVisible(True)
        progress = 0
        self.b_count = 0
        templates = db.select_table('templates', 'direc', 'is_del')
        for i in templates:
            if i[1] != 1:
                self.b_count += 1
        print(self.b_count)

        for i in range(len(templates)):
            self.t_dir = templates[i][0].rpartition('/')[0] + '/' + \
                         templates[i][0].rpartition('/')[-1].rpartition('.')[0]
            if not os.path.exists(self.t_dir):
                progress += int(100 / self.b_count)

                File_viewer.PPTtoPNG(File_viewer, templates[i][0])
                self.progressBar.setValue(progress)
                time.sleep(3)

        self.w2 = Window2()

        self.w2.show()
        self.close()

    def show_menu(self):
        self.menu_win = Menu()
        self.menu_win.show()


class Menu(QWidget):

    def __init__(self):
        self.count = 0

        super(Menu, self).__init__()

        uic.loadUi('menu.ui', self)
        self.spinBox.setMinimum(variables.max_slides)
        self.spinBox.valueChanged.connect(self.change_value)
        self.change_temp.clicked.connect(self.temp_view)

    def change_value(self):
        variables.max_slides = self.spinBox.value()
        self.spinBox.setMinimum(variables.max_slides)

    def temp_view(self):
        self.tw = Tem_view()
        self.tw.show()


class Window2(QWidget):

    def __init__(self):

        self.count = 0

        super(Window2, self).__init__()

        uic.loadUi('tamplate.ui', self)

        self.setWindowTitle('Выбор шаблонов')
        self.setWindowIcon(QIcon('ico/1.png'))
        self.pushButton.clicked.connect(self.show_window_3)
        # self.objs = QFrame.findChildren(self.frame, QLabel)

        min_unactive_size = [210, 110]
        min_active_size = [240, 140]
        first_pos = [60, 50]
        sizes_and_pos = []
        self.b_count = 0
        templates = db.select_table('templates', 'direc', 'is_del')
        self.active_temp = []
        self.used_temp = []
        for i in templates:
            self.t_dir1 = i[0].rpartition('/')[0] + '/' + \
                          i[0].rpartition('/')[-1].rpartition('.')[0]
            if i[1] != 1:
                self.b_count += 1
                self.active_temp.append(self.t_dir1)
                self.used_temp.append(i[0])
        for i in range(1, self.b_count + 1):

            if math.ceil(self.b_count / 2) == i:
                print(i, self.b_count, self.b_count / 2, round(self.b_count / 2))
                first_pos[1] -= int(min_active_size[1] * (3 / self.b_count)) // 8
                sizes_and_pos.append(
                    [*first_pos, int(min_active_size[0] * (3 / self.b_count)),
                     int(min_active_size[1] * (3 / self.b_count))])
                first_pos[1] = 50
                first_pos[0] += int(min_active_size[0] * (3 / self.b_count)) + int(30 * (3 / self.b_count))
            else:
                sizes_and_pos.append(
                    [*first_pos, int(min_unactive_size[0] * (3 / self.b_count)),
                     int(min_unactive_size[1] * (3 / self.b_count))])
                first_pos[0] += int(min_unactive_size[0] * (3 / self.b_count)) + int(30 * (3 / self.b_count))

            self.slide_preview = QLabel(self.frame)
            self.slide_preview.setObjectName(f"p{i}")
            self.slide_preview.setText(str(i))
            self.slide_preview.setGeometry(QtCore.QRect(*sizes_and_pos[i - 1]))
            self.slide_preview.setAutoFillBackground(True)
            self.t_dir = templates[i - 1][0].rpartition('/')[0] + '/' + \
                         templates[i - 1][0].rpartition('/')[-1].rpartition('.')[0]
            pixmap = QPixmap(f"{self.active_temp[i - 1]}/Слайд1.PNG")
            self.slide_preview.setPixmap(pixmap)
            self.slide_preview.setScaledContents(True)
            print(f'p{i}.pptx')
        variables.choosen = math.ceil(self.b_count / 2)
        self.right_btn.clicked.connect(self.resize_anim)
        self.left_btn.clicked.connect(self.resize_anim2)

    def show_window_3(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Выберите место для сохранения", "",
                                                   "PPTX(*.pptx);;All Files(*.*) ")

        if file_path == "":
            return

        self.close()

        dlg = dialog.CustomDialog('''Пожалуйста ожидайте, по готовности откроется меню предпросмотра(не забудьте нажать ok).
        Во время данного процесса не закрывайте окна PowerPoint.''')
        dlg.exec()

        generator.get_temp(self, self.used_temp[variables.choosen - 1], variables.theme, file_path)
        self.w3 = Window3()
        self.w3.show()

    def resize_anim(self):
        if variables.choosen - 1 != 0:
            variables.choosen -= 1
        else:
            variables.choosen = self.b_count
        print(variables.choosen)
        self.objs = QFrame.findChildren(self.frame, QLabel)

        self.count = 0
        self.anim_group = QParallelAnimationGroup()
        self.sizes = []
        for i in self.objs:
            self.sizes.append([i.width(), i.height(), i.x(), i.y()])
        self.sizes = self.sizes[1:] + [self.sizes[0]]

        for i in self.objs:
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

        if variables.choosen + 1 > self.b_count:
            variables.choosen = 1
        else:
            variables.choosen += 1
        print(variables.choosen)

        self.objs = QFrame.findChildren(self.frame, QLabel)

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


class Window3(QWidget):

    def __init__(self):
        super(Window3, self).__init__()

        uic.loadUi('total.ui', self)
        self.setWindowTitle('Предпросмотр')
        self.setWindowIcon(QIcon('ico/1.png'))
        File_viewer.PPTtoPNG(Window3, variables.total)
        self.direrct = variables.result_dir + '/' + variables.result_dir.rpartition('/')[-1]
        print(self.direrct)
        pixmap = QPixmap(self.direrct + '/' + 'Слайд1.PNG')
        self.label_2.setPixmap(pixmap)
        self.slide_number = 1
        self.right_btn.clicked.connect(self.right)
        self.left_btn.clicked.connect(self.left)
        self.s_count = File_viewer.count_temp(File_viewer, self.direrct + '/', 'PNG')

    def right(self):
        if self.slide_number + 1 > self.s_count:
            self.slide_number = 1
        else:
            self.slide_number += 1
        pixmap = QPixmap(self.direrct + '/' + f'Слайд{self.slide_number}.PNG')
        self.label_2.setPixmap(pixmap)

    def left(self):

        if self.slide_number - 1 <= 0:
            self.slide_number = self.s_count

        else:
            self.slide_number -= 1
        print(self.slide_number, self.s_count)

        pixmap = QPixmap(self.direrct + '/' + f'Слайд{self.slide_number}.PNG')
        self.label_2.setPixmap(pixmap)

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
