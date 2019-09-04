import datetime
import math

import requests_cache
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.commonresponses import DOWNSTREAM_ERROR_RESPONSE
from api.modules.holidays.constants import HOLIDAYS_PAGE_URL, HINDI_DAY_STRING_MAP, HINDI_MONTH_STRING_MAP
from api.modules.holidays.utils import load_url_content

week_difference = datetime.timedelta(days=30)
requests_cache.install_cache(expire_after=week_difference)


@api_view(['GET'])
def get_upcoming_holidays(request, year):
    """
    Returns a list of all the holidays in a given year
    :param request:
    :param year:
    :return: 400 if unable to get response from Holidays Page
    :return: 503 if unable to correctly parse Holidays Page
    :return: 200 successful
    """
    holiday_data = []
    try:
        html = load_url_content(HOLIDAYS_PAGE_URL.format(year))
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            cells = soup.findAll(['th', 'td'])
            row_len = int(math.ceil(len(cells) / 4))
            for ctr in range(row_len):
                if ctr == 0:
                    continue

                offset = ctr * 4
                holiday_type = cells[offset + 3].text.split()
                date_string = cells[offset + 0].text.strip().split(" ")
                day_string = cells[offset + 1].text.strip()

                # Check if HTML response is in Hindi
                # If in Hindi, replace with English counterpart
                if date_string[1] in HINDI_MONTH_STRING_MAP.keys():
                    date_string[1] = HINDI_MONTH_STRING_MAP[date_string[1]][:3]
                    day_string = HINDI_DAY_STRING_MAP[day_string]

                try:
                    dt = datetime.datetime.strptime(" ".join(date_string), '%d %b')
                except ValueError:
                    dt = datetime.datetime.strptime(" ".join(date_string), '%b %d')

                holiday_obj = {
                    'month': dt.strftime('%B'),
                    'date': int(dt.strftime('%d')),
                    'day': day_string,
                    'name': cells[offset + 2].text.strip(),
                    'type': holiday_type[0]
                }

                holiday_data.append(holiday_obj)
        else:
            return Response([], status=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return DOWNSTREAM_ERROR_RESPONSE

    return Response(holiday_data, status=status.HTTP_200_OK)
