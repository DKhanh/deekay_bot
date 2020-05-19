
def market_analysis_find_engulfing_structure(market_data, trend = "bullish"):
    data = market_data["result"]
    # interval = market_data["interval"]
    limit = market_data["limit"]
    return_data = []
    peak_data = []

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

        if (len(peak_data) > 0):
            if ( ((trend == "bullish") & (data[i]["low"] < peak_data[len(peak_data) - 1])) |
                 ((trend == "bearish") & (data[i]["high"] > peak_data[len(peak_data) - 1])) ):
                peak_data.pop(len(peak_data)-1)
                return_data.pop(len(return_data)-1)

        if (trend == "bullish"):
            if ((cur_side == "Sell") & (next_side == "Buy") & (next_candle - cur_candle > 50)):
                return_data.append(i)
                peak_data.append(data[i]["low"])
            elif ((cur_side == "Sell") & (next_side == "Buy") & (next_next_side == "Buy") & (next_candle > cur_candle)):
                if ((cur_candle*100)/(next_candle+next_next_candle) < 25):
                    return_data.append(i)
                    peak_data.append(data[i]["low"])

        elif (trend == "bearish"):            
            if ((cur_side == "Buy") & (next_side == "Sell") & (next_candle - cur_candle > 50)):
                return_data.append(i)
                peak_data.append(data[i]["high"])
            elif ((cur_side == "Buy") & (next_side == "Sell") & (next_next_side == "Sell") & (next_candle > cur_candle)):
                if ((cur_candle*100)/(next_candle+next_next_candle) < 25):
                    return_data.append(i)
                    peak_data.append(data[i]["high"])

    return return_data