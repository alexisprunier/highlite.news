from instapy_cli import client
import datetime
import os
import pathlib

username = 'highlite.news'
password = '1224Alex!'
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')
text = 'Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le COVID-19'

project_path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
video_path = os.path.join(project_path, "output", today, f"highlite_instagram_{today}.avi")

with client(username, password) as cli:
    cli.upload(video_path, text)
