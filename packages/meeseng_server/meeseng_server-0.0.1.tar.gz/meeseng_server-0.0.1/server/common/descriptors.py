"""Модуль дескрипторов, проверка pi, порта, имени клиента"""
import configparser
import logging
import os
import sys

import ipaddress
import logs.server_log_config
from common.decos import Log

config = configparser.ConfigParser()

if sys.argv[0].find('servers.py') != -1:
    logger = logging.getLogger('servers')
else:
    logger = logging.getLogger('client')

dir_path = os.getcwd()
config.read(f"{dir_path}/{'servers.ini'}")


class CheckPort:
    """Дескриптор проверки введенного порта"""

    def __set__(self, instance, value):
        logger.debug('Проверка введенного порта')
        try:
            if '-p' in value.argv:
                server_port = int(value.argv[value.argv.index('-p') + 1])
            else:
                server_port = int(config['SETTINGS']['Default_port'])
            if server_port < 1024 or server_port > 65535:
                raise ValueError
            logger.info('Порт сервера %s', server_port)
            instance.__dict__[self.server_port] = server_port
        except IndexError:
            logger.critical(
                'После параметра -\'p\' необходимо указать номер порта.')
            value.exit(1)
        except ValueError:
            logger.critical(
                'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
            value.exit(1)

    @Log()
    def __set_name__(self, owner, server_port):
        self.server_port = server_port


class CheckIP:
    """Дескриптор проверки введенного ip адресса"""

    def __set__(self, instance, value):
        logger.debug('Проверка введенного ip адреса')
        try:
            if '-a' in value.argv:
                server_ip_address = str(ipaddress.ip_address(
                    value.argv[value.argv.index('-a') + 1]))
            else:
                server_ip_address = config['SETTINGS']['Listen_Address']
            logger.info('IP адрес %s', server_ip_address)
            instance.__dict__[self.server_ip_address] = server_ip_address
        except IndexError:
            logger.critical(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            value.exit(1)
        except ValueError:
            logger.critical('неверный ip адрес')
            value.exit(1)

    @Log()
    def __set_name__(self, owner, server_ip_address):
        self.server_ip_address = server_ip_address


class CheckName:
    """Дескриптор проверки введенного имени пользователя"""

    def __set__(self, instance, value):
        logger.debug('Проверка введенного имени клиента')
        try:
            if not hasattr(value, 'argv'):
                instance.__dict__[self.client_name] = value
            elif '-n' in value.argv:
                client_name = value.argv[value.argv.index('-n') + 1]
                logger.info('Имя клиента %s', client_name)
                instance.__dict__[self.client_name] = client_name
            else:
                instance.__dict__[self.client_name] = None
        except IndexError:
            logger.critical('После параметра \'n\'- необходимо указать имя.')
            value.exit(1)

    @Log()
    def __set_name__(self, owner, client_name):
        self.client_name = client_name
