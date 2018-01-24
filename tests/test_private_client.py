import gdax

KEY = ""
B64SECRET = ""
PASSPHRASE = ""

client = gdax.PrivateClient(KEY, B64SECRET, PASSPHRASE,
                            api_url="https://public.sandbox.gdax.com")

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

