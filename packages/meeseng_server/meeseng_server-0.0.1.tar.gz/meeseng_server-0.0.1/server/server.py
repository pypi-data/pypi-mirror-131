"""Серверное приложение чата"""
import os
import socket
import logging
import sys
import threading
from binascii import hexlify, a2b_base64
from configparser import ConfigParser
from hmac import new, compare_digest
from os import urandom, path
from select import select

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import logs.server_log_config
from common.decos import Log, login_required
from common.variables import ACTION, ACCOUNT_NAME, MAX_CONNECTIONS, PRESENCE, \
    TIME, USER, ERROR, MESSAGE, \
    MESSAGE_TEXT, SENDER, EXIT, DESTINATION, ALL, RESPONSE_202, LIST_INFO, \
    ADD_CONTACT, GET_CONTACTS, RESPONSE_200, \
    REMOVE_CONTACT, USERS_REQUEST, RESPONSE_400, PUBLIC_KEY_REQUEST, \
    RESPONSE_511, DATA, PUBLIC_KEY, RESPONSE, \
    RESPONSE_205
from common.utils import get_data, send_data
from common.descriptors import CheckPort, CheckIP
from common.metaclasses import ServerVerifier
from servers.database import ServerStorage
from servers.server_gui import MainWindow

SERVER_LOGGER = logging.getLogger('servers')
conflag_lock = threading.Lock()
NEW_CONNECTION = False


