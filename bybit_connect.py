import requests
import bybit
from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from BybitAuthenticator import APIKeyAuthenticator
from bravado.swagger_model import load_file

import json

from config import bybit_api_key, bybit_api_secret, bybit_host, bybit_pos_percent
import market_data

#
# # # Get server time
# print(client.Common.Common_get().result()[0])
# #
# # # Get Symbol lists
# print(client.Symbol.Symbol_get().result()[0]["result"][0])
# #
# # # Change account user leverage
# print(client.Positions.Positions_saveLeverage(symbol="BTCUSD", leverage="14").result())
# #
# # # Query account positions
# print(client.Positions.Positions_myPosition().result())
# #
# # #Place an Active Order
# print(client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Limit",qty=1,price=8300,time_in_force="GoodTillCancel").result())
# #
# # #Get Active Order
# print(client.Order.Order_getOrders().result())
# #
# # #Cancel Active Order
# print(client.Order.Order_cancel(order_id="baaa9182-86e1-42aa-8420-da6428346b30").result())
# #
# # # Place Conditional Order
# print(client.Conditional.Conditional_new(order_type="Limit",side="Buy",symbol="BTCUSD",qty=1,price=8100,base_price=8300,stop_px=8150,time_in_force="GoodTillCancel").result())
# #
# # #Get Conditional Order
# print(client.Conditional.Conditional_getOrders().result())
# #
# # #Cancel conditional order
# print(client.Conditional.Conditional_cancel(stop_order_id="53c8e250-252b-47f7-a768-5f5456b64e17").result())
# #
# # #changeMargin
# print(client.Positions.Positions_changeMargin(symbol="BTCUSD", margin="10").result())
# #
# # #Set Trading-Stop
# print(client.Positions.Positions_tradingStop(symbol="BTCUSD",stop_loss="8100").result())
# #
# # #Get wallet fund records
# print(client.Wallet.Wallet_getRecords().result())
# #
# # #Get the Last Funding Rate
# print(client.Funding.Funding_myLastFee(symbol="BTCUSD").result())
# #
# # #Get My Last Funding Fee
# # print(client.Funding.Funding_getRate(symbol="BTCUSD").result())
# #
# # #Get Predicted Funding Rate and Funding Fee
# print(client.Funding.Funding_predicted(symbol="BTCUSD").result())
# #
# # #Get the trade records of a order
# print(client.Execution.Execution_getTrades(order_id="24d6c1b1-e2aa-4ef0-8d73-55b751710a0c").result())
# #
# # #Get Orderbook
# print(client.Market.Market_orderbook(symbol="BTCUSD").result())
#
# #Latest information for symbol
# print(client.Market.Market_symbolInfo().result())
#
# print(client.LinearOrder.LinearOrder_new(side="Sell",symbol="BTCUSDT",order_type="Limit",qty=0.22,price=10000,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
# print(client.LinearOrder.LinearOrder_cancel(symbol="BTCUSDT", order_id="87d8a4ed-dc9d-41c9-8dac-6e3c51356645").result())

# print(client.LinearOrder.LinearOrder_getOrders(symbol="BTCUSDT").result())

