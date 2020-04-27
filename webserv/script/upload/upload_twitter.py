import tweepy
import datetime
import os
from utils.config import PROJECT_PATH
import sys
from db.db import DB

consumer_key = "eMhpRZbngPMLg95L2JZnBIk2P"
consumer_secret = "OrzR4HDMOzLNauCdRcT2dRCDA5eQkEDOPb7wxpoM11ZbakL513"
access_token = "1247554748737257472-AC5JfRfNkgeqUMQtpChZ7cVTrKWjr2"
access_token_secret = "JRArrhqeXoTIIjuH5ZY7Tt0s4QBB78rd8NeNiTQ1zmdKu"

category = sys.argv[1]
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')

db = DB()

video = db.get(db.tables["Video"], {"format": "youtube", "category": category, "creation_date": datetime.date.today()})

if len(video) == 0:
    print("No video found")
    sys.exit(0)
else:
    video = video[0]

if video.youtube_id is None:
    print("Video has no youtube ID")
    sys.exit(0)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status(
    status=f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le {category}\n\n"
           f"#Highlite #News #Actu #Today #{category}\n\n"
           f"https://youtube.com/watch?v={video.youtube_id}")
