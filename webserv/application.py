from flask_restful import Api
from flask import render_template
from flask_cors import CORS
from flask import Flask
from webserv.resource.get_videos import GetVideos


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = None#db_uri
application.config['SQLALCHEMY_POOL_RECYCLE'] = 60
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
application.config["ERROR_404_HELP"] = False

cors = CORS(application, resources={r"/*": {"origins": "*"}})
api = Api(application)

# Routes

api.add_resource(GetVideos, '/r/get_videos')


@application.route('/<generic>')
def undefined_route():
    return render_template('404.html'), 404


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
