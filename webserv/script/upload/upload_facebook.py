import facebook
from db.db import DB
import sys
import datetime
from webserv.exception.upload import UploadException


client_id = "958139691273238"
client_secret = "49103d0b53faa969c83831ed48c3dbda"
access_token = "958139691273238|5EkCIBU38wE16cEWUDZOKabe4-s"

# TO GENERATE THE LEY
#
#curl -X GET "https://graph.facebook.com/oauth/access_token
#  ?client_id={958139691273238}
#  &client_secret={49103d0b53faa969c83831ed48c3dbda}
#  &grant_type=client_credentials"

category = sys.argv[1]
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')

db = DB()

#############
# CHECK
#############

video = db.get(db.tables["Video"], {"format": "youtube", "category": category, "creation_date": datetime.date.today()})
video = video[0] if len(video) > 0 else None

if video is None:
    raise UploadException("Video not found in DB")

if video.youtube_id is None:
    raise UploadException("Video has no youtube ID")

upload = db.get(db.tables["Upload"], {"video_id": video.id, "platform": "facebook"})

if len(upload) > 0:
    raise UploadException("This video already in the upload table")

#############
# POST
#############

graph = facebook.GraphAPI(access_token=access_token, version="3.0")

graph.put_object(
    parent_object="highlite.news",
    connection_name="feed",
    message=f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le {category}\n\n"
            f"#Highlite #News #Actu #Today #{category.replace('-', '')}\n\n"
            f"https://youtube.com/watch?v={video.youtube_id}"
)

#############
# ADD TO DB
#############

upload = {
    "video_id": video.id,
    "platform": "facebook",
    "publication_datetime": datetime.datetime.now(),
}

db.merge(upload, db.tables["Upload"])
db.session.close()