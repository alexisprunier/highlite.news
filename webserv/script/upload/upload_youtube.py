import http.client
import httplib2
import os
import random
import time
import datetime
import json
from utils.config import PROJECT_PATH
import sys
from db.db import DB
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import google.auth.transport.requests as google_request
import google.oauth2.credentials


httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
CLIENT_SECRETS_FILE = os.path.join(PROJECT_PATH, "credentials", "client_secret.json")
CREDENTIALS = os.path.join(PROJECT_PATH, "credentials", "google_credentials.json")

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

category = sys.argv[1]
today = datetime.date.today().strftime('%Y-%m-%d')
today_fr = datetime.date.today().strftime('%d-%m-%Y')
article_path = os.path.join(PROJECT_PATH, "data", today, f"articles_{category}_filtered.json")
youtube_video_id_path = os.path.join(PROJECT_PATH, "data", today, f"youtube_video_id_{category}.txt")




def get_authenticated_service():
    file_content = open(CREDENTIALS, "r")
    credentials_dict = json.loads(file_content.read())
    cr = google.oauth2.credentials.Credentials(**credentials_dict)
    cr.refresh(google_request.Request())
    return build(API_SERVICE_NAME, API_VERSION, credentials=cr)


def initialize_upload(youtube, options):
    tags = None
    if "keywords" in options:
        tags = options["keywords"].split(',')

    body = dict(
        snippet=dict(
            title=options["title"],
            description=options["description"],
            tags=tags,
            categoryId=options["category"]
        ),
        status=dict(
            privacyStatus=options["privacyStatus"]
        )
    )

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options["file"], chunksize=-1, resumable=True)
    )

    return resumable_upload(insert_request)


def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    return response['id']
                else:
                    exit('The upload failed with an unexpected response: %s' % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = 'A retriable error occurred: %s' % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print('Sleeping %f seconds and then retrying...' % sleep_seconds)
            time.sleep(sleep_seconds)


if __name__ == '__main__':

    db = DB()

    video = db.get(db.tables["Video"], {"format": "youtube", "category": category, "creation_date": datetime.date.today()})
    video = video[0] if len(video) > 0 else None

    if video is None:
        raise Exception("Video not found in table")
    if video.youtube_id is not None:
        raise Exception("This video already has a Youtube ID")

    upload = db.get(db.tables["Upload"], {"video_id": video.id})

    if len(upload) > 0:
        raise Exception("This video already in the upload table")

    articles = db.get_articles_of_video(video.id)

    articles_body = ""
    for i, a in enumerate(articles):
        articles_body += "Article " + str(i+1) + ": " + (str(a.url) if a.url is not None else "Oops, nous avons perdu le lien") + "\n"

    args = {
        "file": os.path.join(PROJECT_PATH, "output", today, f"highlite_{category}_youtube_{today}.mp4"),
        "title": f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le {category}",
        "description":
            f"Hɪɢʜʟɪᴛᴇ™ du {today_fr} sur le {category}\n"
            "\n"
            "Lien des articles:\n"
            "\n"
            f'{articles_body}'
            "\n"
            "Suivez-nous sur les différents réseaux:\n"
            "\n"
            "Twitter: @highlitenews\n"
            "Facebook: @highlite.news\n"
            "Instagram: @highlite.news\n"
            "Snapchat: @highlite.news\n"
            "TikTok: @highlite.news\n",
        "category": 25,
        "keywords": "highlite, highlight, news, actualités",
        "privacyStatus": "public"
    }

    youtube = get_authenticated_service()

    try:
        youtube_id = initialize_upload(youtube, args)
        if youtube_id is not None:
            video.youtube_id = youtube_id
            db.merge(video, db.tables["Video"])

            upload = {
                "video_id": video.id,
                "platform": "youtube",
                "publication_datetime": datetime.datetime.now(),
            }

            db.merge(upload, db.tables["Upload"])

        else:
            print("Error while uploading the video")
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
