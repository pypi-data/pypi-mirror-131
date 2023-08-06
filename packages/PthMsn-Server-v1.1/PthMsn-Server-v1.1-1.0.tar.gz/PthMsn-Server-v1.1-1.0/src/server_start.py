import argparse
import binascii
import configparser
import hmac
import json
import os
import select
import socket
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMessageBox
from ServerAPP.common.decorators import logger, login_required
from ServerAPP.common.variables import ACTION, ACCOUNT_NAME, PRESENCE, TIME, USER, ERROR, RESP_OK, \
    RESP_BAD, SENDER, DESTINATION, MESSAGE, MESSAGE_TEXT, EXIT, GET_FRIENDS, RESP_202, LIST_INFO, ADD_FRIEND, \
    REMOVE_FRIEND, USERS_REQUEST, RESP_511, PUBLIC_KEY_REQUEST, DATA, RESPONSE, PUBLIC_KEY, RESP_205
from ServerAPP.common.utils import get_message, send_message
import logging
from ServerAPP.server.descriptors import Port, Addr
from ServerAPP.common.metaclasses import ServerMetaVerify
from ServerAPP.server.server_gui import MainWindow, HistoryWindow, create_stat_model, ConfigWindow
from ServerAPP.server.server_storage import ServerDB

LOG = logging.getLogger('server')
new_connection = False
connectflag_lock = threading.Lock()


