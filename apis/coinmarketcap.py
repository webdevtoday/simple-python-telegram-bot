from logging import getLogger

import requests

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
