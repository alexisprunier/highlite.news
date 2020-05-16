import os
from utils.config import PROJECT_PATH, ENVIRONMENT
import schedule
import time
from db.db import DB
import functools
import datetime
import traceback
from webserv.exception.upload import UploadException
from webserv.exception.already_generated import AlreadyGeneratedException


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
            self.db.merge(log, self.db.tables["Log"])
        finally:
            pass

    return wrapper


def run():

    db = DB()
    pipelines = db.get(db.tables["Pipeline"])
    db.session.close()
    pre_command = "sudo python3 " if ENVIRONMENT != "dev" else ""

    @log_manager
    def scrap(category):
        scrap_script = os.path.join(PROJECT_PATH, "webserv", "script", "scrap", "scrap_articles.py")
        os.system(f'{pre_command}{scrap_script} "{category}"')

    @log_manager
    def generate(category):
        generate_script = os.path.join(PROJECT_PATH, "webserv", "script", "generate", "generate_video.py")
        try:
            os.system(f'{pre_command}{generate_script} "{category}" youtube')
        except AlreadyGeneratedException as e:
            print(e)
        try:
            os.system(f'{pre_command}{generate_script} "{category}" instagram')
        except AlreadyGeneratedException as e:
            print(e)
        try:
            os.system(f'{pre_command}{generate_script} "{category}" tiktok')
        except AlreadyGeneratedException as e:
            print(e)

    @log_manager
    def upload(category):
        upload_youtube_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_youtube.py")
        upload_twitter_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_twitter.py")
        upload_facebook_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_facebook.py")

        try:
            os.system(f'{pre_command}{upload_youtube_script} "{category}"')
        except UploadException as e:
            print(e)
        time.sleep(30)
        try:
            os.system(f'{pre_command}{upload_twitter_script} "{category}"')
        except UploadException as e:
            print(e)
        try:
            os.system(f'{pre_command}{upload_facebook_script} "{category}"')
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
