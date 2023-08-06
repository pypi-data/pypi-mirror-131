import binascii
import hashlib
import hmac
import json
import sys
import socket
import threading
import time
import logging
from PyQt5.QtCore import QObject, pyqtSignal

from ClientAPP.common.errors import ClientError

sys.path.append('../../')
from ClientAPP.common.decorators import logger
from ClientAPP.common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, RESP_OK, \
    RESP_BAD, EXIT, SENDER, DESTINATION, MESSAGE, MESSAGE_TEXT, GET_FRIENDS, LIST_INFO, REMOVE_FRIEND, ADD_FRIEND, \
    USERS_REQUEST, PUBLIC_KEY, RESP_511, DATA, ERROR, PUBLIC_KEY_REQUEST
from ClientAPP.common.utils import get_message, send_message

LOG = logging.getLogger('client')
sock_lock = threading.Lock()
CON_ERR = 'Connection to server lost.'


class ClientExchange(threading.Thread, QObject):
    """
    Exchange class. Responsible for interacting with the server.
    """
    new_message = pyqtSignal(dict)
    connection_lost = pyqtSignal()
    message_205 = pyqtSignal()

    def __init__(self, bind_port, bind_ip, database, username, passwd, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.database = database
        self.username = username
        self.keys = keys
        self.password = passwd
        self.exchange = None
        self.connection_init(bind_port, bind_ip)
        try:
            self.user_list_request()
            self.friends_list_request()
        except OSError as err:
            if err.errno:
                LOG.error(CON_ERR)
                raise ClientError(CON_ERR)
            LOG.error('Timeout connection.')
        except json.JSONDecodeError:
            LOG.error(CON_ERR)
            raise ClientError(CON_ERR)
        self.running = True

    def connection_init(self, bind_port, bind_ip):
        """
        Establishing connection to server method.
        :param bind_port:
        :param bind_ip:
        :return:
        """
        self.exchange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.exchange.settimeout(5)
        connected = False
        for i in range(5):
            LOG.debug(f'Trying connect to server. Try {i + 1}.')
            try:
                self.exchange.connect((bind_ip, bind_port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)
        if not connected:
            LOG.error('Cannot connect to te server.')
            raise ClientError('Cannot connect to te server.')
        LOG.debug('Connection established. Authentication.')

        b_pass = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        hash_pass = hashlib.pbkdf2_hmac('sha512', b_pass, salt, 10000)
        str_hash_pass = binascii.hexlify(hash_pass)
        LOG.debug(f'Password hash: {str_hash_pass}')
        pubkey = self.keys.publickey().export_key().decode('ascii')

        with sock_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            try:
                send_message(self.exchange, presense)
                ans = get_message(self.exchange)
                LOG.debug(f'Server response = {ans}.')
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ClientError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        ans_data = ans[DATA]
                        hash_data = hmac.new(str_hash_pass, ans_data.encode('utf-8'), 'MD5')
                        digest = hash_data.digest()
                        my_ans = RESP_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.exchange, my_ans)
                        self.process_answer(get_message(self.exchange))
            except (OSError, json.JSONDecodeError) as err:
                LOG.debug(f'Connection error.', exc_info=err)
                raise ClientError('Connection error.')

    def process_answer(self, message):
        """
        Processing server response method.
        :param message:
        :return:
        """
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                LOG.debug('Server return OK for PRESENCE message')
                return RESP_OK
            elif message[RESPONSE] == 400:
                LOG.error('Server return BAD for PRESENCE message')
                return RESP_BAD
            elif message[RESPONSE] == 205:
                self.user_list_request()
                self.friends_list_request()
                self.message_205.emit()
            else:
                LOG.error('ValueError in server response.')

        elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
            LOG.info(f'Message from user {message[SENDER]}: {message[MESSAGE_TEXT]}')
            self.new_message.emit(message)

    @logger
    def create_presence(self):
        """
        Method to create presence (initial) message for server.
        :return:
        """
        out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: self.username}}
        LOG.debug(f'Presence created from {self.username}.')
        return out

    @logger
    def friends_list_request(self):
        """
        Get friends list from server method.
        :return:
        """
        LOG.debug(f'Friends list request for {self.username}')
        req = {ACTION: GET_FRIENDS, TIME: time.time(), USER: self.username}
        with sock_lock:
            send_message(self.exchange, req)
            answer = get_message(self.exchange)
        LOG.debug(f'Response friends list:  {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            for friend in answer[LIST_INFO]:
                self.database.add_friend_to_list(friend)
        else:
            raise ClientError('Bad response!')

    @logger
    def user_list_request(self):
        """
        Get all users list from server method.
        :return:
        """
        LOG.debug(f'Request all users list {self.username}')
        req = {ACTION: USERS_REQUEST, TIME: time.time(), ACCOUNT_NAME: self.username}
        with sock_lock:
            send_message(self.exchange, req)
            answer = get_message(self.exchange)
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.database.add_all_users(answer[LIST_INFO])
        else:
            raise ClientError('Error while request all users list!')

    def key_request(self, user):
        """
        Public key request method.
        :param user:
        :return:
        """
        LOG.debug(f'Publik key request for user {user}')
        req = {ACTION: PUBLIC_KEY_REQUEST, TIME: time.time(), ACCOUNT_NAME: user}
        with sock_lock:
            send_message(self.exchange, req)
            ans = get_message(self.exchange)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            LOG.error(f'Error while requesting pubkey for user {user}.')

    @logger
    def add_friend(self, friend):
        """
        Add user to friends list request method.
        :param friend:
        :return:
        """
        LOG.debug(f'Adding user to friends list {friend}')
        req = {ACTION: ADD_FRIEND, TIME: time.time(), USER: self.username, ACCOUNT_NAME: friend}
        with sock_lock:
            send_message(self.exchange, req)
            self.process_answer(get_message(self.exchange))

    @logger
    def remove_friend(self, friend):
        """
        Remove user from friends list request method.
        :param friend:
        :return:
        """
        LOG.debug(f'Remove friend {friend} from list.')
        req = {ACTION: REMOVE_FRIEND, TIME: time.time(), USER: self.username, ACCOUNT_NAME: friend}
        with sock_lock:
            send_message(self.exchange, req)
            self.process_answer(get_message(self.exchange))

    @logger
    def exchange_stop(self):
        """
        Stopping exchange with server method.
        :return:
        """
        self.running = False
        message = {ACTION: EXIT, TIME: time.time(), ACCOUNT_NAME: self.username}
        with sock_lock:
            try:
                send_message(self.exchange, message)
            except OSError:
                pass
        LOG.debug('Exchange is stopping.')
        time.sleep(0.5)

    @logger
    def send_message(self, dest, message):
        """
        Send message to server method.
        :param dest:
        :param message:
        :return:
        """
        message_dict = {ACTION: MESSAGE, SENDER: self.username, DESTINATION: dest, TIME: time.time(),
                        MESSAGE_TEXT: message}
        LOG.debug(f'Created message dict: {message_dict}')
        with sock_lock:
            send_message(self.exchange, message_dict)
            self.process_answer(get_message(self.exchange))
            LOG.debug(f'Message was sent to {dest}.')

    def run(self):
        """
        Starting exchange with server method.
        :return:
        """
        while self.running:
            time.sleep(1)
            message = None
            with sock_lock:
                try:
                    self.exchange.settimeout(0.5)
                    message = get_message(self.exchange)
                except OSError as err:
                    if err.errno:
                        LOG.error('Lost connection to server.')
                        self.running = False
                        self.connection_lost.emit()
                except (json.JSONDecodeError, TypeError):
                    LOG.error('Lost connection to server.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.exchange.settimeout(5)
            if message:
                LOG.debug(f'Message from server: {message}')
                self.process_answer(message)
