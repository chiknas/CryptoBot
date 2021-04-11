import krakenex
import pprint
import json

kraken = krakenex.API()
kraken.load_key('kraken.key')

# you are not allow to buy less than that
# current price for minimum around 9GBP
minimumBtcVolume = 0.0002

def placeOrder(type):
    print(kraken.query_private('AddOrder', {
    "pair": "XBTGBP", 
    "volume": minimumBtcVolume,
    "type": type, 
    "ordertype": "market", 
    "leverage": "none",
    "starttm": "0",
    "expiretm": "+86400"
    }))

def getLastTrade():
    totalOrders = kraken.query_private('ClosedOrders', {"ofs": "0", "closetime": "close"})["result"]["count"]
    trades = kraken.query_private('ClosedOrders', {"ofs": totalOrders - 1, "closetime": "close"})["result"]["closed"]
    return trades[list(trades)[0]]

    
    
pprint.pprint(getLastTrade())
