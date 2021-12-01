import datetime
import random


def metadata(_):
    return {
        'TITLE': "Doktor Takes Photos",
        'NAME': "Doktor",
        'TWITTER': "@DoktorTheHusky",
        'DESCRIPTION': "Portrait and event photography by Doktor!",
        'BASE_URL': "https://doktortakes.photos",
        'LAST_UPDATE': datetime.datetime.utcnow(),
    }
