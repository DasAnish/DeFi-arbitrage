from data import *
from csv import reader


def backtest_arbitrage(tradebook, entry1, entry2, time):
    idx_bid = 0
    idx_ask = 20
    order = ArbitrageEntry(*([None]*5))
    order.timestamp = time
    # buying entry2 selling entry1
    while (idx_bid < 10) and (idx_ask < 30):
        if entry1[idx_bid] > entry2[idx_ask]:
            volume = min(entry1[idx_bid+10], entry2[idx_ask+10])
            order.bid = PriceVolume(entry1[idx_bid], volume)
            order.ask = PriceVolume(entry2[idx_ask], volume)
            tradebook.append(order)
            entry1[idx_bid+10] -= volume
            entry2[idx_ask+10] -= volume
            if entry1[idx_bid+10] == 0:
                idx_bid += 1
            if entry2[idx_ask+10] == 0:
                idx_ask += 1
        # if no more arbitrage opportunities
        elif entry1[idx_bid] <= entry2[idx_ask]:
            break


def backtest(path1, path2, tradebook):
    f1 = open(path1)
    f2 = open(path2)
    book1 = reader(f1)
    book2 = reader(f2)
    next(book2)
    next(book1)
    for row1, row2 in zip(book1, book2):
        data1 = [float(i) for i in row1[2:]]
        data2 = [float(i) for i in row2[2:]]
        backtest_arbitrage(tradebook, data1, data1, row1[0])
        backtest_arbitrage(tradebook, data2, data1, row1[0])


if __name__ == '__main__':
    tradebook = []
    path1 = '../backtest/orderbook_bnc.csv'
    path2 = '../backtest/orderbook_hb.csv'
    backtest(path1, path2, tradebook)
from data import read_orders_generator


def backtesting_main():
    total_profits = 0
    for order in read_orders_generator():
        ask = order.ask
        bid = order.bid
        volume = min(ask.volume, bid.volume)
        priceDiff = bid.price - ask.price
        profitCalc = volume * priceDiff
        total_profits += profitCalc
        print(f"bid: {bid.price:.5f} \t ask: {ask.price:.5f} \t volume: {volume:.5f} \t profit: {profitCalc:.5f}")

    print(total_profits)
    return total_profits
