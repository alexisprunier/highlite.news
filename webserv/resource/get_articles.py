from flask_restful import Resource
import traceback
from utils.serializer import Serializer


class GetArticles(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            query = self.db.get_articles_in_wait()

            articles = []

            for q in query:
                self.db.session.expunge(q[0])
                q[0].image = None
                articles.append(q[0])

            articles = Serializer.serialize(articles, self.db.tables["Article"])

            for index, article in enumerate(articles):
                article["nb_vote"] = query[index][1]

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return articles, "200"
