import os
from utils.config import PROJECT_PATH
import schedule
import time


def run():

    def scrap(category):
        scrap_script = os.path.join(PROJECT_PATH, "webserv", "script", "scrap", "scrap_articles.py")
        os.system(f"{scrap_script} {category}")

    def generate(category):
        generate_script = os.path.join(PROJECT_PATH, "webserv", "script", "scrap", "generate_video.py")
        os.system(f"{generate_script} {category}")

    def upload(category):
        upload_youtube_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_youtube.py")
        upload_twitter_script = os.path.join(PROJECT_PATH, "webserv", "script", "upload", "upload_twitter.py")
        os.system(f"{upload_youtube_script} {category}")
        os.system(f"{upload_twitter_script} {category}")

    schedule.every().day.at("17:00").do(scrap, 'COVID-19')
    schedule.every().day.at("18:45").do(generate, 'COVID-19')
    schedule.every().day.at("19:00").do(upload, 'COVID-19')

    schedule.every().day.at("18:00").do(scrap, 'FOOTBALL')
    schedule.every().day.at("19:45").do(generate, 'FOOTBALL')
    schedule.every().day.at("20:00").do(upload, 'FOOTBALL')

    while True:
        print("check")
        schedule.run_pending()
        time.sleep(60)
