import datetime

from collections import namedtuple
from logging import getLogger

import xmltodict
import requests


logger = getLogger(__name__)


Rate = namedtuple('Rate', 'name,rate')


def get_rates():
    session = requests.Session()

    # Request URL
    get_curl = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    # Date format: yearmonthday
    date_format = "%Y%m%d"

    # Request Date
    today = datetime.datetime.today()
    params = {
        "valcode": "USD",
        "date": today.strftime(date_format),
    }

    r = session.get(get_curl, params=params, allow_redirects=True)
    # TODO: Handle errors from API

    resp = r.text

    # TODO: Handle XML parsing errors
    data = xmltodict.parse(resp)

    # TODO: Handle JSON parsing errors
    return Rate(
        name=data["exchange"]["currency"]["cc"],
        rate=float(data["exchange"]["currency"]["rate"]),
    )


def main():
    print(get_rates())


if __name__ == '__main__':
    main()
