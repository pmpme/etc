#!/
import requests
import pdb
from datetime import datetime
from pprint import pprint

today = datetime.now().date().strftime("%m-%d-%Y")
response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
price = response.json().get('bitcoin').get('usd')

message = f"₿ ➡️  ${price:,}"
print(message)
