"""Модуль размещения пользовательских декораторов"""
import socket

import sys
import logging

from functools import wraps

import logs.server_log_config

class Log:
    """Декоратор логирования"""

    def __init__(self):
        if sys.argv[0].find('servers.py') != -1:
            self.server_logger = logging.getLogger('servers')
        else:
            self.server_logger = logging.getLogger('client')

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            self.server_logger.debug(
                'Вызвана функция %s с параметрами %s, '
                '%s.Функция вызвана в функции'
                ' или молуле {inspect.stack(context=1)[1][3]}.',
                func.__name__, args, kwargs)
            res = func(*args, **kwargs)
            return res

        return decorated


def login_required(func):
    '''
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    '''

    def checker(*args, **kwargs):
        from server import Server
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], Server):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
