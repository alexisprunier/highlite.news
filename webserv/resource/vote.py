from flask_restful import Resource
import traceback


class Vote(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def post(self):
        try:



        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return articles, "200"