# print(client.LinearOrder.LinearOrder_query(symbol="BTCUSDT", order_id="87d8a4ed-dc9d-41c9-8dac-6e3c51356645").result())
# print(client.LinearOrder.LinearOrder_cancelAll(symbol="BTCUSDT").result())
#
# print(client.LinearConditional.LinearConditional_new(stop_px=9989, side="Sell",symbol="BTCUSDT",order_type="Limit",qty=0.22,base_price=9900, price=10000,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
# print(client.LinearConditional.LinearConditional_cancel(symbol="BTCUSDT", stop_order_id="52095ff7-b080-498e-b3a4-8b3e76c42f5e").result())
# print(client.LinearConditional.LinearConditional_cancelAll(symbol="BTCUSDT").result())
# print(client.LinearConditional.LinearConditional_getOrders(symbol="BTCUSDT").result())
# print(client.LinearConditional.LinearConditional_query(symbol="BTCUSDT",stop_order_id="eed0915f-d2e5-4e7d-9908-1c73d792c659").result())
# print(client.LinearPositions.LinearPositions_setAutoAddMargin(symbol="BTCUSDT", side="Sell", auto_add_margin=False).result())
# print(client.LinearPositions.LinearPositions_switchIsolated(symbol="BTCUSDT",is_isolated=True, buy_leverage=1, sell_leverage=1).result())
# print(client.LinearPositions.LinearPositions_saveLeverage(symbol="BTCUSDT", buy_leverage=10, sell_leverage=10).result())
# print(client.LinearPositions.LinearPositions_myPosition(symbol="BTCUSDT").result())
# print(client.LinearPositions.LinearPositions_tradingStop(symbol="BTCUSDT", side="Buy", take_profit=10).result())
# print(client.LinearPositions.LinearPositions_changeMargin(symbol="BTCUSDT", side="Buy", margin=0.01).result())
# print(client.LinearExecution.LinearExecution_getTrades(symbol="BTCUSDT").result())
# print(client.LinearPositions.LinearPositions_closePnlRecords(symbol="BTCUSDT").result())
# print(client.LinearFunding.LinearFunding_myLastFee(symbol="BTCUSDT").result())
# print(client.LinearFunding.LinearFunding_prevRate(symbol="BTCUSDT").result())
# print(client.LinearFunding.LinearFunding_predicted(symbol="BTCUSDT").result())
# print(client.LinearKline.LinearKline_get(symbol="BTCUSDT", interval="m", limit=10, **{'from':1}).result())
# print(client.LinearKline.LinearKline_markPrice(symbol="BTCUSDT", interval="m", limit=10, **{'from':1}).result())
#

