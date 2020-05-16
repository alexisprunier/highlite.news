import tweepy
import datetime
from db.db import DB
from webserv.exception.upload import UploadException


class UploadTwitter:

    @staticmethod
    def run(category):

        consumer_key = "eMhpRZbngPMLg95L2JZnBIk2P"
        consumer_secret = "OrzR4HDMOzLNauCdRcT2dRCDA5eQkEDOPb7wxpoM11ZbakL513"
        access_token = "1247554748737257472-AC5JfRfNkgeqUMQtpChZ7cVTrKWjr2"
        access_token_secret = "JRArrhqeXoTIIjuH5ZY7Tt0s4QBB78rd8NeNiTQ1zmdKu"

        today = datetime.date.today().strftime('%Y-%m-%d')
        today_fr = datetime.date.today().strftime('%d-%m-%Y')

        db = DB()

        #############
        # CHECK
        #############

        pipeline = db.get(db.tables["Pipeline"], {"category": category})[0]

        video = db.get(db.tables["Video"], {"format": "youtube", "category": category, "creation_date": datetime.date.today()})
        video = video[0] if len(video) > 0 else None

        if video is None:
            raise UploadException("Video not found in DB")

        if video.youtube_id is None:
            raise UploadException("Video has no youtube ID")

        upload = db.get(db.tables["Upload"], {"video_id": video.id, "platform": "twitter"})

        if len(upload) > 0:
            raise UploadException("This video already in the upload table")

        #############
        # POST
        #############

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        additional_ht = " ".join(["#"+h for h in pipeline.hashtag.split(",")]) if pipeline.hashtag is not None else ""

        api.update_status(
            status=f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur {pipeline.article} {category}\n\n"
                   f"#Highlite #News #Actu #Today #{category.replace('-', '').replace(' ', '')} {additional_ht}\n\n"
                   f"https://youtube.com/watch?v={video.youtube_id}")

        #############
        # ADD TO DB
        #############

        upload = {
            "video_id": video.id,
            "platform": "twitter",
            "publication_datetime": datetime.datetime.now(),
        }

        db.merge(upload, db.tables["Upload"])
        db.session.close()
