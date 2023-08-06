import sys

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
import logging
import datetime

sys.path.append('../../')

LOG = logging.getLogger('server')


class ServerDB:
    """
    The class is a wrapper for working with the server database.
    Uses SQLite database, implemented with
    SQLAlchemy ORM and the classic approach is used.
    """
    class Users:
        """
        All users table class.
        """
        def __init__(self, username, passwd_hash):
            self.id = None
            self.uname = username
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None

    class ActiveUsers:
        """
        Active users table class.
        """
        def __init__(self, user_id, user_addr, user_port, login_time):
            self.user = user_id
            self.user_addr = user_addr
            self.user_port = user_port
            self.login_time = login_time
            self.id = None

    class LoginHistory:
        """
        History of user logins table class.
        """
        def __init__(self, username, user_addr, user_port, login_time):
            self.id = None
            self.username = username
            self.user_addr = user_addr
            self.user_port = user_port
            self.login_time = login_time

    class ContactList:
        """
        Friends list table class.
        """
        def __init__(self, owner, user_id):
            self.owner = owner
            self.friend = user_id
            self.add_time = datetime.datetime.now()

    class UsersHistory:
        """
        Users actions table class.
        """
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, db_file):
        self.database_engine = create_engine(f'sqlite:///{db_file}', echo=False,
                                             pool_recycle=7200, connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        users_tb = Table('Users', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('uname', String, unique=True),
                         Column('last_login', DateTime),
                         Column('passwd_hash', String),
                         Column('pubkey', Text))

        active_users_tb = Table('Active_Users', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('user', ForeignKey('Users.id'), unique=True),
                                Column('user_addr', String),
                                Column('user_port', Integer),
                                Column('login_time', DateTime))

        users_history_tb = Table('History', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('user', ForeignKey('Users.id')),
                                 Column('sent', Integer),
                                 Column('accepted', Integer))

        login_history_tb = Table('Login_History', self.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('username', ForeignKey('Users.id')),
                                 Column('login_time', DateTime),
                                 Column('user_addr', String),
                                 Column('user_port', String))

        contact_list_tb = Table('Contact_List', self.metadata,
                                Column('id', Integer, primary_key=True),
                                Column('owner', ForeignKey('Users.id')),
                                Column('friend', ForeignKey('Users.id')),
                                Column('add_time', DateTime))

        self.metadata.create_all(self.database_engine)
        mapper(self.Users, users_tb)
        mapper(self.ActiveUsers, active_users_tb)
        mapper(self.LoginHistory, login_history_tb)
        mapper(self.ContactList, contact_list_tb)
        mapper(self.UsersHistory, users_history_tb)
        connection = sessionmaker(bind=self.database_engine)
        self.session = connection()
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, user_addr, user_port, key):
        """
        The method executed when the user logs in, writes the fact of the login to the database
        Updates the user's public key when it changes.
        :param username:
        :param user_addr:
        :param user_port:
        :param key:
        :return:
        """
        check_user = self.session.query(self.Users).filter_by(uname=username)
        if check_user.count():
            LOG.info(f'User login: {username}, {user_addr}, {user_port}.')
            user = check_user.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        else:
            raise ValueError('User is not registered.')
        is_active_user = self.ActiveUsers(user.id, user_addr, user_port, datetime.datetime.now())
        self.session.add(is_active_user)
        history = self.LoginHistory(user.id, user_addr, user_port, datetime.datetime.now())
        self.session.add(history)
        self.session.commit()

    def add_user(self, name, passwd_hash):
        """
        Register user method.
        :param name:
        :param passwd_hash:
        :return:
        """
        user_row = self.Users(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        """
        Remove user method.
        :param name:
        :return:
        """
        user = self.session.query(self.Users).filter_by(uname=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(username=user.id).delete()
        self.session.query(self.ContactList).filter_by(owner=user.id).delete()
        self.session.query(
            self.ContactList).filter_by(friend=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.Users).filter_by(uname=name).delete()
        self.session.commit()

    def get_hash(self, name):
        """
        Get password HASH method.
        """
        user = self.session.query(self.Users).filter_by(uname=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        """
        Get user public key method.
        :param name:
        :return:
        """
        user = self.session.query(self.Users).filter_by(uname=name).first()
        return user.pubkey

    def check_user(self, name):
        """
        Check is user registered method.
        :param name:
        :return:
        """
        if self.session.query(self.Users).filter_by(uname=name).count():
            return True
        else:
            return False

    def user_logout(self, username):
        """
        User logout method.
        :param username:
        :return:
        """
        LOG.info(f'User logout: {username}.')
        user = self.session.query(self.Users).filter_by(uname=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        """
        Get all users list method.
        :return:
        """
        LOG.info(f'User List. Query.')
        query = self.session.query(self.Users.uname, self.Users.last_login)
        return query.all()

    def active_users_list(self):
        """
        Get active users list method.
        :return:
        """
        LOG.info(f'Active User List. Query.')
        query = self.session.query(self.Users.uname, self.ActiveUsers.user_addr, self.ActiveUsers.user_port,
                                   self.ActiveUsers.login_time).join(self.Users)
        return query.all()

    def login_history(self, username=None):
        """
        Get user login history method.
        :param username:
        :return:
        """
        LOG.info(f'User Login History. Query. For {username}')
        query = self.session.query(self.Users.uname, self.LoginHistory.login_time, self.LoginHistory.user_addr,
                                   self.LoginHistory.user_port).join(self.Users)
        if username:
            query = query.filter(self.Users.uname == username)
        return query.all()

    def get_user_id(self, username):
        """
        Get user ID by Username method.
        :param username:
        :return:
        """
        user_obj = self.session.query(self.Users).filter_by(uname=username).first()
        return user_obj.id

    def add_friend_to_list(self, owner, friend_name):
        """
        Add user to friends list method.
        :param owner:
        :param friend_name:
        :return:
        """
        owner_id = self.get_user_id(owner)
        friend_id = self.get_user_id(friend_name)
        if not self.session.query(self.ContactList).filter_by(owner=owner_id, friend=friend_id).count():
            LOG.info(f'New friend in list of user {owner}: {friend_name}')
            new_friend = self.ContactList(owner_id, friend_id)
            self.session.add(new_friend)
            self.session.commit()
        else:
            LOG.info(f'User {friend_name} is in contact list of user {owner}. Adding aborted.')

    def del_friend_from_list(self, owner, friend_name):
        """
        Remove user from friends list method.
        :param owner:
        :param friend_name:
        :return:
        """
        owner_list_id = self.get_user_id(owner)
        friend_id = self.get_user_id(friend_name)
        if self.session.query(self.ContactList).filter_by(owner=owner_list_id, friend=friend_id).count():
            self.session.query(self.ContactList).filter_by(owner=owner_list_id, friend=friend_id).delete()
            self.session.commit()
            LOG.info(f'User {friend_name} is delete from contact list of {owner}')
        else:
            LOG.info(f'User {friend_name} not in contact list of user {owner}. Delete aborted.')

    def list_friends(self, owner):
        """
        Get friends list method.
        :param owner:
        :return:
        """
        user_id = self.get_user_id(owner)
        query = self.session.query(self.ContactList, self.Users.uname).filter_by(owner=user_id).join(self.Users,
                                                                        self.ContactList.friend == self.Users.id)
        return [friend[1] for friend in query.all()]

    def process_message(self, sender, recipient):
        """
        Processing messaging. Add to history method.
        :param sender:
        :param recipient:
        :return:
        """
        sender = self.get_user_id(sender)
        recipient = self.get_user_id(recipient)
        sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_row.accepted += 1
        LOG.debug(f'Processing message from {sender} to {recipient}')
        self.session.commit()

    def message_history(self):
        """
        Get messages history method.
        :return:
        """
        LOG.debug('Update message history.')
        query = self.session.query(self.Users.uname, self.Users.last_login, self.UsersHistory.sent,
                                   self.UsersHistory.accepted).join(self.Users)
        return query.all()
