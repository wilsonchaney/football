def try_parse(string):
    try:
        return float(string)
    except Exception:
        return string