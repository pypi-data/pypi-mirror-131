import sys
import logging
# sys.path.append('../')
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt

LOG = logging.getLogger('client')


class AddContactDialog(QDialog):
    """
    Dialogue for adding a user to the friends list.
    Provides the user with a list of possible friends and
    adds the selected one to friends.
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database
        self.setFixedSize(350, 120)
        self.setWindowTitle('Select user to add:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.selector_label = QLabel('Select user to add:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)
        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)
        self.btn_refresh = QPushButton('Refresh list', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)
        self.btn_ok = QPushButton('Add', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)
        self.possible_friends_update()
        self.btn_refresh.clicked.connect(self.update_possible_friends)

    def possible_friends_update(self):
        """
        A method for filling out the list of possible friends.
        Creates a list of all registered users
        except for those already added to friends and yourself.
        """
        self.selector.clear()
        friends_list = set(self.database.get_friends())
        users_list = set(self.database.get_all_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - friends_list)

    def update_possible_friends(self):
        """
        Method for updating the list of possible friends. Requests from the server
        the list of known users and wipes out the contents of the window.
        """
        try:
            self.transport.user_list_request()
        except OSError:
            pass
        else:
            LOG.debug('Refresh users complete.')
            self.possible_friends_update()
