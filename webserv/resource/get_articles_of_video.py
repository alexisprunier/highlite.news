from flask_restful import Resource
from utils.serializer import Serializer
from flask import request


class GetArticlesOfVideo(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            if request.args.get('video_id') is None:
                return "", "500 'video_id' parameter is missing"

            query = self.db.get_articles_of_video(request.args.get('video_id'))

            articles = []

            for a in query:
                self.db.session.expunge(a)
                a.image = None
                articles.append(a)

            articles = Serializer.serialize(articles, self.db.tables["Article"])

        except Exception as e:
            return "", "500 " + str(e)

        return articles, "200"
