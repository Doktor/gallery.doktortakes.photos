def try_parse_int(value, default):
    try:
        return int(value)
    except ValueError:
        return default
