import os.path
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, \
    String, Text, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class ClientDatabase:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью SQLAlchemy ORM
    и используется классический подход.
    """

    class KnownUsers:
        """Класс - отображение для таблицы всех пользователей."""

        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageStat:
        """Класс - отображение для таблицы статистики переданных сообщений."""

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.now()

    class Contacts:
        """Класс - отображение для таблицы контактов."""

        def __init__(self, name):
            self.id = None
            self.name = name

    def __init__(self, name):
        path = os.getcwd()
        filename = f'client_{name}.db3'
        self.db_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False})
        self.metadata = MetaData()

        # Известные пользователи
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String))

        # История сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime))

        # Контакты
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))

        self.metadata.create_all(self.db_engine)

        # Отображения
        mapper(self.KnownUsers, users)
        mapper(self.MessageStat, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Метод добавляющий контакт в базу данных."""
        if not self.session.query(
                self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        """Метод очищающий таблицу со списком контактов."""
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """Метод удаляющий определённый контакт."""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Метод заполняющий таблицу известных пользователей."""
        self.session.query(self.KnownUsers).delete()

        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """Метод сохраняющий сообщение в базе данных."""
        message_row = self.MessageStat(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """Метод возвращающий список всех контактов."""
        return [contact[0] for contact in self.session.query(
            self.Contacts.name).all()]

    def get_users(self):
        """Метод возвращающий список всех известных пользователей."""
        return [user[0] for user in self.session.query(
            self.KnownUsers.username).all()]

    def check_user(self, user):
        """Метод проверяющий существует ли пользователь."""
        if self.session.query(
                self.KnownUsers).filter_by(username=user).count():
            return True
        return False

    def check_contact(self, contact):
        """Метод проверяющий существует ли контакт."""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        return False

    def get_history(self, contact):
        """
        Метод возвращающий историю сообщений с определённым пользователем.
        """
        query = self.session.query(self.MessageStat).filter_by(contact=contact)
        return [(hist_row.contact,
                 hist_row.direction,
                 hist_row.message,
                 hist_row.date) for hist_row in query.all()]


if __name__ == '__main__':
    test_db = ClientDatabase('wasya')
    # for contact in ['masya', 'beaver', 'ipsum']:
    #     test_db.add_contact(contact)
    # test_db.add_contact('someone')
    #
    # test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    # test_db.save_message('test1', 'test2', f'Привет! я тестовое сообщение, время: {datetime.now()}!')
    # test_db.save_message('test2', 'test1', f'Привет! я другое тестовое сообщение, время: {datetime.now()}!')
    #
    # print(test_db.get_contacts())
    # print(test_db.get_users())
    # print(test_db.check_user('test1'))
    # print(test_db.check_user('test10'))
    # print(test_db.get_history('test2'))
    # print(test_db.get_history('test3'))
    # test_db.del_contact('someone')
    # print(test_db.get_contacts())

    # print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
