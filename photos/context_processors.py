import datetime


def metadata(request):
    return {
        'TITLE': "Doktor Takes Photos",
        'NAME': "Doktor",
        'TWITTER': "@DoktorTheHusky",
        'DESCRIPTION': "Photos by Doktor",
        'BASE_URL': "https://doktortakes.photos",
        'LAST_UPDATE': datetime.datetime(2017, 10, 18),
    }
