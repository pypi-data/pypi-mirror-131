"""Модуль содержащий класс описания клиентской базы данных"""
import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, \
    Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientDataBase:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """

    class KnownUsers:
        """
        Класс - отображение всех пользователей
        """

        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """
        Класс - отображение статистики сообщений
        """

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """
        Класс - контакты пользователей
        """

        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        self.database_engine = create_engine(
            f'sqlite:///client_{name}.db3',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})
        self.metadata = MetaData()

        users = Table('Known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        self.metadata.create_all(self.database_engine)

        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """
        Метод добавления контакта в базу данных
        """
        if not self.session.query(
                self.Contacts).filter_by(
            name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def del_contact(self, contact):
        """
        Метод удаления контакта из базы данных
        """
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """
        Метод заполняющий таблицу известных пользователей
        """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """
        Метод сохраняющий сообщение в базе данных
        """
        message_row = self.MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """
        Метод получения всех контактов из базы данных
        """
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """
        Метод получения всех пользователей из базы данных
        """
        return [user[0]
                for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """
        Метод проверяющий существует ли пользователь
        """
        return bool(self.session.query(
            self.KnownUsers).filter_by(
            username=user).count())

    def check_contact(self, contact):
        """
        Метод проверяющий существует ли контакт
        """
        return bool(
            self.session.query(self.Contacts).filter_by(name=contact).count())

    def get_history(self, contact):
        """
        Метод возвращающий историю сообщений с определённым пользователем
        """
        query = self.session.query(
            self.MessageHistory).filter_by(
            contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]
