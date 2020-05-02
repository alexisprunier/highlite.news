from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from webserv.pattern.singleton import Singleton
from utils.config import DB_URI
import datetime
from sqlalchemy.orm import defer
from sqlalchemy import func


class DB(metaclass=Singleton):

    engine = None

    def __init__(self):
        db_uri = URL(**DB_URI)

        self.engine = create_engine(db_uri, pool_recycle=100, pool_pre_ping=True, isolation_level="READ COMMITTED")
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

    def count(self, table, filters={}):
        q = self.session.query(table)
        for attr, value in filters.items():
            if type(value) == list:
                q = q.filter(getattr(table, attr).in_(value))
            else:
                q = q.filter(getattr(table, attr) == value)
        return q.count()

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
        self.session.query(table).delete()
        self.session.commit()

    ###############
    # ARTICLE     #
    ###############

    def get_articles_in_wait(self):
        sub_query = self.session.query(self.tables["Video"].category) \
            .filter(self.tables["Video"].creation_date == datetime.date.today()) \
            .distinct().subquery()

        rows = self.session.query(self.tables["Article"], func.count(self.tables["ArticleVote"].id)) \
            .options(defer("image")) \
            .filter(self.tables["Article"].category.notin_(sub_query)) \
            .filter(self.tables["Article"].scrap_date == datetime.date.today()) \
            .outerjoin(self.tables["ArticleVote"]).group_by(self.tables["Article"]).all()
        return rows

    def get_articles_of_the_day(self, category):
        rows = self.session.query(self.tables["Article"], func.count(self.tables["ArticleVote"].id)) \
            .filter(self.tables["Article"].category == category) \
            .filter(self.tables["Article"].scrap_date == datetime.date.today()) \
            .outerjoin(self.tables["ArticleVote"]).group_by(self.tables["Article"]).all()

        rows.sort(key=lambda o: o[1], reverse=True)

        articles = []

        for i in range(0, min(10, len(rows))):
            articles.append(rows[i][0])

        return articles

    def get_articles_of_video(self, video_id):
        sub_query = self.session.query(self.tables["VideoArticle"].article_id) \
            .filter(self.tables["VideoArticle"].video_id == video_id).subquery()

        rows = self.session.query(self.tables["Article"]) \
            .options(defer("image")) \
            .filter(self.tables["Article"].id.in_(sub_query)).all()

        return rows
