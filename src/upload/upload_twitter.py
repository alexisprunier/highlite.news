import tweepy
import datetime
import os
from utils.config import PROJECT_PATH
import sys

consumer_key = "eMhpRZbngPMLg95L2JZnBIk2P"
consumer_secret = "OrzR4HDMOzLNauCdRcT2dRCDA5eQkEDOPb7wxpoM11ZbakL513"
access_token = "1247554748737257472-AC5JfRfNkgeqUMQtpChZ7cVTrKWjr2"
access_token_secret = "JRArrhqeXoTIIjuH5ZY7Tt0s4QBB78rd8NeNiTQ1zmdKu"

category = sys.argv[1]
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')
youtube_video_id_path = os.path.join(PROJECT_PATH, "data", today, f"youtube_video_id_{category}.txt")

if not os.path.exists(youtube_video_id_path):
    print("Youtube video not found")
    exit()

f = open(youtube_video_id_path, "r")
youtube_video_id = f.read()
f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status(status=f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le {category}\n\nhttps://youtube.com/watch?v={youtube_video_id}")
