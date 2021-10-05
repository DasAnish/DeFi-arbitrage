from data import *
from src import arbitrage
from asyncio import gather, get_event_loop


if __name__ == '__main__':
    tradeBook = []
    event_loop = get_event_loop()
    dataIO = DataIO(event_loop)
    while True:
        output = event_loop.run_until_complete(dataIO.get_next_entries())
        arbitrage(tradeBook, dataIO, output[0], output[1])
        arbitrage(tradeBook, dataIO, output[1], output[0])
