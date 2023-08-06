from datetime import datetime


def from_datetime_to_time(date):
    was = date.split("T")
    was = " ".join(was)
    was = was[:19]
    date_time_obj = datetime.strptime(was, '%Y-%m-%d %H:%M:%S')
    was = date_time_obj - datetime(1970, 1, 1)
    return was.total_seconds() - 3600 * 3

def now():
    today = datetime.utcnow()
    dt = today - datetime(1970, 1, 1)
    return dt.total_seconds()
