from flask_restful import Resource
import traceback
from utils.serializer import Serializer
import datetime


class GetVideosOfTheDay(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            today = datetime.date.today()

            videos = self.db.get(self.db.tables["Video"], {"creation_date": today})
            videos = Serializer.serialize(videos, self.db.tables["Video"])

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return videos, "200"
