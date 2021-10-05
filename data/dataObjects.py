from typing import List, Generator
from .dataIO import *
from dataclasses import dataclass


@dataclass
class PriceVolume:
    price: int
    volume: float


@dataclass()
class BookEntry:
    bids: List[PriceVolume]
    asks: List[PriceVolume]
    timestamp: str
    exchange_id: str


@dataclass()
class ArbitrageEntry:
    bid: PriceVolume
    ask: PriceVolume
    bidExchangeID: str
    askExchangeID: str
    timestamp: str


def read_orders():
    orders = []
    with open('data/tradeorder.txt', 'r') as f:
        for line in f.readlines():
            order = eval(line)
            orders.append(order)
    return orders


def read_orders_generator():
    with open('data/tradeorder.txt', 'r') as f:
        for line in f.readlines():
            order = eval(line)
            yield order
