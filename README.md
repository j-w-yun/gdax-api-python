# gdax-api-python

More information can be found at:

    https://docs.gdax.com/

## Dependencies

If you are installing gdax-api with native pip, skip this step.

    $ pip install requests

## Install

#### Installing with native pip

    $ pip install gdax-api

#### Validate your installation

Start a terminal.

Invoke python from your shell as follows:

    $ python

Enter the following short program inside the python interactive shell:

    >>> import gdax
    >>> client = gdax.PublicClient()
    >>> print(client.get_currencies())

If the system outputs a JSON response from GDAX, then you are ready to begin using gdax-api in your programs.

## Usage

#### Public Client

To access the public client, create a PublicClient

    client = gdax.PublicClient()

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

#### Authenticated Client

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

## Donations

ETH: `0x1111111113dfd50282276F1D165E0F4f35Dd6Fd5`

## License

MIT. See LICENSE for details.