import os
from utils.config import PROJECT_PATH
import schedule
import time
from db.db import DB
import functools
import datetime
import traceback


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

    @log_manager
    def scrap(category):
        scrap_script = os.path.join(PROJECT_PATH, "webserv", "script", "scrap", "scrap_articles.py")
        os.system(f"{scrap_script} {category}")

    @log_manager
    def generate(category):
        generate_script = os.path.join(PROJECT_PATH, "webserv", "script", "generate", "generate_video.py")
        os.system(f"{generate_script} {category}")

    @log_manager
    def upload(category):
        upload_youtube_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_youtube.py")
        upload_twitter_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_twitter.py")
        upload_facebook_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_facebook.py")
        os.system(f"{upload_youtube_script} {category}")
        time.sleep(30)
        os.system(f"{upload_twitter_script} {category}")
        os.system(f"{upload_facebook_script} {category}")

    for p in pipelines:
        schedule.every().day.at(p.scrap_time).do(scrap, p.category)
        schedule.every().day.at(p.genaration_time).do(generate, p.category)
        schedule.every().day.at(p.publication_time).do(upload, p.category)

    while True:
        print("check")
        schedule.run_pending()
        time.sleep(60)
