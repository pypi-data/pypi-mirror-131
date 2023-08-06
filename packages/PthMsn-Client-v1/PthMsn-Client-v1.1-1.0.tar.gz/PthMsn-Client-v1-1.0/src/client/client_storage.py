from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime
import logging

LOG = logging.getLogger('client')


class ClientDB:
    """
    The class is a wrapper for working with the client database.
    Uses SQLite database, implemented with
    QLAlchemy ORM and the classic approach is used.
    """
    class AllUsers:
        """
        All Users table class.
        """
        def __init__(self, user):
            self.id = None
            self.username = user

    class Friends:
        """
        Friends table class.
        """
        def __init__(self, contact):
            self.id = None
            self.name = contact

    class MessageHistory:
        """
        Message statistic table class.
        """
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    def __init__(self, username):
        self.database_engine = create_engine(f'sqlite:///dbs/client_{username}.db3',
                                             echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.metadata = MetaData()
        users = Table('all_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String))

        friends = Table('friends', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String, unique=True))

        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime))

        self.metadata.create_all(self.database_engine)
        mapper(self.AllUsers, users)
        mapper(self.Friends, friends)
        mapper(self.MessageHistory, history)
        connection = sessionmaker(bind=self.database_engine)
        self.session = connection()
        self.session.query(self.Friends).delete()
        self.session.commit()

    def add_friend_to_list(self, friend):
        """
        Add user to friends list method.
        :param friend:
        :return:
        """
        if not self.session.query(self.Friends).filter_by(name=friend).count():
            friend_row = self.Friends(friend)
            self.session.add(friend_row)
            self.session.commit()
            LOG.debug(f'We have a new friend: {friend}')

    def del_friend_from_list(self, friend):
        """
        Remove user from friends list method.
        :param friend:
        :return:
        """
        self.session.query(self.Friends).filter_by(name=friend).delete()
        LOG.debug(f'Deleting {friend} from friends list.')

    def add_all_users(self, users_list):
        """
        Fill All User table method.
        :param users_list:
        :return:
        """
        LOG.debug(f'Fill all users: {users_list}')
        self.session.query(self.AllUsers).delete()
        for user in users_list:
            user_row = self.AllUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, from_user, direction, message):
        """
        Save message to client storage method.
        :param from_user:
        :param direction:
        :param message:
        :return:
        """
        LOG.debug(f'New message in history. From {from_user}.')
        message_row = self.MessageHistory(from_user, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_friends(self):
        """
        Get full friends list method.
        :return:
        """
        LOG.debug('Getting friends list.')
        return [contact[0] for contact in self.session.query(self.Friends.name).all()]

    def get_all_users(self):
        """
        Get all users method.
        :return:
        """
        LOG.debug('Getting all users list.')
        return [user[0] for user in self.session.query(self.AllUsers.username).all()]

    def check_user(self, user):
        """
        Check user in all users table method.
        :param user:
        :return:
        """
        LOG.debug(f'Checking user in all users: {user}.')
        if self.session.query(self.AllUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_friend(self, friend):
        """
        Check is user in a friends list method.
        :param friend:
        :return:
        """
        LOG.debug(f'Checking is user {friend} in friends list.')
        if self.session.query(self.Friends).filter_by(name=friend).count():
            return True
        else:
            return False

    def get_history(self, friend):
        """
        Get messages history with friend method.
        :param friend:
        :return:
        """
        query = self.session.query(self.MessageHistory).filter_by(contact=friend)
        return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
                for history_row in query.all()]
