"""Модуль конфигурирования логирования сервера"""
"""Модуль конфигурирования логирования сервера"""

import logging.handlers
import os.path
import sys

from common.variables import LOGGING_LEVEL, LOGGING_FORMATTER, LOGGING_FOLDER, LOGGING_SERVER_NAME

SERVER_FORMATTER = logging.Formatter(LOGGING_FORMATTER)

PATH = os.getcwd()
PATH = os.path.join(PATH, 'logs')
PATH = os.path.join(PATH, LOGGING_FOLDER)
PATH = os.path.join(PATH, LOGGING_SERVER_NAME)

CONSOLE_HANDLER = logging.StreamHandler(sys.stderr)
CONSOLE_HANDLER.setFormatter(SERVER_FORMATTER)
CONSOLE_HANDLER.setLevel(logging.ERROR)

FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf8', interval=1, when='D')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)

LOGGER = logging.getLogger('servers')
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Critical err')
    LOGGER.error('error')
    LOGGER.debug('debug message')
    LOGGER.info('info message')
