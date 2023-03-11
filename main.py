import os
os.system("pip install -r requirements.txt")
import aiohttp
import sys
import orjson,json
import asyncio

os.system("clear||cls")
os.system("title Crypto Notifier - Made by Auth#1337")

# /**/
# ; tutorial
# ; add your webhook in webhook.json, in webhook variable.

api = "https://api.binance.com/api/v3/ticker/price" #binance api, to get latest price
coins = ["LTC", "BTC", "SOL", "ETH"] # you can add your coins too, but in short forms only

print("[-] Crypto Price Notifier | Made By Auth#1337")

# */* Config
with open("config.json", "r") as f:
  config = json.load(f)
webhook = config.get("webhook")
delay = config.get("delay")
async def fetch_price(session, coin):
  async with session.get(api+f"?symbol={coin}USDT") as response:
    return await response.text(), response.status

async def send_log(session, content):
  payload = dict(content=content)
  async with session.post(webhook, json=payload) as response:
    assert response.status in [200,204,201], "Failed To Send Log."

def check(o,n):
  return n != o


async def main():
  async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
    cache = {}
    for coin in coins:
      price,status = await fetch_price(session, coin)
      print(price)
      price = str(orjson.loads(price)['price'])
      price_formatted = f"{float(price):.2f}"
      cache[coin] = price_formatted
    while True:
      for coin in coins:
        iprice = cache.get(coin)
        new_p, s= await fetch_price(session, coin)
        new_p = str(orjson.loads(new_p)["price"])
        snap = check(float(iprice), float(new_p))
        if snap:
          cache[coin] = str(new_p)
          try:
            if float(new_p) > float(iprice):
              now = f"{coin} Is Up."
            else:
              now = f"{coin} Is Down."
            await send_log(session, f">>> Price Updated\nCoin: {coin}\nLast Price: ${float(iprice):.2f}\nNew Price: ${float(new_p):.2f}\nNow: {now}\n\n***Crypto Price Notifer By Auth#1337***")
          except Exception as e:
            if isinstance(e, AssertionError):
              print("[-] Failed To Sent Log")
            else:
              print(f"[-] Unknown Error, {e}")
        await asyncio.sleep(delay)

 
if __name__ == "__main__":
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())
