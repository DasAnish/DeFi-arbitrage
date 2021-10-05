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
