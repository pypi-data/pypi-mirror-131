"""Клиентское приложение"""
import argparse
import sys
import os
import logging
from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox
import logs.config_client_log
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS
from common.errors import ServerError
from common.decos import log
from client.client_database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

logger = logging.getLogger('client')


@log
def arg_parser():
    """
    Парсер аргументов командной строки.
    Выполняет проверку на корректность номера порта.
    :return:serv_address - адрес сервера, serv_port - порт сервера, cl_name - имя клиента, cl_passwd - пароль клиента
    """
    logger.debug(
        f'Инициализация парсера аргументов командной строки: {sys.argv}')
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port
    cl_name = namespace.name
    cl_passwd = namespace.password

    if not 1023 < serv_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {serv_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return serv_address, serv_port, cl_name, cl_passwd


if __name__ == '__main__':
    server_address, server_port, client_name, client_passwd = arg_parser()
    logger.debug('Аргументы загружены')

    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое и
        # удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            logger.debug(
                f'Используется Имя - {client_name}, пароль - {client_passwd}')
        else:
            sys.exit(0)

    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address},'
        f' порт: {server_port}, имя пользователя: {client_name}')

    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    logger.debug('Ключи успешно загружены')

    database = ClientDatabase(client_name)

    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
    except ServerError as err:
        message = QMessageBox()
        message.critical(start_dialog, 'ошибка сервера', err.text)
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
