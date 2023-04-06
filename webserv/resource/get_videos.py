from flask_restful import Resource
import traceback
from utils.serializer import Serializer
import datetime


class GetVideos(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)

            videos = self.db.get(self.db.tables["Video"], {"format": "youtube"})
            videos = [v for v in videos if v.youtube_id is not None and v.creation_date > week_ago]
            videos = Serializer.serialize(videos, self.db.tables["Video"])

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return videos, "200"
