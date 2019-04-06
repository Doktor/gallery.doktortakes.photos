import re

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]+$')


def is_valid_username(username):
    return USERNAME_REGEX.match(username)
