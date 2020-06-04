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
import threading


class trading_thread(threading.Thread):
    def __init__(self, thread_id, twitter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.twitter = twitter

    def run(self):
        try:
            self.twitter.establish_connection()
        finally:
            logging.error("ERROR!!! Exiting thread - " + str(self.thread_id))

def access_twitter_bot():
    thread_id = 0
    twitter = twitter_api()
    while (thread_id <= 100):
        logging.info("Starting thread - " + str(thread_id))
        thread = trading_thread(thread_id, twitter)
        thread.start()
        thread.join()
        thread_id = thread_id + 1
        time.sleep(1)
        logging.info("Create next thread - " + str(thread_id))
            
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
    logging.basicConfig(level=logging.INFO, filename="./log/logfile_" + str(date.today()), filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info("hello")
    main(sys.argv)