class Server(threading.Thread, metaclass=ServerVerifier):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    server_port = CheckPort()
    ip_address = CheckIP()

    def __init__(self, argv, database):
        self.ip_address = argv
        self.server_port = argv
        self.clients = []
        self.messages = []
        self.names = {}
        self.database = database
        self.running = True
        self.listen_sockets = None
        self.error_sockets = None
        self.sock = None
        super().__init__()

    def socket_init(self):
        """Метод инициализатор сокета"""
        SERVER_LOGGER.info(
            'Запущен сервер, порт для подключений: %s , '
            'адрес с которого принимаются подключения: %s. '
            'Если адрес не указан, принимаются соединения с любых адресов.',
            self.server_port,
            self.ip_address)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.ip_address, self.server_port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        """
        SERVER_LOGGER.info(
            'Клиент %s отключился от сервера.', client.getpeername())
        for name in self.names.items():
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def service_update_lists(self):
        """Метод реализующий отправки сервисного сообщения 205 клиентам."""

        for client in self.names.items():
            try:
                send_data(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])

    @Log()
    def run(self):
        self.socket_init()
        SERVER_LOGGER.info(
            'Запущен сервер с параметрами %s: %s',
            self.ip_address,
            self.server_port)

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.debug(
                    'Установлено соедение с ПК %s', client_address)
                client.settimeout(5)
                self.clients.append(client)

            read_data_lst = []

            try:
                if self.clients:
                    read_data_lst, self.listen_sockets, error_sockets = select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                SERVER_LOGGER.error('Ошибка работы с сокетами: %s', err.errno)

            if read_data_lst:
                for client_msg in read_data_lst:
                    try:
                        self.check_client_message(
                            get_data(client_msg), client_msg)
                    except BaseException:
                        SERVER_LOGGER.info(
                            'Клиент %s отключился.', client_msg.getpeername())
                        self.clients.remove(client_msg)

            for i in self.messages:
                try:
                    SERVER_LOGGER.debug('Sending messages')
                    self.sending_message(i, self.names, self.listen_sockets)
                except BaseException:
                    if not i[DESTINATION] == ALL:
                        SERVER_LOGGER.info(
                            'Связь с клиентом с именем %s была потеряна',
                            i[DESTINATION])
                        self.clients.remove(self.names[i[DESTINATION]])
                        del self.names[i[DESTINATION]]
            self.messages.clear()

    @login_required
    def check_client_message(self, message, client):
        """
        Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клинта, проверяет корректность,
        возвращает словарь-ответ для клиента

        :param message:
        :param client:
        :return:
        """
        SERVER_LOGGER.debug('Разбор сообщения от клиента : %s', message)
        if ACTION in message and message[
                ACTION] == PRESENCE and TIME in message and USER in message:
            self.autorize_user(message, client)

        elif ACTION in message and message[
            ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and \
                self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.process_message(
                    message[SENDER], message[DESTINATION])
                self.sending_message(message, self.names, self.listen_sockets)
                try:
                    send_data(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_data(client, response)
                except OSError:
                    pass
            return

        elif ACTION in message and message[
            ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        elif ACTION in message and message[
            ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_data(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[
            ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_data(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[
            ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_data(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[
            ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            try:
                send_data(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[
                ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            if response[DATA]:
                try:
                    send_data(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[
                    ERROR] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_data(client, response)
                except OSError:
                    self.remove_client(client)

        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_data(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        """Метод реализующий авторизцию пользователей."""

        SERVER_LOGGER.debug('Start auth process for %s', message[USER])
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            try:
                SERVER_LOGGER.debug('Username busy, sending %s', response)
                send_data(sock, response)
            except OSError:
                SERVER_LOGGER.debug('OS Error')
            self.clients.remove(sock)
            sock.close()
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                SERVER_LOGGER.debug('Unknown username, sending %s', response)
                send_data(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            SERVER_LOGGER.debug('Correct username, starting passwd check.')
            message_auth = RESPONSE_511
            random_str = hexlify(urandom(64))
            message_auth[DATA] = random_str.decode('ascii')
            hash_val = new(
                self.database.get_hash(
                    message[USER][ACCOUNT_NAME]),
                random_str,
                'MD5')
            digest = hash_val.digest()
            SERVER_LOGGER.debug('Auth message = %s', message_auth)
            try:
                send_data(sock, message_auth)
                ans = get_data(sock)
            except OSError as err:
                SERVER_LOGGER.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = a2b_base64(ans[DATA])
            if RESPONSE in ans and ans[RESPONSE] == 511 and compare_digest(
                    digest, client_digest):

                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_data(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                self.database.user_login(
                    message[USER][ACCOUNT_NAME],
                    client_ip,
                    client_port,
                    message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'
                try:
                    send_data(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    @Log()
    def sending_message(self, message, names, listen_socks):
        """
        Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
        список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
        :param message:
        :param names:
        :param listen_socks:
        :return:
        """
        if message[DESTINATION] in names and names[message[DESTINATION]
                                                   ] in listen_socks:
            send_data(names[message[DESTINATION]], message)
            SERVER_LOGGER.info(
                'Отправлено сообщение пользователю %s '
                'от пользователя %s.', message[DESTINATION], message[SENDER])
        elif message[DESTINATION] == ALL:
            for name in names:
                message[DESTINATION] = name
                send_data(names[name], message)
            SERVER_LOGGER.info(
                'Отправлено сообщение всем от пользователя %s.',
                message[SENDER])
        elif message[DESTINATION] in names and names[
                message[DESTINATION]] not in listen_socks:
            self.remove_client(names[message[DESTINATION]])
            SERVER_LOGGER.error(
                'Связь с клиентом %s была потеряна. Соединение закрыто, доставка невозможна.',
                message[DESTINATION])
        else:
            SERVER_LOGGER.error(
                'Пользователь %s не зарегистрирован на сервере, отправка сообщения невозможна.',
                message[DESTINATION])


@Log()
def main():
    """Основная функция"""
    config = ConfigParser()

    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'servers.ini'}")
    database = ServerStorage(
        path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    server_messenger = Server(sys, database)
    server_messenger.daemon = True
    server_messenger.start()

    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(database, server_messenger, config)
    server_app.exec_()
    server_messenger.running = False


if __name__ == '__main__':
    main()
