from flask_restful import Resource
import traceback
from flask import request


class Vote(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def post(self):
        try:
            form = request.get_json()

            if "article_id" not in form:
                return "", "500 'article_id' parameter is missing"

            try:
                self.db.merge(
                    {"article_id": form["article_id"], "ip": request.remote_addr},
                    self.db.tables["ArticleVote"]
                )
            except Exception as e:
                self.db.session.rollback()
                print(e)
                return "", "500 Vous ne pouvez plus voter pour cette article"

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return "", "200"
