"""
market_data = {   
                "interval",
                "limit",
                "from",
                "result": {   
                    "interval" , 
                    "open_time", 
                    "open", 
                    "high", 
                    "low" , 
                    "close", 
                    "volume", 
                    "turnover",
                    "side" 
                    }
}        
"""

def market_analysis_find_engulfing_structure(market_data, trend = "bullish"):
    data = market_data["result"]
    # interval = market_data["interval"]
    limit = market_data["limit"]
    return_data = []
    peak_data = []
    next_check = 0

    if (trend == "bullish"):
        trend_side = "Buy"
        preverse_side = "Sell"
        peak = "low"
    elif (trend == "bearish"):
        trend_side = "Sell"
        preverse_side = "Buy"
        peak = "high"

    # find bullish engulfing structure
    # small red candle happen then a larger green candle
    # if large green candle is 100%, small red candle would be > 40%
    #   green candle ==> open < close
    #   red candle   ==> open > close 
    for i in range(0, limit-2):
        cur_side = data[i]["side"]
        next_side = data[i+1]["side"]
        next_next_side = data[i+2]["side"]
        cur_candle = abs(data[i]["open"] - data[i]["close"])
        next_candle = abs(data[i+1]["open"] - data[i+1]["close"])
        next_next_candle = abs(data[i+2]["open"] - data[i+2]["close"])

        if (next_check == 1):
            next_check = 0
            continue

        # remove the engulfing structure that no longer available
        # because these struc are invalidated when the price break and go
        #   lower in case of bullish engulfing structure
        #   higher in case or bearish engulfing structure
        if (len(peak_data) > 0):
            if ( ((trend == "bullish") & (data[i]["low"] < peak_data[len(peak_data) - 1])) |
                 ((trend == "bearish") & (data[i]["high"] > peak_data[len(peak_data) - 1])) ):
                peak_data.pop(len(peak_data)-1)
                return_data.pop(len(return_data)-1)

        if ((cur_side == preverse_side) & (next_side == trend_side) & (next_candle > cur_candle)):
            if (((next_candle - cur_candle) > 50) | 
                ((next_next_side == trend_side) & ((cur_candle*100)/(next_candle+next_next_candle) < 25))):
                    return_data.append(i)
                    peak_data.append(data[i][peak])
                    next_check = 1

    return return_data

def market_analysis_find_demand_zone(market_data):
    result = market_data["result"]
    limit = market_data["limit"]
    # start_timestamp = market_data["from"]
    # interval = market_data["interval"]

    

    local_high = 0
    local_low = 0
    higher_high = 0
    # lower_high = 0
    lower_low = 0
    # higher_low = 0

    for i in range (0, limit):
        if (result[i]["high"] > local_high):
            if (result[i]["high"] < higher_high):
                local_high = result[i]["high"]
            else:
                higher_high = result[i]["high"]
        if (result[i]["low"] < local_low):
            if (result[i]["low"] > lower_low):
                local_low = result[i]["low"]
            else:
                lower_low = result[i]["low"]

    return 0

def market_analysis_find_supply_zone(market_data):
    return 0