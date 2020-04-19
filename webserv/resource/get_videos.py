from flask_restful import Resource
import traceback


class GetVideos(Resource):

    db = None

    def __init__(self, db):
        self.db = db

    def get(self):
        try:

            ret = []

            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "FOOTBALL",
                "date": "18-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com", "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })
            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "COVID-19",
                "date": "18-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })
            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "COVID-19",
                "date": "17-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })
            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "COVID-19",
                "date": "17-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })
            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "COVID-19",
                "date": "17-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })
            ret.append({
                "youtube_url": "https://www.youtube.com/embed/AQhazFDH5xU",
                "title": "Highlite COVD-19 ",
                "category": "COVID-19",
                "date": "17-04-2020",
                "publishing_date": "19h",
                "articles": [
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Deffferg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zeeeeerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                    {"title": "Degj,zezrfzefzefzefzerg", "url": "http://google.com",
                     "img": "https://media.ouest-france.fr/v1/pictures/MjAyMDA0ZWMzNjYwMWVhY2ZmMjkzMjI1OWI3YWZlNGUyMGM1YTI?width=630&amp"},
                ]
            })

        except Exception as e:
            traceback.print_exc()
            return "", "500 " + str(e)

        return ret, "200"
