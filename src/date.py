import datetime


def get_time_now() -> str:
    """
    The function returns the current date and time with the uA789 delimiter.
    Unicode char (uA789) means "Modifier letter colon". For more
    information visit: https://www.fileformat.info/info/unicode/char/a789/index.htm
    Returns:
        А formatted string with the current time.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S")
