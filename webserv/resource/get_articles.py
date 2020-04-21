from flask_restful import Resource
import traceback
from utils.serializer import Serializer
import datetime


class GetArticles(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            today = datetime.date.today()
            articles = self.db.get(self.db.tables["Article"], {"scrap_date": today})

            for article in articles:
                article.image = None

            articles = Serializer.serialize(articles, self.db.tables["Article"])

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return articles, "200"
