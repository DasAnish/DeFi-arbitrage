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
