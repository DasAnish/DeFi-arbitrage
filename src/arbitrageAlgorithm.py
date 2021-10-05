from data import ArbitrageEntry, PriceVolume


def arbitrage(tradebook, dataIO, entry1, entry2, backtesting=False):
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
            if not backtesting:
                dataIO.send_order(order)
            else:
                tradebook.append(order)
                print(order)
            entry1.bids[idx_bid].volume -= volume
            entry2.asks[idx_ask].volume -= volume
            if entry1.bids[idx_bid].volume == 0:
                idx_bid += 1
            if entry2.asks[idx_ask].volume == 0:
                idx_ask += 1
        # if no more arbitrage opportunities
        elif entry1.bids[idx_bid].price <= entry2.asks[idx_ask].price:
            break
