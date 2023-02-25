import json
import os
from typing import List

from loguru import logger
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from alert.model.token import Token


class CryptoService():
    parameters = {
        'start':'1',
        'limit':'5000',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        #'X-CMC_PRO_API_KEY': os.getenv('X_CMC_PRO_API_KEY_TEST', 'YOUR_TEST_API_KEY'), # Only for Test
        'X-CMC_PRO_API_KEY': os.getenv('X_CMC_PRO_API_KEY', 'YOUR_API_KEY'),
    }
    watchlist = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'XRP', 'LINK', 'LTC', 'MATIC', 'BCH', 'XLM', 'FTM', 'ONE', 'HOT', 'CELR', 'TOMO', 'FORTH', 'BEAM']

    threshold_for_buy = 10 # Percentage %
    threshold_for_sell = 20 # Percentage %

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers.update(self.headers)

    def get_listings(self):

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        #url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' # Only for Test
        try:
            response = self.session.get(url, params=self.parameters)
            data = json.loads(response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            logger.debug(e)

    def extract_data(self):
        raw_data = self.get_listings()
        data = raw_data['data']
        result = [Token(**{
                            'name':token['name'],
                            'symbol':token['symbol'],
                            'price':token['quote']['USD']['price'],
                            'percent_change_1h': token['quote']['USD']['percent_change_1h'],
                            'percent_change_24h': token['quote']['USD']['percent_change_24h'],
                            'percent_change_7d': token['quote']['USD']['percent_change_7d'],
                        }) for token in data if token['symbol'] in self.watchlist]
        return result

    def get_buy_list(self, tokens_list:List[Token]):
        result = []
        for token in tokens_list:
            if token.percent_change_1h < -1*self.threshold_for_buy or \
                token.percent_change_24h < -1*self.threshold_for_buy or \
                    token.percent_change_7d < -1*self.threshold_for_buy:
                result.append(token)
        return result

    def get_sell_list(self, tokens_list:List[Token]):
        result = []
        for token in tokens_list:
            if token.percent_change_1h > self.threshold_for_sell or \
                token.percent_change_24h > self.threshold_for_sell or \
                    token.percent_change_7d > self.threshold_for_sell:
                result.append(token)
        return result

    def get_filtered_tokens(self)->List[Token]:
        all_tokens = self.extract_data()
        result = self.get_buy_list(all_tokens) + self.get_sell_list(all_tokens)
        return result
