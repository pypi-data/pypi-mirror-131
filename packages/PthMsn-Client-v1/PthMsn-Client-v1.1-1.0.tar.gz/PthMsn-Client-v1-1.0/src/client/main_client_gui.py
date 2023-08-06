from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, Qt
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import base64
import sys
import json
import logging

from ServerAPP.common.variables import MESSAGE_TEXT, SENDER

sys.path.append('../../')

from ClientAPP.client.main_client_gui_conv import Ui_MainClientWindow
from ClientAPP.client.add_friend import AddContactDialog
from ClientAPP.client.del_friend import DelContactDialog

LOG = logging.getLogger('client')
CON_ERR = 'Lost connection!'
TIME_ERR = 'Timeout!'


class ClientMainWindow(QMainWindow):
    """
    Main user GUI class.
    Contains all the main logic of the client module.
    Window configuration created in QTDesigner and loaded from
    converted file main_client_gui_conv.py
    """
    def __init__(self, database, transport, keys):
        super().__init__()
        self.database = database
        self.transport = transport
        self.decrypter = PKCS1_OAEP.new(keys)
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)
        self.ui.menu_exit.triggered.connect(qApp.exit)
        self.ui.btn_send.clicked.connect(self.send_message)
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)
        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """
        Deactivating fields method.
        :return:
        """
        self.ui.label_new_message.setText('Double click to choose destination user.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()
        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)
        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_list_update(self):
        """
        Fill history messaging method.
        :return:
        """
        dataset = sorted(self.database.get_history(self.current_chat), key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()
        length = len(dataset)
        start_index = 0
        if length > 20:
            start_index = length - 20
        for i in range(start_index, length):
            item = dataset[i]
            if item[1] == 'in':
                mess = QStandardItem(f'Incoming from {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(f'Outgoing to {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """
        Double click event in friends list.
        :return:
        """
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """
        Activate chat with friend method.
        :return:
        """
        try:
            self.current_chat_key = self.transport.key_request(
                self.current_chat)
            LOG.debug(f'Loaded public key for {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            LOG.debug(f'Error loading public key for {self.current_chat}')
        if not self.current_chat_key:
            self.messages.warning(
                self, 'Error', 'Crypto key for user not found.')
            return
        self.ui.label_new_message.setText(
            f'Input message for user {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)
        self.history_list_update()

    def clients_list_update(self):
        """
        Update friends list method.
        :return:
        """
        friends_list = self.database.get_friends()
        self.contacts_model = QStandardItemModel()
        for i in sorted(friends_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """
        Create add friend window method.
        :return:
        """
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """
        Adding user to friends list event method.
        :param item:
        :return:
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Adding user to friends list in client and server DB method.
        :param new_contact:
        :return:
        """
        try:
            self.transport.add_friend(new_contact)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', CON_ERR)
                self.close()
            self.messages.critical(self, 'Error', TIME_ERR)
        else:
            self.database.add_friend_to_list(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            LOG.debug(f'Added friend {new_contact}')
            self.messages.information(self, 'Success', 'Friend added.')

    def delete_contact_window(self):
        """
        Remove user from friends list event method.
        :return:
        """
        global remove_dialog
        remove_dialog = DelContactDialog(self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """
        Remove user from friends list in client and server DB method.
        :param item:
        :return:
        """
        selected = item.selector.currentText()
        try:
            self.transport.remove_friend(selected)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', CON_ERR)
                self.close()
            self.messages.critical(self, 'Error', TIME_ERR)
        else:
            self.database.del_friend_from_list(selected)
            self.clients_list_update()
            LOG.debug(f'Removed from friends list {selected}')
            self.messages.information(self, 'Success', 'User removed.')
            item.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Encrypt and send message to friend method.
        :return:
        """
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        message_text_encrypted = self.encryptor.encrypt(message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(message_text_encrypted)
        try:
            self.transport.send_message(self.current_chat, message_text_encrypted_base64.decode('ascii'))
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', CON_ERR)
                self.close()
            self.messages.critical(self, 'Error', TIME_ERR)
        else:
            self.database.save_message(self.current_chat, 'out', message_text)
            LOG.debug(f'Message was sent to {self.current_chat}: {message_text}')
            self.history_list_update()

    @pyqtSlot(dict)
    def message(self, message):
        """
        Slot handler of incoming messages, performs decryption
        received messages and their saving in the message history.
        Asks the user if the message is not from the current one
        interlocutor. Changes the interlocutor if necessary.
        :param message:
        :return:
        """
        encrypted_message = base64.b64decode(message[MESSAGE_TEXT])
        LOG.debug(f'Encrypted message {encrypted_message}')
        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
            LOG.debug(f'Decrypted message {decrypted_message}')
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Error', 'Cannot decode message.')
            return
        sender = message[SENDER]
        self.database.save_message(sender, 'in', decrypted_message.decode('utf8'))
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_friend(sender):
                if self.messages.question(self, 'New message', f'New message from {sender}, open chat?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                if self.messages.question(self, 'New message',
                                          f'New message from {sender}.\n User not in friends list.\n Add and open chat?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.database.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """
        Slot handler of Connection lost.
        :return:
        """
        self.messages.warning(self, 'Connection error', CON_ERR)
        self.close()

    def make_connection(self, trans_obj):
        """
        Connect signals with slots.
        :param trans_obj:
        :return:
        """
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)
        trans_obj.message_205.connect(self.sig_205)

    @pyqtSlot()
    def sig_205(self):
        """
        Database update from server method.
        :return:
        """
        if self.current_chat and not self.database.check_user(self.current_chat):
            self.messages.warning(self, 'Sorry', 'User deleted.')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_list_update()
