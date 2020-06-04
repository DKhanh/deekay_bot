#! /usr/bin/python
import sys
import logging
from datetime import datetime, date
import calendar
import time
import market_data as md
import market_analysis as ma
import twitter_api
from twitter_api import twitter_api

def access_twitter_bot():
    count = 0
    twitter = twitter_api()
    while (count <= 100):
        if (twitter.establish_connection() == False):
            count = count + 1
            #print("There are ERROR on twitter stream!! Trying to reconnect: " + str(count))
            logging.error("There are ERROR on twitter stream!! Trying to reconnect: " + str(count))
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
    
    ma.market_analysis_export_engulfing_structure_from_main(argv)

    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="./log/logfile_" + str(date.today()), filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("hello")
    main(sys.argv)
