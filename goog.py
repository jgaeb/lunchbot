from datetime import date
from json import loads
from random import choice
import os

from requests import get

from .utils import last_sunday, extract_url

API_ENDPOINT = ("https://sheets.googleapis.com/v4/spreadsheets"
        "/{sheet_id}/values/{range_}"
        "?key={key}&valueRenderOption=FORMULA"
        "&dateTimeRenderOption=SERIAL_NUMBER"
)
SHEET_ID = "1pJ8NdaQ8SMGVoDWx6SGKMhonkFY7s6wyYjgi-w6DEsE"
API_KEY = os.environ.get('GOOGLE_API_KEY')
DATE_OFFSET = date(1899, 12, 30).toordinal()

def get_current_dictator():
    values = loads(get(API_ENDPOINT.format(
        sheet_id=SHEET_ID,
        range_="Schedule!A:F",
        key=API_KEY
    )).content)["values"]
    headers = values.pop(0)
    for row in values:
        if date.fromordinal(row[0] + DATE_OFFSET) == last_sunday():
            return Dictator(**{head:item for head, item in zip(headers, row)})

class Dictator():
    def __init__(self, week, name, **kwargs):
        self.name = name
        self.week = date.fromordinal(week + DATE_OFFSET)
        for key in ["monday", "monday_vegan", "thursday", "thursday_vegan"]:
            if key in kwargs:
                setattr(self, key, extract_url(kwargs[key]) if kwargs[key] else
                        None)
            else:
                setattr(self, key, None)

    def get_random_rest(self, vegan=False):
        values = loads(get(API_ENDPOINT.format(
            sheet_id=SHEET_ID,
            range_="Restaurants and ratings!A:H",
            key=API_KEY
        )).content)["values"]
        headers = values.pop(0)
        if vegan:
            # NOTE: Expects that vegan / not vegan in Column C.
            values = [row for row in values if len(row) > 2 if row[2]]
        val = choice(values)
        return val[1]
