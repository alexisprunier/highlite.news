from flask_restful import Resource
import traceback


class GetVideos(Resource):

    def get(self):
        try:
            pass
        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return "", "200"
