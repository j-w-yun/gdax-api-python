from _socket import timeout
import base64
import hashlib
import hmac
import json
import time

import requests
from requests.auth import AuthBase

from gdax.coinbase_exchange_auth import CoinbaseExchangeAuth


class PrivateClient():

    def __init__(self, key, b64secret, passphrase, api_url="https://api.gdax.com", timeout=30):
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
        return r.json()