class Server(threading.Thread, metaclass=ServerMetaVerify):
    port = Port()
    addr = Addr()

    def __init__(self, listen_address, listen_port, database):
        self.database = database
        self.addr = listen_address
        self.port = listen_port
        self.clients = []
        self.messages_list = []
        self.listen_sockets = None
        self.names = dict()
        super().__init__()

    def init_socket(self):
        LOG.debug(f'Used interface: {self.addr}:{self.port}')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)
        self.sock = transport
        self.sock.listen()

    def run(self):
        self.init_socket()
        while True:
            try:
                client, client_ip = self.sock.accept()
            except OSError:
                pass
            else:
                LOG.debug(f'New client appended: {client}')
                client.settimeout(5)
                self.clients.append(client)
            receive_data_list = []
            try:
                if self.clients:
                    receive_data_list, self.listen_sockets, error_list = select.select(self.clients, self.clients, [],
                                                                                       0)
            except OSError:
                pass
            if receive_data_list:
                for client_messaging in receive_data_list:
                    try:
                        self.process_client_message(get_message(client_messaging), client_messaging)
                    except (OSError, json.JSONDecodeError, TypeError):
                        LOG.debug(f'Connection with client is closed: {client_messaging.getpeername()}')
                        self.clients.remove(client_messaging)

    def process_message(self, message):
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in self.listen_sockets:
            send_message(self.names[message[DESTINATION]], message)
            LOG.info(f'Message sent to {message[DESTINATION]} from  {message[SENDER]}.')
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in self.listen_sockets:
            raise ConnectionError
        else:
            LOG.error(f'USER {message[DESTINATION]} is unknown, message terminated.')

    @login_required
    def process_client_message(self, message, client):
        global new_connection
        LOG.debug(f'Message from client: {message}.')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            self.autorize_user(message, client)

        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.messages_list.append(message)
                self.database.process_message(message[SENDER], message[DESTINATION])
                self.process_message(message)
                try:
                    send_message(client, RESP_OK)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESP_BAD
                response[ERROR] = 'Unknown user.'
                try:
                    send_message(client, response)
                except OSError:
                    pass

        elif ACTION in message and message[ACTION] == GET_FRIENDS and USER in message and \
                self.names[message[USER]] == client:
            response = RESP_202
            response[LIST_INFO] = self.database.list_friends(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == ADD_FRIEND and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_friend_to_list(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESP_OK)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == REMOVE_FRIEND and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.del_friend_from_list(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, RESP_OK)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = RESP_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.database.user_logout(message[ACCOUNT_NAME])
            LOG.debug(f'User {message[ACCOUNT_NAME]} disconnected (going offline).')
            self.clients.remove(self.names[message[ACCOUNT_NAME]])
            self.names[message[ACCOUNT_NAME]].close()
            del self.names[message[ACCOUNT_NAME]]
            with connectflag_lock:
                new_connection = True

        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESP_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESP_BAD
                response[ERROR] = 'Error loading public key'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
        else:
            response = RESP_BAD
            response[ERROR] = 'BAD REQUEST.'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        LOG.debug(f'Start auth for {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = RESP_BAD
            response[ERROR] = 'Username is in use.'
            try:
                LOG.debug(f'Username is in use, sending {response}')
                send_message(sock, response)
            except OSError:
                LOG.debug('OS Error')
            self.clients.remove(sock)
            sock.close()
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = RESP_BAD
            response[ERROR] = 'User is not registered.'
            try:
                LOG.debug(f'Unknown username, sending {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            LOG.debug('Correct username, starting passwd check.')
            message_auth = RESP_511
            random_str = binascii.hexlify(os.urandom(64))
            message_auth[DATA] = random_str.decode('ascii')
            hash_data = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash_data.digest()
            LOG.debug(f'Auth message = {message_auth}')
            try:
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                LOG.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, RESP_OK)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port, message[USER][PUBLIC_KEY])
            else:
                response = RESP_BAD
                response[ERROR] = 'Bad password.'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        for client in self.names:
            try:
                send_message(self.names[client], RESP_205)
            except OSError:
                self.remove_client(self.names[client])

    def remove_client(self, client):
        LOG.info(f'User {client.getpeername()} logout.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()


@logger
def arg_parser(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('-a', default=default_address, nargs='?')
    arguments = parser.parse_args(sys.argv[1:])
    bind_ip = arguments.a
    bind_port = arguments.p
    return bind_ip, bind_port


@logger
def start_server():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server/server.conf'}")
    LOG.debug(f'Reading server config: {config}')
    bind_ip, bind_port = arg_parser(config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])
    database = ServerDB(os.path.join(config['SETTINGS']['Database_path'], config['SETTINGS']['Database_file']))
    server = Server(bind_ip, bind_port, database)
    server.daemon = True
    server.start()
    LOG.debug(f'Server started. IP: {bind_ip}  Port: {bind_port}')
    server_app = QApplication(sys.argv)
    main_window = MainWindow(database, server, config)
    main_window.statusBar().showMessage('Server Working')
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    def show_statistics():
        global stat_window
        stat_window = HistoryWindow()
        stat_window.history_table.setModel(create_stat_model(database))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    def server_config():
        global config_window
        config_window = ConfigWindow()
        config_window.db_path.insert(config['SETTINGS']['Database_path'])
        config_window.db_file.insert(config['SETTINGS']['Database_file'])
        config_window.port.insert(config['SETTINGS']['Default_port'])
        config_window.ip.insert(config['SETTINGS']['Listen_Address'])
        config_window.save_btn.clicked.connect(save_server_config)

    def save_server_config():
        global config_window
        message = QMessageBox()
        config['SETTINGS']['Database_path'] = config_window.db_path.text()
        config['SETTINGS']['Database_file'] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Error', 'Port must be integer')
        else:
            config['SETTINGS']['Listen_Address'] = config_window.ip.text()
            if 1023 < port < 65536:
                config['SETTINGS']['Default_port'] = str(port)
                print(port)
                with open('server/server.conf', 'w') as conf:
                    config.write(conf)
                    message.information(config_window, 'OK', 'Settings saved!')
                    LOG.debug(f'New server settings saved: {config}')
            else:
                message.warning(config_window, 'Error', 'Port must be in range from 1024 to 65536')

    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_btn.triggered.connect(server_config)
    server_app.exec_()


if __name__ == '__main__':
    start_server()
