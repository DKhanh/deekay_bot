from __future__ import absolute_import, print_function
import tweepy
from pprint import pprint

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#tweets = api.user_timeline(screen_name = "GainzyBot",count=400, tweet_mode ="extended")
#pprint(vars(tweets[0])['full_text'])
#print("")
#print("")
#
#first_split = str(vars(tweets[0])['full_text']).split('\n')
#coin = first_split[0].split(' ')[0]
#if ((coin != "$BTC") & (coin != '$ETH')):
#    coin = first_split[0]
#
#for j in range (0, len(first_split)):
#    second_split = first_split[j].split(': ')
#    if (len(second_split) > 1):
#        if (second_split[0] == 'Symbol'):
#            symbol = second_split[1]
#        elif (second_split[0] == 'Signal'):
#            signal = second_split[1]
#        elif (second_split[0] == 'Price'):
#            price = float(second_split[1])
#        elif (second_split[0] == 'Previous Balance'):
#            pre_balance = float(second_split[1])
#            cur_balance = float(first_split[j-1].split(': ')[1])
#        
#
#print(coin)
#print(symbol)
#print(signal)
#print(price)
#print(cur_balance)
#print(pre_balance)
#
#result = {'coin': coin, 'symbol': symbol, 'signal': signal,
#          'price': price, 'cur_balance': cur_balance, 'pre_balance': pre_balance}
#
#print("")
#print(result)

#pprint(vars(tweets[0])['full_text'])
#first_split = tweet_text[0].split(': ')
#print(first_split)
#for i in range (0, len(text1)):
#  print(text1[i])
#pprint(vars(tweets[1])['full_text'])


#for tweet in tweets:
#  pprint(vars(tweet)['full_text'])
#  print(" ")



#@gainzybot => 1171769235829415939
#@dkhanh1702 => 1264577597486198785
class MyStreamListener(tweepy.StreamListener):
    def parse_bot_data(self):
        coin = 'None'
        symbol = 'None'
        signal = 'None'
        price = 0
        cur_balance = 0
        pre_balance = 0 
        tweets = api.user_timeline(screen_name = "gainzybot",count=400, tweet_mode ="extended")

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
    
    def on_status(self, status):
        result = self.parse_bot_data()
        print(result)
        print("")
        #pprint(vars(tweets[2])['full_text'])
        #pprint(vars(tweets[3])['full_text'])


tweets = api.user_timeline(screen_name = "GainzyBot",count=400, tweet_mode ="extended")
pprint(vars(tweets[0])['full_text'])
print("")

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(follow=["1171769235829415939"]) #GainzyBot
