"""Модуль содержит класс реализации стартовог окна пользователя"""
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, qApp


class UserNameDialog(QDialog):
    """
    Класс - стартовое окно с запросом логина и пароля
    """

    def __init__(self):
        super().__init__()
        self.success_event = False

        self.setWindowTitle('Hello!')
        self.setFixedSize(175, 143)

        self.label = QLabel('Enter name:', self)
        self.label.move(15, 10)
        self.label.setFixedSize(150, 15)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.label = QLabel('Enter password:', self)
        self.label.move(15, 55)
        self.label.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)

        self.btn_ok = QPushButton('Start', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Exit', self)
        self.btn_cancel.move(90, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    def click(self):
        """
        Метод обработки кнопки ОК
        """
        if self.client_name.text() and self.client_passwd.text():
            self.success_event = True
            qApp.exit()
