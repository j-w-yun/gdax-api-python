import requests


class PublicClient(object):
    """GDAX public client API for market data
    
    The Market Data API is an unauthenticated set of endpoints for retrieving
    market data. These endpoints provide snapshots of market data.
    """

    # List of products offered as of 1/31/2018.
    BTC_USD = "BTC-USD"
    BCH_BTC = "BCH-BTC"
    BCH_USD = "BCH-USD"
    BCH_EUR = "BCH-EUR"
    BTC_EUR = "BTC-EUR"
    BTC_GBP = "BTC-GBP"
    BTC_USD = "BTC-USD"
    ETH_BTC = "ETH-BTC"
    ETH_EUR = "ETH-EUR"
    ETH_USD = "ETH-USD"
    LTC_BTC = "LTC-BTC"
    LTC_EUR = "LTC-EUR"
    LTC_USD = "LTC-USD"

    def __init__(self, api_url='https://api.gdax.com', timeout=30):
        """Create GDAX API public client.
        Args:
            api_url (Optional[str]): API URL.
        """
        self.url = api_url.rstrip('/')
        self.timeout = timeout

    def _get(self, path, params=None):
        """Perform a get request
        Args:
            path: Command path
            params (Optional{[str]}): Set of parameters
        Returns:
            dictionary: Output from the get request
        """
        r = requests.get(self.url + path, params=params, timeout=self.timeout)
        return r.json()

    def get_products(self):
        """Get a list of available currency pairs for trading.
        Returns:
            list: A list of available currency pairs for trading. Example
                response::
                [
                    {
                        "id": "BTC-USD",
                        "base_currency": "BTC",
                        "quote_currency": "USD",
                        "base_min_size": "0.01",
                        "base_max_size": "10000.00",
                        "quote_increment": "0.01"
                    }
                ]
        """
        return self._get('/products')

    def get_product_order_book(self, product_id, level=1):
        """Get a list of open orders for a product. The amount of detail shown 
        can be customized with the level parameter.
        Args:
            product_id (str): ID of the product
            level (Optional[int]): Level of the order book depth. Default is 1.
                level 1: Only the best bid and ask (aggregated)
                level 2: Top 50 bids and asks (aggregates)
                level 3: Full order book (non aggregated)
                
        Returns:
            dict: A dictionary of order books. Example response for level 1::
                {
                    "sequence": "3",
                    "bids": [
                        [ price, size, num-orders ],
                    ],
                    "asks": [
                        [price, size, num-orders ],
                    ]
                }
        """
        assert level in range(1, 4)
        return self._get('/products/{}/book'.format(str(product_id)),
                         params={'level': level})

    def get_product_ticker(self, product_id):
        """Snapshot information about the last trade (tick), best bid/ask and
        24h volume. Polling is discouraged in favor of connecting via the
        websocket stream and listening for match messages.
        Args:
            product_id (str): ID of the product
        Returns:
            dict: A dictionary of product ticker. Example response::
                {
                    "trade_id": 4729088,
                    "price": "333.99",
                    "size": "0.193",
                    "bid": "333.98",
                    "ask": "333.99",
                    "volume": "5957.11914015",
                    "time": "2015-11-14T20:46:03.511254Z"
                }
        """
        return self._get('/products/{}/ticker'.format(str(product_id)))

    def get_trades(self, product_id):
        """List the latest trades for a product
        Args:
            product_id (str): ID of the product
        Returns:
            list: A list of latest trades. Example response::
                [{
                    "time": "2014-11-07T22:19:28.578544Z",
                    "trade_id": 74,
                    "price": "10.00000000",
                    "size": "0.01000000",
                    "side": "buy"
                }, {
                    "time": "2014-11-07T01:08:43.642366Z",
                    "trade_id": 73,
                    "price": "100.00000000",
                    "size": "0.01000000",
                    "side": "sell"
                }]
        """
        return self._get('/products/{}/trades'.format(str(product_id)))

    def get_historic_rates(self, product_id, start=None, end=None,
                           granularity=None):
        """Historic rates for a product. Rates are returned in grouped buckets
        based on requested granularity.
        Args:
            product_id (str): ID of the product
            start (Optional[str]): Start time in ISO 8601
            end (Optional[str]): End time in ISO 8601
            granularity (Optional[str]): Desired timeslice in seconds. Must be
                one of the following values: {60, 300, 900, 3600, 21600, 86400}
        Returns:
            list: A list of historic data in candle format. Example response::
                [
                    [ time, low, high, open, close, volume ],
                    [ 1415398768, 0.32, 4.2, 0.35, 4.2, 12.3 ],
                    ...
                ]
        """
        assert granularity is None or str(granularity) in ["60", "300", "900",
                                                           "3600", "21600",
                                                           "86400"]
        params = {}
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if granularity is not None:
            params['granularity'] = granularity
        return self._get('/products/{}/candles'.format(str(product_id)),
                         params=params)

    def get_24hr_stats(self, product_id):
        """Get 24hr stats for the product. Volume is in base currency units.
        Open, high, low are in quote currency units.
        Args:
            product_id (str): ID of the product
        Returns:
            dict: A dictionary of 24hr stats. Example response::
                {
                    "open": "34.19000000",
                    "high": "95.70000000",
                    "low": "7.06000000",
                    "volume": "2.41000000"
                }
        """
        return self._get('/products/{}/stats/'.format(str(product_id)))

    def get_currencies(self):
        """List known currencies
        Returns:
            list: A list of known currencies. Example response::
                [{
                    "id": "BTC",
                    "name": "Bitcoin",
                    "min_size": "0.00000001"
                }, {
                    "id": "USD",
                    "name": "United States Dollar",
                    "min_size": "0.01000000"
                }]
        """
        return self._get('/currencies')

    def time(self):
        """Get the API server time.
        Returns:
            dict: Information on API server time. Example response::
                {
                    "iso": "2015-01-07T23:47:25.201Z",
                    "epoch": 1420674445.201
                }
        """
        return self._get('/time')
