"""Клиентское приложение"""
import logging
import os
import sys

from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

import logs.client_log_config
from client.client_database import ClientDataBase
from client.main_windows import ClientMainWindow
from client.transport import ClientTransport
from client.start_dialog import UserNameDialog
from common.utils import get_port_server, get_ip_server, get_client_name, \
    get_client_password
from common.errors import ServerError

CLIENT_LOGGER = logging.getLogger('client')

if __name__ == '__main__':
    server_address = get_ip_server(CLIENT_LOGGER)
    server_port = get_port_server(CLIENT_LOGGER)
    client_name = get_client_name(CLIENT_LOGGER)
    client_passwd = get_client_password(CLIENT_LOGGER)

    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dialog.success_event:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            CLIENT_LOGGER.debug(
                'Using USERNAME = %s, PASSWD = %s.', client_name,
                client_passwd)
        else:
            sys.exit(0)

    CLIENT_LOGGER.info(
        'Запущен клиент с парамертами: адрес сервера: %s ,\
         порт: {server_port}, имя пользователя: %s',
        server_address, client_name)

    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    CLIENT_LOGGER.debug('Keys sucsessfully loaded.')

    database = ClientDataBase(client_name)
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        CLIENT_LOGGER.debug('Transport ready.')
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()
    del start_dialog

    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
