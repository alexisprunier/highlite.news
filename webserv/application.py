from flask_restful import Api
from flask_cors import CORS
from flask import Flask, send_from_directory
from webserv.resource.get_videos import GetVideos
from webserv.resource.get_videos_of_the_day import GetVideosOfTheDay
from webserv.resource.get_articles import GetArticles
from webserv.resource.get_articles_of_video import GetArticlesOfVideo
from webserv.resource.get_votes_of_article import GetVotesOfArticle
from webserv.resource.download_video import DownloadVideo
from webserv.resource.vote import Vote
from utils.config import DB_URI, ENVIRONMENT, PROJECT_PATH
from threading import Thread
from db.db import DB
from sqlalchemy.engine.url import URL
from webserv.script.cron import Cron
import os


db_uri = URL(**DB_URI)
application = Flask(__name__, static_folder=None)
application.config['SQLALCHEMY_DATABASE_URI'] = db_uri
application.config['SQLALCHEMY_POOL_RECYCLE'] = 60
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["ERROR_404_HELP"] = False

cors = CORS(application, resources={r"/*": {"origins": "*"}})
api = Api(application)
db = DB()

# Routes

api.add_resource(GetVideos, '/r/get_videos', resource_class_kwargs={"db": db})
api.add_resource(GetVideosOfTheDay, '/r/get_videos_of_the_day', resource_class_kwargs={"db": db})
api.add_resource(GetArticles, '/r/get_articles', resource_class_kwargs={"db": db})
api.add_resource(GetArticlesOfVideo, '/r/get_articles_of_video', resource_class_kwargs={"db": db})
api.add_resource(GetVotesOfArticle, '/r/get_votes_of_article', resource_class_kwargs={"db": db})
api.add_resource(Vote, '/r/vote', resource_class_kwargs={"db": db})
api.add_resource(DownloadVideo, '/r/download_video')


@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(PROJECT_PATH, "webapp", "build", path)):
        return send_from_directory(os.path.join(PROJECT_PATH, "webapp", "build"), path)
    else:
        return send_from_directory(os.path.join(PROJECT_PATH, "webapp", "build"), 'index.html')


cron = Cron()
cron = Thread(target=cron.run)
cron.start()

if __name__ == '__main__':
    application.run(
        debug=False if ENVIRONMENT == "production" else True,
        use_reloader=True if ENVIRONMENT == "production" else False,
        port=None if ENVIRONMENT == "production" else 5002
    )
