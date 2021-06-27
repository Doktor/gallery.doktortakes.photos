class MD5HashConverter:
    regex = '[a-f0-9]{32}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