class bybit_api:
    def __init__(self, api_key, api_secret):
        self.host = bybit_host

        self.api_key = api_key
        self.api_secret = api_secret

        self.spec_uri = self.host + "/doc/swagger.txt"

        self.config = {
            # Don't use models (Python classes) instead of dicts for #/definitions/{models}
            'use_models': False,
            # bravado has some issues with nullable fields
            'validate_responses': False,
            # Returns response in 2-tuple of (body, response); if False, will only return body
            'also_return_response': True,
            "host": self.host
        }

        if api_key and api_secret:
            self.request_client = RequestsClient()
            self.request_client.authenticator = APIKeyAuthenticator(self.host, self.api_key, self.api_secret)

            self.client = SwaggerClient.from_url(self.spec_uri, config=self.config, http_client=self.request_client)
        else:
            self.client = SwaggerClient.from_url(self.spec_uri, config=self.config)

        # self.client  = bybit.bybit(test=True, api_key=bybit_api_key, api_secret=bybit_secret_key)

    def get_server_time(self):
        # Get server time
        return self.client.Common.Common_get().result()[0]

    def get_symbol_lists(self):
        # Get Symbol lists
        print(self.client.Symbol.Symbol_get().result()[0]["result"][0])

    def set_account_leverage(self, symbol, leverage):
        # Change account user leverage
        print("Change account user leverage: symbol[" + str(symbol) + "] - leverage = " + str(leverage))
        print(self.client.Positions.Positions_saveLeverage(symbol=symbol, leverage=leverage).result())
        return (symbol, leverage)

    def get_account_position(self):
        # Query account positions
        return self.client.Positions.Positions_myPosition().result()

    def get_account_position(self):
        return self.client.Positions.Positions_myPosition().result()

    def get_active_order(self):
        return self.client.Order.Order_getOrders().result()

    def cancel_active_order(self, order_id):
        return self.client.Order.Order_cancel(order_id=order_id).result()

    def get_orderbook(self, symbol):
        return self.client.Market.Market_orderbook(symbol=symbol).result()

    def get_latest_information(self):
        return self.client.Market.Market_symbolInfo().result()

    def set_margin(self, symbol, margin):
        return self.client.Positions.Positions_changeMargin(symbol=symbol, margin=margin).result()

    def set_trading_stop(self, symbol, stop_loss):
        #print(client.Positions.Positions_tradingStop(symbol="BTCUSD",stop_loss="8100").result())
        return self.client.Positions.Positions_tradingStop(symbol=symbol,stop_loss=stop_loss).result()
        
    def set_active_order(self, side, symbol, type, qty, price):
        # print(client.Order.Order_new(side="Buy",symbol="BTCUSD",order_type="Limit",qty=1,price=8300,time_in_force="GoodTillCancel").result())
        return self.client.Order.Order_new(side=side,symbol=symbol,order_type=type,qty=qty,price=price,time_in_force="GoodTillCancel").result()[0]['ret_msg']
        
    def get_max_qty(self, price):
        self.cur_balance = round(float(self.client.Wallet.Wallet_getRecords().result()[0]['result']['data'][0]['wallet_balance']), 5)
        self.cur_balance = self.cur_balance*float(0.98)
        self.cur_leverage = float(self.client.Positions.Positions_myPosition().result()[0]['result'][0]['effective_leverage'])
        tmp_price = float(price)
        return round((round(float(self.cur_balance*tmp_price))-1)*self.cur_leverage)
        
    def get_needed_qty(self, price, percent):
        if (percent >= 1) & (percent <= 100):
            return round(float((self.get_max_qty(price)*percent)/100))
        else:
            return round(float((self.get_max_qty(price)*90)/100))
        
    def get_current_position_info(self):
        cur_qty = 0
        tmp_qty = self.client.Positions.Positions_myPosition().result()[0]['result'][0]['size']
        if (tmp_qty != 'None'):
            cur_qty = round(float(tmp_qty))

        # if not in any position, side = None
        cur_side = self.client.Positions.Positions_myPosition().result()[0]['result'][0]['side']
        return (cur_side, cur_qty)
          
    def place_active_order(self, side, symbol, price):
        self.cur_qty = self.get_max_qty(price)
        if (self.set_active_order(side, symbol, 'Limit', self.cur_qty, price) == 'ok'):
            return 'ok'
        else:
            return 'not_ok'
        
    def place_active_order_immediately(self, side, symbol, percent):
        market_price = market_data.market_data_get_current_price()
        if (side == 'Buy'):
            price = str(float(market_price[0])+10)
            tmp_side = 'Sell'
            tmp_price = str(float(market_price[1])-10)
        else: #(side == 'Sell')
            price = str(float(market_price[1])-10)
            tmp_side = 'Buy'
            tmp_price = str(float(market_price[1])+10)
        
        (pos_side, pos_qty) = self.get_current_position_info()
        if ((pos_side != 'None') & (pos_side !=  side)):
            self.set_active_order(side, symbol, 'Limit', pos_qty, price)
        elif ((pos_side != 'None') & (pos_side ==  side)):
            self.set_active_order(tmp_side, symbol, 'Limit', pos_qty, tmp_price)
            
        #self.cur_qty = self.get_max_qty(price)
        self.cur_qty = self.get_needed_qty(price, percent)
        if (self.set_active_order(side, symbol, 'Limit', self.cur_qty, price) == 'ok'):
            (pos_side, pos_qty) = self.get_current_position_info()
            return (pos_side, pos_qty)
        else:
            return ('None', 0)
            
        
    def close_active_order_immediately(self, side, symbol, qty):
        market_price = market_data.market_data_get_current_price()
        if (side == 'Buy'):
            price = str(float(market_price[0])+10)
        else: #(side == 'Sell')
            price = str(float(market_price[1])-10)
            
        # self.cur_qty = self.get_max_qty(price)
        # self.cur_qty = self.get_needed_qty(price, 25)
        if (self.set_active_order(side, symbol, 'Limit', qty, price) == 'ok'):
            return (price, qty)
        else:
            return 'not_ok'

    def test_func(self):
      return self.client.Positions.Positions_myPosition().result()[0]['result'][0]['size']
        
        
#bybit_obj = bybit_api(bybit_api_key, bybit_api_secret)
#print(bybit_obj.get_server_time())
# bybit_obj.set_account_leverage('BTCUSD', '1')
# bybit_obj.get_orderbook('BTCUSD')
#print(bybit_obj.place_active_order_immediately('Sell', 'BTCUSD'))
#bybit_obj.set_trading_stop('BTCUSD', '9000')
#bybit_obj.set_active_order('Sell', 'BTCUSD', 'Limit', '1', '9525')
#bybit_obj.set_active_order('Sell', 'BTCUSD', 'Limit', '2', '9526')
#bybit_obj.set_active_order('Buy', 'BTCUSD', 'Limit', '3', '9506')
#print(bybit_obj.get_needed_qty('9600', 100))
#bybit_obj.set_account_leverage('BTCUSD', '3')
#print((bybit_obj.test_func()))


