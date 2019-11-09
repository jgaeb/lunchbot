from datetime import date, timedelta
import re

def last_sunday():
    day_diff = (date.today().weekday() + 1) % 7
    return date.today() - timedelta(days = day_diff)

def extract_url(string):
    result = re.search(r"https://[^\"]+", string)
    return result.group() if result else None
