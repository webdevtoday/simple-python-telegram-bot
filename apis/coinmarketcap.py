from logging import getLogger
from pathlib import Path

import requests
import json
from datetime import datetime, timezone
import dateutil.parser

logger = getLogger(__name__)


class CoinMarketCapError(Exception):
    """ Unknown error when requesting CoinMarketCap API
    """
    pass


class CoinMarketCapRequestError(CoinMarketCapError):
    """ Error on invalid request
    """


class CoinMarketCapClient(object):

    def __init__(self, api_key) -> None:
        self.base_url = "https://pro-api.coinmarketcap.com"
        self.API_KEY = api_key

    def __request(self, method, params):
        url = self.base_url + method
        headers = {"X-CMC_PRO_API_KEY": self.API_KEY}

        try:
            r = requests.get(url=url, params=params, headers=headers)
            result = r.json()
        except Exception:
            logger.exception("CoinMarketCap error")
            raise CoinMarketCapError

        if result.get("data"):
            # Successful request
            return result
        else:
            # Bad request
            logger.error("Request error: %s", result.get(
                "status").get("error_message"))
            raise CoinMarketCapRequestError

    def get_ticker(self, pair):
        params = {
            "symbol": pair[0],
            "convert": pair[1],
        }
        return self.__request(method="/v2/cryptocurrency/quotes/latest", params=params)

    def get_last_price(self, pair):
        res = self.get_ticker(pair=pair)
        return res["data"][pair[0]][0]["quote"][pair[1]]["price"]

    def get_markets_from_cache(self):
        current_date = datetime.now().strftime('%m_%Y')
        file_name = '{}.json'.format(current_date)
        file_path = Path(__file__).resolve().parent.joinpath(file_name)

        try:
            with open(file_path, 'r') as openfile:
                return json.load(openfile)
        except FileNotFoundError:
            return None

    def get_markets_set_cache(self, data):
        current_date = datetime.now().strftime('%m_%Y')
        file_name = '{}.json'.format(current_date)
        file_path = Path(__file__).resolve().parent.joinpath(file_name)

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    def get_markets(self):
        cached_data = self.get_markets_from_cache()
        if cached_data is not None:
            return cached_data

        params = {
            "limit": 5000,
        }
        data = self.__request(method="/v1/cryptocurrency/map", params=params)
        self.get_markets_set_cache(data)
        return data

    def get_all_names(self):
        """ Get a list of all possible cryptocurrencies that are traded for $
        """
        res = self.get_markets()

        for i in res['data']:
            yield i['symbol']

    def get_markets_summaries_from_cache(self):
        file_name = 'prices.json'
        file_path = Path(__file__).resolve().parent.joinpath(file_name)

        try:
            with open(file_path, 'r') as openfile:
                res = json.load(openfile)
                current_date = datetime.now(timezone.utc)
                request_date = dateutil.parser.parse(
                    res['status']['timestamp'])
                time_delta = current_date - request_date
                hour_delta = time_delta.seconds / 60 / 60

                if hour_delta > 2:
                    return None

                return res
        except FileNotFoundError:
            return None

    def get_markets_summaries_set_cache(self, data):
        file_name = 'prices.json'
        file_path = Path(__file__).resolve().parent.joinpath(file_name)

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    def get_market_summaries(self):
        cached_data = self.get_markets_summaries_from_cache()
        if cached_data is not None:
            return cached_data

        params = {
            "limit": 5000,
        }
        
        data = self.__request(
            method="/v1/cryptocurrency/listings/latest", params=params)
        self.get_markets_summaries_set_cache(data)
        return data

    def get_last_prices(self, pairs: list):
        res = self.get_market_summaries()
        for i in res['data']:
            if i['symbol'] in pairs:
                yield i['symbol'], i['quote']['USD']['price']
