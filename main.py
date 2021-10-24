import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication




class PayForm(QWidget):
    def __init__(self):
        super(PayForm, self).__init__()
        uic.loadUi('main_window.ui', self)

     # обработка нажатия для октрытия 2 окна
        self.pushButton.clicked.connect(self.show_window_2)

    def show_window_2(self):  # открытие 2  окна
        self.w2 = Window2()
        self.w2.show()


class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        uic.loadUi('tamplate.ui', self)




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PayForm()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())