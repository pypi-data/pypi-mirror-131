"""Constants"""
import logging

# Порт поумолчанию для сетевого ваимодействия
DEFAULT_ETHERNET_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 10240
# Кодировка проекта
ENCODING = 'utf-8'
SERVER_DATABASE = 'sqlite:///server_base.db3'

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMATTER = '%(asctime)s %(levelname)-10s %(filename) -25s %(message)s'
LOGGING_FOLDER = 'data'
LOGGING_CLIENT_NAME = 'client.log'
LOGGING_SERVER_NAME = 'servers.log'

# JIM protocol main keys:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'
ALL = 'all'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_202 = {RESPONSE: 202,
                LIST_INFO: None
                }
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
RESPONSE_205 = {
    RESPONSE: 205
}
RESPONSE_511 = {
    RESPONSE: 511,
    DATA: None
}
