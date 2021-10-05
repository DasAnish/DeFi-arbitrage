from data import *
from asyncio import gather, get_event_loop, wait

def writeOutTrades(trade):
    tradeBook.add_entry()


# entry1 is hb, entry2 is bnc
def arbitrage(entry1, entry2):
    idx_bid = 0
    idx_ask = 10
    order = ArbitrageEntry()
    order.bidExchangeID = entry1.exchangeID
    order.askExchangeID = entry2.exchangeID
    order.timestamp = entry1.timestamp
    # buying entry2 selling entry1
    while (idx_bid < 10) and (idx_ask < 20):
        if entry1[idx_bid].price > entry2[idx_ask].price:
            volume = min(entry1[idx_bid].volume, entry2[idx_ask].volume)
            order.bid = PriceVolume(entry1[idx_bid].price, volume)
            order.ask = PriceVolume(entry2[idx_ask].price, volume)
            # need to execute trade/send to IO, below is add to trade book
            tradeBook.add_entry(order)
            entry1[idx_bid].volume -= volume
            entry2[idx_ask].volume -= volume
            if entry1[idx_bid].volume == 0:
                idx_bid += 1
            if entry2[idx_ask].volume == 0:
                idx_ask += 1
        # if no more arbitrage opportunities
        elif entry1[idx_bid].price <= entry2[idx_ask].price:
            break


if __name__ == '__main__':
    tradeBook = Trades
    # call IO
    # send trades
    pass
    event_loop = get_event_loop()
    dataIO = DataIO(event_loop)
    while True:
        output = event_loop.run_until_complete(dataIO.get_next_entries())
    # results = event_loop.run_until_complete(dataIO.get_next_entries())
    # print(results)
    # dataIO.close()