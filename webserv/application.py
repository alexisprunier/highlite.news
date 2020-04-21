from flask_restful import Api
from flask import render_template
from flask_cors import CORS
from flask import Flask
from webserv.resource.get_videos import GetVideos
from webserv.resource.get_articles import GetArticles
from webserv.resource.get_articles_of_video import GetArticlesOfVideo
from webserv.resource.vote import Vote
from utils.config import DB_URI
from db.db import DB
from sqlalchemy.engine.url import URL


db_uri = URL(**DB_URI)
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = db_uri
application.config['SQLALCHEMY_POOL_RECYCLE'] = 60
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["ERROR_404_HELP"] = False

cors = CORS(application, resources={r"/*": {"origins": "*"}})
api = Api(application)
db = DB()

# Routes

api.add_resource(GetVideos, '/r/get_videos', resource_class_kwargs={"db": db})
api.add_resource(GetArticles, '/r/get_articles', resource_class_kwargs={"db": db})
api.add_resource(GetArticlesOfVideo, '/r/get_articles_of_video', resource_class_kwargs={"db": db})
api.add_resource(Vote, '/r/vote', resource_class_kwargs={"db": db})


@application.route('/<generic>')
def undefined_route():
    return render_template('404.html'), 404


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
