import argparse
import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
import logging
from ClientAPP.common.decorators import logger
from ClientAPP.common.variables import DEF_IP, DEF_PORT
from ClientAPP.client.main_client_gui import ClientMainWindow
from ClientAPP.client.uname_dialog import UserNameDialog
from ClientAPP.client.exchange_proto import ClientExchange
from ClientAPP.client.client_storage import ClientDB
from Cryptodome.PublicKey import RSA

LOG = logging.getLogger('client')


@logger
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEF_IP, nargs='?')
    parser.add_argument('port', default=DEF_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    arguments = parser.parse_args(sys.argv[1:])
    server_address = arguments.addr
    server_port = arguments.port
    client_name = arguments.name
    client_passwd = arguments.password
    if not 1023 < server_port < 65536:
        LOG.critical(f'Port not valid: {server_port}. Valid values: 1024 - 65535.')
        sys.exit(1)
    return server_address, server_port, client_name, client_passwd


def start_client():
    bind_ip, bind_port, client_name, client_passwd = arg_parser()
    client_app = QApplication(sys.argv)
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            LOG.debug(f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)
    LOG.info(f'Starting client with username: {client_name}. Connecting to server {bind_ip}:{bind_port}')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, 'keys', f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())
    LOG.debug("Keys successfully loaded.")

    database = ClientDB(client_name)
    try:
        exchange = ClientExchange(bind_port, bind_ip, database, client_name, client_passwd, keys)
    except (OSError, ValueError) as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Server error', error.text)
        exit(1)
    exchange.setDaemon(True)
    exchange.start()
    del start_dialog

    main_window = ClientMainWindow(database, exchange,  keys)
    main_window.make_connection(exchange)
    main_window.setWindowTitle(f'Python-messenger. Client - {client_name}')
    client_app.exec_()
    exchange.exchange_stop()
    exchange.join()


if __name__ == '__main__':
    start_client()

