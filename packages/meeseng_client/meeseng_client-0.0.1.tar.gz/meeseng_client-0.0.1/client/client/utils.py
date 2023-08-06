"""
Модуль содержащий классы диалогового окна
добовление контактов и удаление контактов
"""
import logging

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

import logs.client_log_config

CLIENT_LOGGER = logging.getLogger('client')


class DelContactDialog(QDialog):
    """
    Диалог удаления контакта. Прделагает текущий список контактов,
    не имеет обработчиков для действий
    """
    def __init__(self, database):
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Select contact fo delete:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Select contact fo delete:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Delete', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.selector.addItems(sorted(self.database.get_contacts()))


class AddContactDialog(QDialog):
    """
    Диалог добавления пользователя в список контактов.
    Предлагает пользователю список возможных контактов и
    добавляет выбранный в контакты.
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Select contact for add:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Select contact for add:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Update list', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Add', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)
        self.possible_contacts_update()

        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self):
        """
        Метод заполнения списка возможных контактов.
        Создаёт список всех зарегистрированных пользователей
        за исключением уже добавленных в контакты и самого себя
        """
        self.selector.clear()
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        """
        Метод обновления списка возможных контактов. Запрашивает с сервера
        список известных пользователей и обновляет содержимое окна
        """
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            CLIENT_LOGGER.debug('Updated list success')
            self.possible_contacts_update()
