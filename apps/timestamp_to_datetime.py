import datetime
import re


def parse_timestamp(timestamp):
    timestamp = str(timestamp)
    return datetime.datetime(*[int(x) for x in re.findall(r'\d+', timestamp)])
