import datetime
import shlex
from subprocess import check_output

timestamp = check_output(shlex.split("/usr/bin/git log -1 --pretty=format:%ct"))
updated = datetime.datetime.utcfromtimestamp(int(timestamp))


def metadata(_):
    return {
        'TITLE': "Doktor Takes Photos",
        'NAME': "Doktor",
        'TWITTER': "@DoktorTheHusky",
        'DESCRIPTION': "Portrait and event photography by Doktor!",
        'BASE_URL': "https://doktortakes.photos",
        'LAST_UPDATE': updated,
    }
