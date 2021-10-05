from data import *
from asyncio import gather, get_event_loop, wait

if __name__ == '__main__':
    event_loop = get_event_loop()
    dataIO = DataIO(event_loop)
    while True:
        output = event_loop.run_until_complete(dataIO.get_next_entries())
    # results = event_loop.run_until_complete(dataIO.get_next_entries())
    # print(results)
    # dataIO.close()