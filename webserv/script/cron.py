import schedule
import time
from db.db import DB
import functools
import datetime
import traceback
from webserv.exception.upload import UploadException
from webserv.exception.already_generated import AlreadyGeneratedException
from webserv.script.upload.upload_twitter import UploadTwitter
from webserv.script.upload.upload_youtube import UploadYoutube
from webserv.script.generate.generate_video import GenerateVideo
from webserv.script.scrap.scrap_articles import ScrapArticles


def log_manager(func):
    @functools.wraps(func)
    def wrapper(*args):
        self = args[0]
        try:
            return func(self)
        except Exception as error:
            log = {
                "status": "ERROR",
                "date": datetime.datetime.now(),
                "trace": traceback.format_exc()
            }
            #self.db.merge(log, self.db.tables["Log"])
        finally:
            pass

    return wrapper


def run():

    db = DB()
    pipelines = db.get(db.tables["Pipeline"])
    db.session.close()

    @log_manager
    def scrap(category):
        try:
            ScrapArticles.run(category)
        except AlreadyGeneratedException as e:
            print(e)

    @log_manager
    def generate(category):
        try:
            GenerateVideo.run(category, 'youtube')
        except AlreadyGeneratedException as e:
            print(e)
        try:
            GenerateVideo.run(category, 'instagram')
        except AlreadyGeneratedException as e:
            print(e)
        try:
            GenerateVideo.run(category, 'tiktok')
        except AlreadyGeneratedException as e:
            print(e)

    @log_manager
    def upload(category):
        try:
            UploadYoutube.run(category)
        except UploadException as e:
            print(e)
        time.sleep(30)
        try:
            UploadTwitter.run(category)
        except UploadException as e:
            print(e)

    for p in pipelines:
        schedule.every().day.at(p.scrap_time).do(scrap, p.category)
        schedule.every().day.at(p.generation_time).do(generate, p.category)
        if p.publication_time is not None:
            schedule.every().day.at(p.publication_time).do(upload, p.category)

    while True:
        print("check")
        schedule.run_pending()
        time.sleep(60)
