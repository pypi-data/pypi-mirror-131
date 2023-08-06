"""Модуль оброботки сообщений клиента"""
import json
import logging
import socket
import time
import threading
import hashlib
import hmac
import binascii
from PyQt5.QtCore import pyqtSignal, QObject

import logs.client_log_config
from common.errors import ServerError
from common.utils import get_data, send_data
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    PUBLIC_KEY, RESPONSE, ERROR, DATA, RESPONSE_511, MESSAGE, SENDER, \
    DESTINATION, MESSAGE_TEXT, GET_CONTACTS, LIST_INFO, USERS_REQUEST, \
    PUBLIC_KEY_REQUEST, ADD_CONTACT, REMOVE_CONTACT, EXIT

CLIENT_LOGGER = logging.getLogger('client')
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    """
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.database = database
        self.username = username
        self.password = passwd
        self.keys = keys
        self.transport = None
        self.connection_init(port, ip_address)
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            CLIENT_LOGGER.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
        self.running = True

    def connection_init(self, port, ip_addr):
        """
        Метод отвечающий за устанновку соединения с сервером
        """
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transport.settimeout(5)

        connected = False
        for i in range(5):
            CLIENT_LOGGER.info('Попытка подключения № %s', i + 1)
            try:
                self.transport.connect((ip_addr, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        if not connected:
            CLIENT_LOGGER.critical(
                'Не удалось установить соединение с сервером')
            raise ServerError('Не удалось установить соединение с сервером')

        CLIENT_LOGGER.debug('Установлено соединение с сервером')

        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        CLIENT_LOGGER.debug('Passwd hash_val ready: %s', passwd_hash_string)
        pubkey = self.keys.publickey().exportKey().decode('ascii')

        with socket_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            CLIENT_LOGGER.debug("Presense message = %s", presense)

            try:
                send_data(self.transport, presense)
                ans = get_data(self.transport)
                CLIENT_LOGGER.debug('Server response = %s.', ans)
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ServerError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        ans_data = ans[DATA]
                        hash_val = hmac.new(
                            passwd_hash_string, ans_data.encode('utf-8'),
                            'MD5')
                        digest = hash_val.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_data(self.transport, my_ans)
                        self.process_server_ans(get_data(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                CLIENT_LOGGER.debug('Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    def process_server_ans(self, message):
        """
        Метод обработчик поступающих сообщений с сервера
        """
        CLIENT_LOGGER.debug('Разбор сообщения от сервера: %s', message)

        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                CLIENT_LOGGER.debug(
                    'Принят неизвестный код подтверждения %s',
                    message[RESPONSE])

        elif ACTION in message and message[
            ACTION] == MESSAGE and SENDER in message and \
                DESTINATION in message and MESSAGE_TEXT in message and message[
            DESTINATION] == self.username:
            CLIENT_LOGGER.debug(
                'Получено сообщение от пользователя %s: %s', message[SENDER],
                message[MESSAGE_TEXT])
            self.new_message.emit(message)

    def contacts_list_update(self):
        """
        Метод обновления списка контактов
        """
        CLIENT_LOGGER.debug(
            'Запрос контакт листа для пользователся %s', self.name)
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        CLIENT_LOGGER.debug('Сформирован запрос %s', req)
        with socket_lock:
            send_data(self.transport, req)
            ans = get_data(self.transport)
        CLIENT_LOGGER.debug('Получен ответ %s', ans)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            CLIENT_LOGGER.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        """
        Метод обновления списка пользователей
        """
        CLIENT_LOGGER.debug(
            'Запрос списка известных пользователей %s', self.username)
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            send_data(self.transport, req)
            ans = get_data(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            CLIENT_LOGGER.error(
                'Не удалось обновить список известных пользователей.')

    def key_request(self, user):
        '''Метод запрашивающий с сервера публичный ключ пользователя.'''
        CLIENT_LOGGER.debug('Запрос публичного ключа для %s', user)
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with socket_lock:
            send_data(self.transport, req)
            ans = get_data(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            CLIENT_LOGGER.error('Не удалось получить ключ собеседника %s.',
                                user)

    def add_contact(self, contact):
        """
        Метод отправляющий на сервер сведения о добавлении контакта
        """
        CLIENT_LOGGER.debug('Создание контакта %s', contact)
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_data(self.transport, req)
            self.process_server_ans(get_data(self.transport))

    def remove_contact(self, contact):
        """
        Метод удаления контакта
        """
        CLIENT_LOGGER.debug('Удаление контакта %s', contact)
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_data(self.transport, req)
            self.process_server_ans(get_data(self.transport))

    def transport_shutdown(self):
        """
        Метод уведомляющий сервер о завершении работы клиента.
        """
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_data(self.transport, message)
            except OSError:
                pass
        CLIENT_LOGGER.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, to_user, message):
        """
        Метод отправляющий на сервер сообщения для пользователя
        """
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to_user,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug('Сформирован словарь сообщения: %s', message_dict)

        with socket_lock:
            send_data(self.transport, message_dict)
            self.process_server_ans(get_data(self.transport))
            CLIENT_LOGGER.info('Отправлено сообщение для пользователя %s',
                               to_user)

    def run(self):
        CLIENT_LOGGER.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_data(self.transport)
                except OSError as err:
                    if err.errno:
                        CLIENT_LOGGER.critical(
                            'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (
                        ConnectionError, ConnectionAbortedError,
                        ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    CLIENT_LOGGER.debug('Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.transport.settimeout(5)

            if message:
                CLIENT_LOGGER.debug('Принято сообщение с сервера: %s', message)
                self.process_server_ans(message)
