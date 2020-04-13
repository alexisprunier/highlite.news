import tweepy
import datetime
import pathlib
import os

consumer_key = "eMhpRZbngPMLg95L2JZnBIk2P"
consumer_secret = "OrzR4HDMOzLNauCdRcT2dRCDA5eQkEDOPb7wxpoM11ZbakL513"
access_token = "1247554748737257472-AC5JfRfNkgeqUMQtpChZ7cVTrKWjr2"
access_token_secret = "JRArrhqeXoTIIjuH5ZY7Tt0s4QBB78rd8NeNiTQ1zmdKu"

project_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')
youtube_video_id_path = os.path.join(project_path, "data", today, "youtube_video_id.txt")

if not os.path.exists(youtube_video_id_path):
    print("Youtube video not found")
    exit()

f = open("demofile.txt", "r")
youtube_video_id = f.read()
f.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

api.update_status(status=f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le COVID-19\n\nhttps://youtube.com/watch?v={youtube_video_id}")
