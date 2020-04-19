from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from webserv.pattern.singleton import Singleton
from flask_sqlalchemy import SQLAlchemy
from utils.config import DB_URI


class DB(metaclass=Singleton):

    engine = None

    def __init__(self, application=None):
        db_uri = URL(**DB_URI)

        self.engine = create_engine(db_uri, pool_recycle=100, pool_pre_ping=True)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()

        self.tables = {}
        base = declarative_base()
        base.metadata = MetaData(bind=self.engine)

        self.db = self

        for table in self.db.engine.table_names():
            attr = {'__tablename__': table,
                    '__table_args__': {'autoload': True, 'autoload_with': self.db.engine}}
            self.tables[table] = type(table, (base,), attr)

    ###############
    # GLOBAL      #
    ###############

    def merge(self, data, table):
        if type(data) == dict:
            data = table(**data)
            data = self.session.merge(data)
        elif type(data) == list:
            for row in data:
                if type(row) == dict:
                    row = table(**row)
                self.session.merge(row)
        else:
            data = self.session.merge(data)

        self.session.commit()
        return data

    def insert(self, data, table):
        if type(data) == dict:
            data = table(**data)
            self.session.add(data)
        else:
            for row in data:
                if type(row) == dict:
                    row = table(**row)
                self.session.add(row)
        self.session.commit()

    def get(self, table, filters={}):
        q = self.session.query(table)
        for attr, value in filters.items():
            if type(value) == list:
                q = q.filter(getattr(table, attr).in_(value))
            else:
                q = q.filter(getattr(table, attr) == value)
        return q.all()

    def delete(self, table, filters=None):
        if filters is None:
            # We don't take the risk to have to filter on delete, truncate() is made for that
            return
        else:
            q = self.session.query(table)
            for attr, value in filters.items():
                if type(value) == list:
                    q = q.filter(getattr(table, attr).in_(value))
                else:
                    q = q.filter(getattr(table, attr) == value)
            q.delete()
            self.session.commit()

    def get_count(self, table):
        return self.session.query(table).count()

    def truncate(self, table):
        if ".Smowg" in str(table):
            self.session.query(table).delete()
            self.session.commit()