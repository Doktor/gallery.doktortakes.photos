import datetime


def metadata(request):
    return {
        'TITLE': "Doktor Takes Photos",
        'NAME': "Doktor",
        'TWITTER': "@DoktorTheHusky",
        'DESCRIPTION': "Photography by a blue dog.",
        'BASE_URL': "https://photos.doktorthehusky.com",
        'LAST_UPDATE': datetime.datetime(2016, 10, 10),
    }
