import json

import requests

from gdax.coinbase_exchange_auth import CoinbaseExchangeAuth
from gdax.public_client import PublicClient


class PrivateClient(PublicClient):
    """Authenticated client for accessing GDAX accounts. requires passphrase,
    key, and b64secret key to access your accounts.
    """

    def __init__(self, key, b64secret, passphrase,
                 api_url="https://api.gdax.com", timeout=30):
        self.url = api_url.rstrip('/')
        self.timeout = timeout
        self.auth = CoinbaseExchangeAuth(key, b64secret, passphrase)

    def list_accounts(self):
        """Get a list of trading accounts
        Returns:
            list: A list of trading accounts. Example response::
                [
                    {
                        "id": "71452118-efc7-4cc4-8780-a5e22d4baa53",
                        "currency": "BTC",
                        "balance": "0.0000000000000000",
                        "available": "0.0000000000000000",
                        "hold": "0.0000000000000000",
                        "profile_id": "75da88c5-05bf-4f54-bc85-5c775bd68254"
                    }, {
                        "id": "e316cb9a-0808-4fd7-8914-97829c1925de",
                        "currency": "USD",
                        "balance": "80.2301373066930000",
                        "available": "79.2266348066930000",
                        "hold": "1.0035025000000000",
                        "profile_id": "75da88c5-05bf-4f54-bc85-5c775bd68254"
                    }
                ]
        """

        r = requests.get(self.url + '/accounts', auth=self.auth,
                         timeout=self.timeout)
        return r.json()

    def get_account(self, account_id):
        """Information for a single account. Use this endpoint when you know
        the account_id.
        Args:
            account_id (str): ID of the account
        Returns:
            dict: Information about the account. Example response::
                {
                    "id": "a1b2c3d4",
                    "balance": "1.100",
                    "holds": "0.100",
                    "available": "1.00",
                    "currency": "USD"
                }
        """
        r = requests.get(self.url + '/accounts/' + account_id, auth=self.auth,
                         timeout=self.timeout)
        return r.json()

    def get_account_history(self, account_id):
        """List account activity. Account activity either increases or decreases
        your account balance. Items are paginated and sorted latest first.
        Args:
            account_id (str): ID of the account
        Returns:
            list: A list of account activity. Example response::
                [
                    {
                        "id": "100",
                        "created_at": "2014-11-07T08:19:27.028459Z",
                        "amount": "0.001",
                        "balance": "239.669",
                        "type": "fee",
                        "details": {
                            "order_id": "d50ec984-77a8-460a-b958-66f114b0de9b",
                            "trade_id": "74",
                            "product_id": "BTC-USD"
                        }
                    }
                ]
        """
        r = requests.get(self.url +
                         '/accounts/{}/ledger'.format(str(account_id)),
                         auth=self.auth, timeout=self.timeout)
        # TODO: pagination
        return r.json()

    def get_holds(self, account_id):
        """Holds are placed on an account for any active orders or pending
        withdraw requensts. As an order is filled, the hold amount is updated.
        If an order is canceled, any remaining hold is removed. For a withdraw,
        once it is completed, the hold is removed.
        Args:
            account_id (str): ID of the account
        Returns:
            list: A list of account holds. Example response::
                [
                    {
                        "id": "82dcd140-c3c7-4507-8de4-2c529cd1a28f",
                        "account_id": "e0b3f39a-183d-453e-b754-0c13e5bab0b3",
                        "created_at": "2014-11-06T10:34:47.123456Z",
                        "updated_at": "2014-11-06T10:40:47.123456Z",
                        "amount": "4.23",
                        "type": "order",
                        "ref": "0a205de4-dd35-4370-a285-fe8fc375a273",
                    }
                ]
        """
        r = requests.get(self.url +
                         '/accounts/{}/holds'.format(str(account_id)),
                         auth=self.auth, timeout=self.timeout)
        # TODO: pagination
        return r.json()

    def _order(self, **kwargs):
        """You can place different orders: limit, market, and stop. Orders can
        only be placed if your account has sufficient funds. Once an order is
        placed, your account funds will be put on hold for the duration of the
        order. How much and which funds are put on hold depends on the order
        type and parameters specified.
        
        """
        return requests.post(self.url + '/orders', data=json.dumps(kwargs),
                          auth=self.auth, timeout=self.timeout)

    def limit_buy(self, product_id, price, size, client_oid=None, stp=None,
                  time_in_force="GTC", cancel_after=None, post_only="True"):
        """Place a limit buy order.
        Args:
            product_id (str): ID of the product
            price (str): price in base currency
            size (str): Amount of product to order
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
            time_in_force (Optional[str]): GTC, GTT, IOC, or FOk (default is
                GTC)
            cancel_after (Optional[str]): min, hour, day. Requires
                time_in_force to be GTT
            post_only (Optional[str]): Post only flag. Invalid when
                time_in_force is IOC or FOK
        Returns:
            dict: Limit buy result
        """
        param = {}
        param["side"] = "buy"
        param["type"] = "limit"
        param["product_id"] = product_id
        param["price"] = price
        param["size"] = size
        param["time_in_force"] = time_in_force

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp
        if cancel_after is not None:
            param["cancel_after"] = cancel_after
        if post_only is not None:
            param["post_only"] = post_only

        r = self._order(**param)
        return r.json()

    def limit_sell(self, product_id, price, size, client_oid=None, stp=None,
                   time_in_force="GTC", cancel_after=None, post_only="True"):
        """Place a limit sell order.
        Args:
            product_id (str): ID of the product
            price (str): price in base currency
            size (str): Amount of product to order
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
            time_in_force (Optional[str]): GTC, GTT, IOC, or FOk (default is
                GTC)
            cancel_after (Optional[str]): min, hour, day. Requires
                time_in_force to be GTT
            post_only (Optional[str]): Post only flag. Invalid when
                time_in_force is IOC or FOK
        Returns:
            dict: Limit sell result
        """
        param = {}
        param["side"] = "sell"
        param["type"] = "limit"
        param["product_id"] = product_id
        param["price"] = price
        param["size"] = size
        param["time_in_force"] = time_in_force

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp
        if cancel_after is not None:
            param["cancel_after"] = cancel_after
        if post_only is not None:
            param["post_only"] = post_only

        r = self._order(**param)
        return r.json()

    def market_buy(self, product_id, size=None, funds=None, client_oid=None,
                   stp=None):
        """Place a market buy order.
        Args:
            product_id (str): ID of the product
            size (str): Desired amount in BTC. Funds does not need to be
                specified if size is specified
            funds (str): Desired amout of quote currency to use. Size does not
                need to be specified if funds is specified
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
        Returns:
            dict: Market buy result
        """
        param = {}
        param["side"] = "buy"
        param["type"] = "market"
        param["product_id"] = product_id

        if size is not None:
            param["size"] = size
        else:
            assert funds is not None
            param["funds"] = funds

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp

        r = self._order(**param)
        return r.json()

    def market_sell(self, product_id, size=None, funds=None, client_oid=None,
                    stp=None):
        """Place a market sell order.
        Args:
            product_id (str): ID of the product
            size (str): Desired amount in BTC. Funds does not need to be
                specified if size is specified
            funds (str): Desired amout of quote currency to use. Size does not
                need to be specified if funds is specified
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
        Returns:
            dict: Market sell result
        """
        param = {}
        param["side"] = "sell"
        param["type"] = "market"
        param["product_id"] = product_id

        if size is not None:
            param["size"] = size
        else:
            assert funds is not None
            param["funds"] = funds

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp

        r = self._order(**param)
        return r.json()

    def stop_buy(self, product_id, price, size=None, funds=None,
                 client_oid=None, stp=None):
        """Place a stop buy order.
        Args:
            product_id (str): ID of the product
            price (str): Desired price at which the stop order triggers
            size (str): Desired amount in BTC. Funds does not need to be
                specified if size is specified
            funds (str): Desired amout of quote currency to use. Size does not
                need to be specified if funds is specified
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
        """
        param = {}
        param["side"] = "buy"
        param["type"] = "stop"
        param["product_id"] = product_id
        param["price"] = price

        if size is not None:
            param["size"] = size
        else:
            assert funds is not None
            param["funds"] = funds

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp

        r = self._order(**param)
        return r.json()

    def stop_sell(self, product_id, price, size=None, funds=None,
                  client_oid=None, stp=None):
        """Place a stop sell order.
        Args:
            product_id (str): ID of the product
            price (str): Desired price at which the stop order triggers
            size (str): Desired amount in BTC. Funds does not need to be
                specified if size is specified
            funds (str): Desired amout of quote currency to use. Size does not
                need to be specified if funds is specified
            client_oid (Optional[str]): Order ID selected by you to identify
                your order
            stp (Optional[str]): Self-trade=prevention flag
        """
        param = {}
        param["side"] = "sell"
        param["type"] = "stop"
        param["product_id"] = product_id
        param["price"] = price

        if size is not None:
            param["size"] = size
        else:
            assert funds is not None
            param["funds"] = funds

        if client_oid is not None:
            param["client_oid"] = client_oid
        if stp is not None:
            param["stp"] = stp

        r = self._order(**param)
        return r.json()

    def cancel_order(self, order_id):
        """Cancel a previously placed order.
        Args:
            order_id (str): ID of the order previously placed
        """
        r = requests.delete(self.url + '/orders/' + order_id, auth=self.auth,
                            timeout=self.timeout)
        return r.json()

    def cancel_all(self, product_id=None):
        """With best effort, cancel all open orders. The response is a list of
        ids of the canceled orders.
        Args:
            product_id (Optional[str]): Only cancel orders open for a specific
                product
        Returns:
            list: A list of ids of the canceled orders
        """
        url = self.url + '/orders/'
        if product_id is not None:
            url += "?product_id={}&".format(str(product_id))
        r = requests.delete(url, auth=self.auth, timeout=self.timeout)
        return r.json()

    def list_orders(self, product_id=None, status=[]):
        """List your current open orders. Only open or un-settled orders are
        returned. As soon as an order is no longer open and settled, it will no
        longer appear in the default request.
        Args:
            status (Optional[list]): Limit list of orders to these statuses
                [open, pending, active]. Passing all returns orders of all
                statuses.
            product_id (Optional[str]): Only list orders for a specific product
        Returns:
            list: Information about all your current open orders. Example
                response::
                [
                    {
                        "id": "d0c5340b-6d6c-49d9-b567-48c4bfca13d2",
                        "price": "0.10000000",
                        "size": "0.01000000",
                        "product_id": "BTC-USD",
                        "side": "buy",
                        "stp": "dc",
                        "type": "limit",
                        "time_in_force": "GTC",
                        "post_only": false,
                        "created_at": "2016-12-08T20:02:28.53864Z",
                        "fill_fees": "0.0000000000000000",
                        "filled_size": "0.00000000",
                        "executed_value": "0.0000000000000000",
                        "status": "open",
                        "settled": false
                    }, {
                        "id": "8b99b139-58f2-4ab2-8e7a-c11c846e3022",
                        "price": "1.00000000",
                        "size": "1.00000000",
                        "product_id": "BTC-USD",
                        "side": "buy",
                        "stp": "dc",
                        "type": "limit",
                        "time_in_force": "GTC",
                        "post_only": false,
                        "created_at": "2016-12-08T20:01:19.038644Z",
                        "fill_fees": "0.0000000000000000",
                        "filled_size": "0.00000000",
                        "executed_value": "0.0000000000000000",
                        "status": "open",
                        "settled": false
                    }
                ]
        """
        url = self.url + "/orders"
        params = {}
        if product_id is not None:
            params["product_id"] = product_id
        if status:
            params["status"] = status
        # TODO: paginate
        r = requests.get(url, auth=self.auth, params=params, timeout=self.timeout)
        return r.json()

    def get_order(self, order_id):
        """Get a single order by order ID.
        Args:
            order_id (str): ID of your order
        Returns:
            dict: Information about the order. Example response::
                {
                    "id": "68e6a28f-ae28-4788-8d4f-5ab4e5e5ae08",
                    "size": "1.00000000",
                    "product_id": "BTC-USD",
                    "side": "buy",
                    "stp": "dc",
                    "funds": "9.9750623400000000",
                    "specified_funds": "10.0000000000000000",
                    "type": "market",
                    "post_only": false,
                    "created_at": "2016-12-08T20:09:05.508883Z",
                    "done_at": "2016-12-08T20:09:05.527Z",
                    "done_reason": "filled",
                    "fill_fees": "0.0249376391550000",
                    "filled_size": "0.01291771",
                    "executed_value": "9.9750556620000000",
                    "status": "done",
                    "settled": true
                }
        """
        r = requests.get(self.url + '/orders/' + order_id, auth=self.auth,
                         timeout=self.timeout)
        return r.json()
