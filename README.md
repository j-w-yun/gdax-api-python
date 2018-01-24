# gdax-api-python

More information about GDAX API can be found at

    https://docs.gdax.com/?python#introduction

# Dependencies

    $ pip install requests

# Usage

## Public Client

To access public client, create a MarketDataClient

    client = gdax.MarketDataClient()

Get product order book

    client.get_product_order_book(client.ETH_USD, 1)

Get product ticker

    client.get_product_ticker(client.ETH_USD)

Get trades

    client.get_trades(client.ETH_USD)

Get historic rates

    client.get_historic_rates(client.ETH_USD, "2018-01-01", "2018-01-02", granularity=300)

Get currencies

    client.get_currencies()

Get API time

    client.time()

## Authenticated Client

To access your authenticated client, create a PrivateClient

    client = gdax.PrivateClient(KEY, B64SECRET, PASSPHRASE)

List accounts

    client.list_accounts()

Get account

    client.get_account(account_id)

Get account history

    client.get_account_history(account_id)

Get holds

    client.get_holds(account_id)

Limit buy

    client.limit_buy(client.ETH_USD, price=1050, size=1)

Limit sell

    client.limit_sell(client.ETH_USD, price=3000, size=1)

_caution_ : limit buy and limit sell will not be rejected under any circumstance if post_only="True" (default) is set to "False"


Market buy

    client.market_buy(client.ETH_USD, size=1)

Market sell

    client.market_sell(client.ETH_USD, size=1)

Stop buy

    client.stop_buy(client.ETH_USD, price=1000)

Stop sell

    client.stop_sell(client.ETH_USD, price=1000)

Cancel order

    client.cancel_order(order_id)

Cancel all orders

    client.cancel_all()

List orders

    client.list_orders()

Get an order

    client.get_order(order_id)

