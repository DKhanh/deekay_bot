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


class twitter_polling_thread(threading.Thread):
    def __init__(self, thread_id, twitter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.twitter = twitter

    def run(self):
        try:
            self.twitter.twitter_thread_status = 1
            self.twitter.establish_connection()
        finally:
            self.twitter.twitter_thread_status = 0
            logging.error("ERROR!!! Exiting thread - " + str(self.thread_id))
            
class trade_polling_thread(threading.Thread):
    def __init__(self, thread_id, twitter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.twitter = twitter
        
    def run(self):
        while (self.twitter.twitter_thread_status == 1):
            time.sleep(5)
            while (self.twitter.myStreamListener.bybit.new_order_is_triggered == 0):
                time.sleep(5)
                if (self.twitter.myStreamListener.bybit.placing_stop_and_take_order('BTCUSD') == 0):
                    self.twitter.myStreamListener.bybit.new_order_is_triggered = 1
                    
def access_twitter_bot():
    thread_id = 0
    twitter = twitter_api()
    while (thread_id <= 100):
        logging.info("Starting thread - " + str(thread_id))
        twitter_thread = twitter_polling_thread(thread_id, twitter)
        trade_thread = trade_polling_thread(thread_id, twitter)
        twitter_thread.start()
        time.sleep(5)
        trade_thread.start()
        twitter_thread.join()
        trade_thread.join()
        thread_id = thread_id + 1
        time.sleep(5)
        logging.info("Create next thread - " + str(thread_id))
            
    return False

# [1]: interval
# [2]: limit
# [3]: bullish/bearish
def main(argv):
    if (len(argv) < 3):
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