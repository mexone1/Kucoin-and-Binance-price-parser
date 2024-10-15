import requests


coin_k = ['BTC-USDT', 'ETH-USDT', 'ARB-USDT', 'ZRO-USDT', 'SUI-USDT']
coin_b = ['BTCUSDT', 'ETHUSDT', 'ARBUSDT', 'ZROUSDT', 'SUIUSDT']
i = 0
url_k = "https://api.kucoin.com/api/v1/market/allTickers"
url_b = "https://api.binance.com/api/v3/ticker/bookTicker"

res_b = requests.get(url_b)
res_k = requests.get(url_k)

r_b = res_b.json()
r_k = res_k.json()

token_name = ''
price_of_token_b = 0
price_of_token_k = 0


while i != len(coin_k) and len(coin_k):
    for price_b in r_b:
        sym = price_b['symbol']
        price_binance = float(price_b['askPrice'])
        if sym == coin_b[i]:
            price_of_token_b = price_binance

    for token in r_k["data"]["ticker"]:
        symbol = token["symbol"]
        price = float(token["last"])
        if symbol == coin_k[i]:
            token_name = symbol
            price_of_token_k = price



    if price_of_token_b > price_of_token_k:
        print(f'Нашел спред на монете {token_name[:3]} c Kucoin на Binance \n'
              f'Покупка: {price_of_token_k}\n'
              f'Продажа: {price_of_token_b}\n'
              f'Профит: {price_of_token_b - price_of_token_k}$')


    if price_of_token_b < price_of_token_k:
        print(f'Нашел спред на монете {token_name[:3]} c Binance на Kucoin \n'
              f'Покупка: {price_of_token_b}\n'
              f'Продажа: {price_of_token_k}\n'
              f'Профит: {price_of_token_k - price_of_token_b}$')

    i += 1

