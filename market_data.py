import requests
import time
import datetime 
from datetime import datetime
import calendar

orderbook_url = "https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSD"
query_kline_url = "https://api.bybit.com/v2/public/kline/list?symbol=BTCUSD&interval=%d&limit=%d&from=%d"

def market_data_get_1m_open_timestamp():
    timestamp = round(calendar.timegm(time.gmtime()))
    timestamp =  timestamp - (timestamp%60)
    return int(timestamp)-60

def market_data_get_5m_open_timestamp():
    m1_timestamp = market_data_get_1m_open_timestamp()
    m5_timestamp = requests.get(query_kline_url % (5, 1, m1_timestamp-300)).json()["result"][0]["open_time"]
    
    return int(m5_timestamp)

def market_data_get_15m_open_timestamp():
    m1_timestamp = market_data_get_1m_open_timestamp()
    m15_timestamp = requests.get(query_kline_url % (15, 1, m1_timestamp-60*15)).json()["result"][0]["open_time"]
    
    return int(m15_timestamp) 

def market_data_get_open_timestamp(interval):
    timestamp = calendar.timegm(time.gmtime())
    timestamp = int(float(timestamp) - float(timestamp%60))

    timestamp = requests.get(query_kline_url % (interval, 1, timestamp-60*interval)).json()["result"][0]["open_time"]
    return timestamp

# Get market data from current timestamp
def market_data_query_kline(interval, limit):
    total_batch = limit
    start_timestamp = market_data_get_open_timestamp(interval) - interval*total_batch*60

    market_data = {   
                    "interval"  : interval,
                    "limit"     : total_batch,
                    "from"      : start_timestamp,
                    "result"    : []
                  }

    while (total_batch > 0):
        if (total_batch > 200):
            loop = 200
        else:
            loop = total_batch

        start_timestamp = market_data_get_open_timestamp(interval) - interval*total_batch*60
        result = requests.get(query_kline_url % (interval, loop, start_timestamp)).json()["result"]
        
        for i in range (0, loop):
            if (float(result[i]["open"]) > float(result[i]["close"])):
                side = "Sell"
            else:
                side = "Buy"

            tmp_batch = {   "interval"  : float(result[i]["interval"]), 
                            "open_time" : float(result[i]["open_time"]), 
                            "open"      : float(result[i]["open"]), 
                            "high"      : float(result[i]["high"]), 
                            "low"       : float(result[i]["low"]), 
                            "close"     : float(result[i]["close"]), 
                            "volume"    : float(result[i]["volume"]), 
                            "turnover"  : float(result[i]["turnover"]),
                            "side"      : side 
                        }          
            market_data["result"].append(tmp_batch)

        total_batch = total_batch - 200
        
    return market_data
   
def market_data_find_max_volume_in_batches(market_data, side):
    max_volume = market_data[0]["volume"]
    max_idx = 0
    min_volume = market_data[0]["volume"]
    min_idx = 0

    for i in range(0, len(market_data)):
        if (market_data[i]["side"] == side):
            if (market_data[i]["volume"] > max_volume):
                max_volume = market_data[i]["volume"]
                max_idx = i
            
            if (market_data[i]["volume"] < min_volume):
                min_volume = market_data[i]["volume"]
                min_idx = i
        else:
            continue

    return (max_idx, min_idx)

def market_data_get_current_price():
    buy_price = requests.get(orderbook_url).json()["result"][0]["price"]
    sell_price = requests.get(orderbook_url).json()["result"][1]["price"]
    print ("buy order:  " + buy_price)
    print ("sell order: " + sell_price)
