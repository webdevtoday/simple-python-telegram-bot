from apis.coinmarketcap import CoinMarketCapClient


class Searcher:

    def __init__(self):
        # Get a list of available currencies
        self.coinmarketcap = CoinMarketCapClient('<API_KEY>')
        self.names = list(self.coinmarketcap.get_all_names())

    def parse_query(self, text: str) -> list:
        """ Understand what the user is asking for
        """
        val = text.upper().strip()
        # TODO: fuzzy search
        return [name for name in self.names if val in name]

    def get_prices(self, names: list) -> list:
        """ Get a list of prices for the requested currencies
        """
        for (name, price) in self.coinmarketcap.get_last_prices(pairs=names):
            yield name, price
