from typing import List, Generator
from .dataIO import *


class PriceVolume:
    def __init__(self, price=0, volume=0):
        self.price = price
        self.volume = volume


class BookEntry:
    def __init__(self):
        self.bids: List[PriceVolume] = []
        self.asks: List[PriceVolume] = []
        self.timestamp: str = ''


class Book:
    def __init__(self):
        self.entries: Generator[BookEntry] = None

    def read_book(self, filename):
        self.entries = read_in_csv(filename)


class ArbitrageEntry:
    def __init__(self):
        self.bid: PriceVolume = PriceVolume()
        self.ask: PriceVolume = PriceVolume()
        self.timestamp: str = ''


class Trades:
    def __init__(self):
        self.entries: List[ArbitrageEntry] = list()

    def add_entry(self, entry: ArbitrageEntry):
        self.entries.append(entry)
