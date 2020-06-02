#! /usr/bin/python3
import tweepy
from config import consumer_key, consumer_secret, access_token, access_token_secret, bybit_api_key, bybit_api_secret
from pprint import pprint
import bybit_connect
from bybit_connect import bybit_api

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_token, access_token_secret)
#api = tweepy.API(auth)

screen_name = "gainzybot"
usr_id = "1171769235829415939"

#@gainzybot => 1171769235829415939
#@dkhanh1702 => 1264577597486198785
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        
        self.bybit = bybit_api(bybit_api_key, bybit_api_secret)
        self.cur_price = 'None'
        self.cur_qty = 'None'
        self.cur_side = 'None'
        self.pre_side = 'None'

    def parse_bot_data(self):
        coin = 'None'
        symbol = 'None'
        signal = 'None'
        price = 0
        cur_balance = 0
        pre_balance = 0 
        tweets = self.api.user_timeline(screen_name = screen_name, count=400, tweet_mode ="extended")

        first_split = str(vars(tweets[0])['full_text']).split('\n')
        coin = first_split[0].split(' ')[0]
        if ((coin != "$BTC") & (coin != '$ETH')):
            coin = first_split[0]

        for j in range (0, len(first_split)):
            second_split = first_split[j].split(': ')
            if (len(second_split) > 1):
                if (second_split[0] == 'Symbol'):
                    symbol = second_split[1]
                elif (second_split[0] == 'Signal'):
                    signal = second_split[1]
                elif (second_split[0] == 'Price'):
                    price = float(second_split[1])
                elif (second_split[0] == 'Previous Balance'):
                    pre_balance = float(second_split[1])
                    cur_balance = float(first_split[j-1].split(': ')[1])

        result = {'coin': coin, 'symbol': symbol, 'signal': signal,
                  'price': price, 'cur_balance': cur_balance, 'pre_balance': pre_balance}
        return result
    
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
    
    def on_status(self, status):
        result = self.parse_bot_data()
        print(result)
        print("")
        
        if ( (result['coin'] == '$BTC') & (result['symbol'] == 'XBTUSD') & ((result['signal'] == 'Buy') | (result['signal'] == 'Sell')) & 
        (result['price'] != 0) & (result['cur_balance'] != 0) & (result['pre_balance'] != 0) ):
            if (result['signal'] != self.pre_side):
                self.pre_side = result['signal']
                (self.cur_price, self.cur_qty) = self.bybit.place_active_order_immediately(result['signal'], 'BTCUSD', 25)
                print('current price: ' + str(self.cur_price))
                print('current qty: ' + str(self.cur_qty))


class twitter_api():
    def __init__(self):
        self.myStreamListener = MyStreamListener()
        tweets = self.myStreamListener.api.user_timeline(screen_name = screen_name, count=400, tweet_mode ="extended")
        pprint(vars(tweets[0])['full_text'])
        print("")
        
    def establish_connection(self):
        myStream = tweepy.Stream(auth = self.myStreamListener.api.auth, listener=self.myStreamListener)
        return myStream.filter(follow=[usr_id])
        

#myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#if (myStream.filter(follow=[usr_id]) == False):
    
twitter = twitter_api()
twitter.establish_connection()