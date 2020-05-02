from flask_restful import Resource
import traceback
from flask import request


class GetVotesOfArticle(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            if request.args.get('article_id') is None:
                return "", "500 'article_id' parameter is missing"

            count = self.db.count(self.db.tables["ArticleVote"], {"article_id": request.args.get('article_id')})

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return count, "200"
