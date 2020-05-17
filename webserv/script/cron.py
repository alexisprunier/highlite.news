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
        try:
            return func(*args)
        except Exception as error:
            print(traceback.format_exc())
        finally:
            pass

    return wrapper


class Cron:

    def run(self):

        db = DB()
        pipelines = db.get(db.tables["Pipeline"])
        db.session.close()

        @log_manager
        def scrap(db, category):
            try:
                ScrapArticles.run(db, category)
            except AlreadyGeneratedException as e:
                print(e)

        @log_manager
        def generate(db, category):
            try:
                GenerateVideo.run(db, category, 'youtube')
            except AlreadyGeneratedException as e:
                print(e)
            try:
                GenerateVideo.run(db, category, 'instagram')
            except AlreadyGeneratedException as e:
                print(e)
            try:
                GenerateVideo.run(db, category, 'tiktok')
            except AlreadyGeneratedException as e:
                print(e)

        @log_manager
        def upload(db, category):
            try:
                UploadYoutube.run(db, category)
            except UploadException as e:
                print(e)
            time.sleep(30)
            try:
                UploadTwitter.run(db, category)
            except UploadException as e:
                print(e)

        for p in pipelines:
            schedule.every().day.at(p.scrap_time).do(scrap, db, p.category)
            schedule.every().day.at(p.generation_time).do(generate, db, p.category)
            if p.publication_time is not None:
                schedule.every().day.at(p.publication_time).do(upload, db, p.category)

        while True:
            print("check")
            schedule.run_pending()
            time.sleep(60)
