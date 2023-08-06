"""Модуль пользовательских меттаклассов"""

import dis


class ServerVerifier(type):
    """Метакласс, проверяющий что в результирующем классе нет клиентских
    вызовов таких как: connect. Также проверяется, что серверный
    сокет является TCP и работает по IPv4 протоколу."""

    def __init__(cls, clsname, bases, clsdict):

        method = []
        attrs = []
        for func in clsdict:
            try:
                result = dis.get_instructions(clsdict[func])
            except BaseException:
                pass
            else:
                for i in result:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in method:
                            method.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        if 'connect' in method:
            raise TypeError('Использование метода connect не допустимо')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Не коректная инициализация сркета')
        super().__init__(clsname, bases, clsdict)
