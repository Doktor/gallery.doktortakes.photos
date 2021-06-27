import datetime
import random

from photos.settings_photos import TAGLINES


def metadata(_):
    return {
        'TITLE': "Doktor Takes Photos",
        'NAME': "Doktor",
        'TWITTER': "@DoktorTheHusky",
        'DESCRIPTION': "Portrait and event photography by Doktor!",
        'BASE_URL': "https://doktortakes.photos",
        'LAST_UPDATE': datetime.datetime.utcnow(),
        'TAGLINE': random.choice(TAGLINES),
    }
