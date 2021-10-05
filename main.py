from data import *
from asyncio import gather, get_event_loop


# entry1 is hb, entry2 is bnc
def arbitrage(tradebook, dataIO, entry1, entry2):
    idx_bid = 0
    idx_ask = 0
    order = ArbitrageEntry(*([None]*5))
    order.bidExchangeID = entry1.exchange_id
    order.askExchangeID = entry2.exchange_id
    order.timestamp = entry1.timestamp
    # buying entry2 selling entry1
    while (idx_bid < 10) and (idx_ask < 10):
        if entry1.bids[idx_bid].price > entry2.asks[idx_ask].price:
            volume = min(entry1.bids[idx_bid].volume, entry2.asks[idx_ask].volume)
            order.bid = PriceVolume(entry1.bids[idx_bid].price, volume)
            order.ask = PriceVolume(entry2.asks[idx_ask].price, volume)
            dataIO.send_order(order)
            tradebook.append(order)
            entry1.bids[idx_bid].volume -= volume
            entry2.asks[idx_ask].volume -= volume
            if entry1.bids[idx_bid].volume == 0:
                idx_bid += 1
            if entry2.asks[idx_ask].volume == 0:
                idx_ask += 1
        # if no more arbitrage opportunities
        elif entry1.bids[idx_bid].price <= entry2.asks[idx_ask].price:
            break


if __name__ == '__main__':
    tradeBook = []
    event_loop = get_event_loop()
    dataIO = DataIO(event_loop)
    while True:
        output = event_loop.run_until_complete(dataIO.get_next_entries())
        arbitrage(tradeBook, dataIO, output[0], output[1])
        arbitrage(tradeBook, dataIO, output[1], output[0])
