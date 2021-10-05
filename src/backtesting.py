from data import *
from csv import reader
from src import *
import matplotlib.pyplot as plt
import numpy as np


def conversion(data1, timestamp, exchange):
    i = 0
    results = BookEntry([], [], '', '')
    results.timestamp = timestamp
    results.exchange_id = exchange
    while i < 10:
        results.bids.append(PriceVolume(data1[i], data1[i+10]))
        i += 1
    i = 20
    while i < 30:
        results.asks.append(PriceVolume(data1[i], data1[i + 10]))
        i += 1
    return results


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
        data1 = conversion(data1, row1[0], row1[1])
        data2 = conversion(data2, row2[0], row2[1])
        arbitrage(tradebook, None, data1, data1, True)
        arbitrage(tradebook, None, data2, data1, True)


def backtesting_main():
    total_profits = 0
    time = []
    profits = []
    for order in read_orders_generator():
        ask = order.ask
        bid = order.bid
        volume = min(ask.volume, bid.volume)
        priceDiff = bid.price - ask.price
        profitCalc = volume * priceDiff
        total_profits += profitCalc
        print(f"bid: {bid.price:.5f} \t ask: {ask.price:.5f} \t volume: {volume:.5f} \t profit: {profitCalc:.5f}")
        time.append(order.timestamp)
        profits.append(total_profits)
    print(total_profits)
    return time, profits


if __name__ == '__main__':
    tradebook = []
    path1 = '../backtest/orderbook_bnc.csv'
    path2 = '../backtest/orderbook_hb.csv'
    backtest(path1, path2, tradebook)
    with open('../data/tradeorder.txt', 'w') as f:
        for item in tradebook:
            f.write("%s\n" % item)
    x,y = backtesting_main()
    plt.plot(x,y)
    plt.fill_between(x,y)
    temp = ([i for i in x[::len(x)//4]] + [x[-1]])
    # temp = [i[-8:] for i in temp]
    plt.xticks(temp)
    plt.yticks(np.arange(0, 26, step=5))
    plt.show()
