from .dataObjects import BookEntry, PriceVolume
from typing import Generator, Tuple
import os
import sys
from asyncio import gather, get_event_loop
from pprint import pprint
from dataclasses import dataclass

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402


class DataIO:
    def __init__(self, asyncio_loop):
        exchanges_symbols = (
            ('okex', 'BTC/USDT'),
            ('binance', 'BTC/USDT'),
        )

        self.exchanges = []
        args = {'enableRateLimit': True,
                'asyncio_loop': asyncio_loop}
        for exchange_id, symbol in exchanges_symbols:
            exchange_class = getattr(ccxt, exchange_id)
            exchange = exchange_class(args)
            self.exchanges.append((exchange_id, exchange, symbol))

    @staticmethod
    async def get_orderbook(exchange_id, exchange, symbol):
        _orderbook = await exchange.fetch_order_book(symbol)

        _bids = _orderbook['bids'][:10]
        _asks = _orderbook['asks'][:10]

        bids = []
        asks = []

        for bidPrice, bidVolume in _bids:
            bid = PriceVolume(bidPrice, bidVolume)
            bids.append(bid)

        for askPrice, askVolume in _asks:
            ask = PriceVolume(askPrice, askVolume)
            asks.append(ask)

        timestamp = exchange.milliseconds()
        timestamp = exchange.iso8601(timestamp)
        bookEntry = BookEntry(bids=bids,
                              asks=asks,
                              timestamp=timestamp,
                              exchange_id=exchange_id)
        return bookEntry

    async def get_next_entries(self):
        routines = [self.get_orderbook(*args) for args in self.exchanges]
        output = await gather(*routines)
        # print(output)

        return output

    def close(self):
        for _, exchange, _ in self.exchanges:
            exchange.close()
        self.fileObj.close()

    def send_order(self, order):
        if self.fileObj is None:
            self.fileObj = open('data/tradeorder.txt', 'a')

        self.fileObj.write(str(order) + '\n')
        # with open('data/tradeorder.txt', 'a') as f:
        #     f.write(str(order) + "\n")


