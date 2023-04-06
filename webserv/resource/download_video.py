from flask_restful import Resource
import traceback
from utils.config import PROJECT_PATH
import os
import datetime
from flask import request, send_from_directory


class DownloadVideo(Resource):

    def get(self):
        try:

            if request.args.get('video_name') is None:
                return "", "500 'video_name' parameter is missing"

            today = datetime.date.today()

            directory = os.path.join(PROJECT_PATH, "output", today.strftime("%Y-%m-%d"))
            video = send_from_directory(directory=directory, filename=request.args.get('video_name'))

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return video
