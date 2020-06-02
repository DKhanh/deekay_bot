#! /usr/bin/python
import sys
from datetime import datetime
import calendar
import time
import market_data as md
import market_analysis as ma
import twitter_api

def access_twitter_bot():
    count = 0
    twitter = twitter_api()
    while (count <= 100):
        if (twitter.establish_connection() == False):
            count = count + 1
            print("There are ERROR on twitter stream!! Trying to reconnect: " + str(count))
            time.sleep(1)
            
    if (count > 100):
        return False

# [1]: interval
# [2]: limit
# [3]: bullish/bearish
def main(argv):
    if (len(argv) < 4):
        md.market_data_get_current_price()
        access_twitter_bot()
        return 0

    interval = int(argv[1])
    limit = int(argv[2])
    trend = str(argv[3])

    if ((interval > 0 & interval <  720) |
        (limit > 0 & limit < 10000) |
        ((trend == "bullish") | (trend == "bearish"))):
        market_data = md.market_data_query_kline(interval, limit)
        engulfing = ma.market_analysis_find_engulfing_structure(market_data, trend)

        # if bearish: 
        #   + entry point: between open and low
        #   + stop loss: above the high
        # if bullish: 
        #   + entry point: between close and high
        #   + stop loss: below the low

        for i in range(0, len(engulfing)):
            print(str(datetime.fromtimestamp(market_data["result"][engulfing[i]]["open_time"]))
            + " - open = " + str(market_data["result"][engulfing[i]]["open"])
            + " - close = " + str(market_data["result"][engulfing[i]]["close"])
            + " - high = " + str(market_data["result"][engulfing[i]]["high"])
            + " - low = " + str(market_data["result"][engulfing[i]]["low"])
            )

    return 0

if __name__ == "__main__":
    main(sys.argv)
