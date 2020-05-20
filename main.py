#! /usr/bin/python
import sys
from datetime import datetime
import calendar
import market_data as md
import market_analysis as ma

# [1]: interval
# [2]: limit
# [3]: bullish/bearish
def main(argv):
    if (len(argv) < 4):
        return 0

    interval = int(argv[1])
    limit = int(argv[2])
    trend = str(argv[3])

    if ((interval > 0 & interval <  720) |
        (limit > 0 & limit < 10000) |
        ((trend == "bullish") | (trend == "bearish"))):
        market_data = md.market_data_query_kline(interval, limit)
        engulfing = ma.market_analysis_find_engulfing_structure(market_data, trend)

        for i in range(0, len(engulfing)):
            print(datetime.fromtimestamp(market_data["result"][engulfing[i]]["open_time"]))


    return 0

if __name__ == "__main__":
    main(sys.argv)
