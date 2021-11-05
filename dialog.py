from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
import variables


class CustomDialog(QDialog):
    def __init__(self, mess, title='Внимание', is_ok=True):
        super().__init__()

        self.setWindowTitle(title)

        self.layout = QVBoxLayout()
        message = QLabel(mess)

        self.layout.addWidget(message)

        self.setLayout(self.layout)
        if is_ok:
            QBtn = QDialogButtonBox.Ok

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)
            self.layout.addWidget(self.buttonBox)

        # message = QLabel(f'К сожалению нам не удалось найти "{variables.theme}"')


