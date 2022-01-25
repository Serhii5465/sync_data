import datetime

def get_time_now():
    """
    Function retuns current date and time.
    Unicode char (uA789) means "Modifier letter colon". For more
    information visit: https://www.fileformat.info/info/unicode/char/a789/index.htm
    :return: current date and time in string format
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S")