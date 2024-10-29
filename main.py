
import requests
import asyncio
import json
from aiohttp import ClientSession

class BinanceKucoinParser:
    def __init__(self, binance_data=None, kucoin_data=None, binance_lst=None, kucoin_lst=None,
                 tickers_binance=None,tickers_kucoin=None):
        self.binance_data = binance_data
        self.kucoin_data = kucoin_data
        self.binance_lst = binance_lst
        self.kucoin_lst = kucoin_lst
        self.tickers_kucoin = tickers_kucoin
        self.tickers_binance = tickers_binance


    async def pars_binance(self):
        async with ClientSession() as session:
            url = "https://api.binance.com/api/v3/ticker/bookTicker"

            try:
                async with session.get(url=url) as responce:
                    self.binance_data = await responce.json()
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    async def pars_kucoin(self):
        async with ClientSession() as session:
            url = "https://api.kucoin.com/api/v1/market/allTickers"

            try:
                async with session.get(url=url) as responce:
                    self.kucoin_data = await responce.json()
            except Exception as e:
                print(f'Произошла ошибка: {e}')

    async def sorting(self):
        self.tickers_binance = ['BTCUSDT', 'ETHUSDT', 'ARBUSDT', 'ZROUSDT', 'SUIUSDT']
        self.tickers_kucoin = ['BTC-USDT', 'ETH-USDT', 'ARB-USDT', 'ZRO-USDT', 'SUI-USDT']
        self.binance_lst = []
        self.kucoin_lst = []
        token_index = 0

        while token_index != len(self.tickers_kucoin):
            for token_b in self.binance_data:
                if dict(token_b)['symbol'] == self.tickers_binance[token_index]:
                    ticker_binance = dict(token_b)['symbol']
                    price_of_ticker_binance = float(dict(token_b)['askPrice'])
                    self.binance_lst.append({ticker_binance: price_of_ticker_binance})

            for token_k in self.kucoin_data["data"]["ticker"]:
                if dict(token_k)["symbol"] == self.tickers_kucoin[token_index]:
                    ticker_kucoin = dict(token_k)["symbol"]
                    price_of_ticker_kucoin = float(dict(token_k)["last"])
                    self.kucoin_lst.append({ticker_kucoin: price_of_ticker_kucoin})
            token_index += 1


    async def comparison(self):
        stop = 0
        res_b_lst = []
        res_k_lst = []
        while stop != len(self.binance_lst):
            for token_b in self.binance_lst:
                for res_b in dict(token_b).values():
                    res_b_lst.append(res_b)

            for token_k in self.kucoin_lst:
                for res_k in dict(token_k).values():
                    res_k_lst.append(res_k)

            if res_k_lst[stop] > res_b_lst[stop]:
                print(f'Нашел спред на паре {self.tickers_kucoin[stop]} c Kucoin на Binance \n'
                      f'Покупка: {res_b_lst[stop]}$ \n'
                      f'Продажа: {res_k_lst[stop]}$ \n'
                      f'Профит: {res_k_lst[stop]-res_b_lst[stop]}$')

            elif res_k_lst[stop] < res_b_lst[stop]:
                print(f'Нашел спред на паре {self.tickers_kucoin[stop]} c Binance на Kucoin \n'
                      f'Покупка: {res_k_lst[stop]}$ \n'
                      f'Продажа: {res_b_lst[stop]}$ \n'
                      f'Профит: {res_b_lst[stop]-res_k_lst[stop]}$')
            stop += 1


    async def main(self):
        task1 = asyncio.create_task(BinanceKucoinParser.pars_binance(self))
        task2 = asyncio.create_task(BinanceKucoinParser.pars_kucoin(self))
        await  asyncio.gather(task1, task2)
        await self.sorting()
        await self.comparison()

parser = BinanceKucoinParser()
asyncio.run(parser.main())
