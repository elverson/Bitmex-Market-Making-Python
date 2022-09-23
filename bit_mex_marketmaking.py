import bitmex
import requests
import json
import datetime
import time

bitmex_api_key_test = '' 
bitmex_api_secret_test = ''
client = bitmex.bitmex(api_key=bitmex_api_key_test, api_secret=bitmex_api_secret_test)

symbol = 'XBTUSD'
leverage = 1
orderqty = 100

result = client.Quote.Quote_get(symbol=symbol, reverse=True, count=1).result()
print(result[0][0]['bidPrice'])
print(result[0][0]['askPrice'])    
print("")
print("")  
buy_make = int(result[0][0]['bidPrice'] * 0.995)
sell_make = int(result[0][0]['askPrice'] * 1.005)   
order = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=buy_make).result()
order2 = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=sell_make, side='Sell').result()   
count = 3000
count2 = 4000
while True:  
    result = client.Quote.Quote_get(symbol=symbol, reverse=True, count=1).result()
    print('bid:',result[0][0]['bidPrice'])
    print('ask:',result[0][0]['askPrice'])    
    buy_make2 = int(result[0][0]['bidPrice'] * 0.995)
    sell_make2 = int(result[0][0]['askPrice'] * 1.005)      
    buy_make = buy_make2
    #order = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=buy_make).result()
    countmm = 'mm1' + str(count)
    order = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=buy_make, side='Buy',clOrdID = (countmm)).result()
    sell_make = sell_make2         
    #order2 = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=sell_make, side='Sell').result() 
    countmm2 = 'mm2' + str(count2)
    order2 = client.Order.Order_new(symbol=symbol, orderQty=orderqty, price=sell_make, side='Sell',clOrdID = (countmm2)).result()       
              
    positions = client.Position.Position_get(filter=json.dumps({"symbol": symbol})).result()[0][0]
    processed_position = {}
    timestamp_minute = str(positions["timestamp"]).split(':')[0] + ":" + \
                        str(positions["timestamp"]).split(':')[1] + ":00"
    processed_position["symbol"] = positions["symbol"]
    processed_position["timestamp"] = timestamp_minute
    processed_position["isOpen"] = positions["isOpen"]
    processed_position["currentQty"] = positions["currentQty"]
    processed_position["leverage"] = positions["leverage"]
    processed_position["liquidationPrice"] = positions["liquidationPrice"]
    print('current positions:',processed_position["currentQty"])
    client.Order.Order_cancel(clOrdID=(countmm)).result()
    client.Order.Order_cancel(clOrdID=(countmm2)).result()
    client.Order.Order_cancel()
    print('price_buy:', order[0]['price'])
    print('price_sell:', order2[0]['price'])
    time.sleep(10)
    print("")
    print("") 
    count = count + 1
    count2 = count2 + 1
