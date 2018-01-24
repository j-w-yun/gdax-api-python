import gdax

PASSPHRASE = ""
KEY = ""
B64SECRET = ""

client = gdax.PrivateClient(KEY, B64SECRET, PASSPHRASE)

output = client.list_accounts()
print("list_accounts()")
print(output, "\n")

# get ID for ETH account
account_id = None
for elem in output:
    if elem['currency'] == 'BTC':
        account_id = elem['id']
        break

output = client.get_account(account_id)
print("get_account()")
print(output, "\n")

output = client.get_account_history(account_id)
print("get_account_history()")
print(output, "\n")

output = client.get_holds(account_id)
print("get_holds()")
print(output, "\n")

output = client.limit_sell(client.ETH_USD, price=1020, size=0.01)
print("limit_sell()")
print(output, "\n")

output = client.list_orders()
print("list_orders()")
print(output, "\n")

output = client.cancel_all()
print("cancel_all()")
print(output, "\n")

output = client.list_orders()
print("list_orders()")
print(output, "\n")
