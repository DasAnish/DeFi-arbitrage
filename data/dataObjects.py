from typing import List, Generator
from .dataIO import *
from dataclasses import dataclass


@dataclass
class PriceVolume:
    price: int
    volume: float


@dataclass
class BookEntry:
    bids: List[PriceVolume]
    asks: List[PriceVolume]
    timestamp: str
    exchange_id: str
    # def __init__(self):
    #     self.bids: List[PriceVolume] = []
    #     self.asks: List[PriceVolume] = []
    #     self.timestamp: str = ''


@dataclass()
class ArbitrageEntry:
    bid: PriceVolume
    ask: PriceVolume
    timestamp: str
    # def __init__(self):
    #     self.bid: PriceVolume = PriceVolume()
    #     self.ask: PriceVolume = PriceVolume()
    #     self.timestamp: str = ''


class Trades:
    def __init__(self):
        self._entries: List[ArbitrageEntry] = list()

    def add_entry(self, entry: ArbitrageEntry):
        self._entries.append(entry)

    def write_out_trades(self):
        pass
