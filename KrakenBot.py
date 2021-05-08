import krakenex
import pprint
import time
from ObvCalculator import ObvCalculator

kraken = krakenex.API()
kraken.load_key('kraken.key')
obv = ObvCalculator()

# KRAKEN_DATA_LABELS
#   a: "Ask",
#   b: "Bid",
#   c: "Last Trade Closed",
#   v: "Volume",
#   l: "Low",
#   h: "High",
#   o: "Today Opening Price"

# you are not allow to buy less than that
# current price for minimum around 9GBP
minimumBtcVolume = 0.0002
cryptoCode = "BTCGBP"

def placeOrder(type):
    print(kraken.query_private('AddOrder', {
    "pair": cryptoCode, 
    "volume": minimumBtcVolume,
    "type": type, 
    "ordertype": "market", 
    "leverage": "none",
    "starttm": "0",
    "expiretm": "+86400"
    }))

def getLastTrade():
    trades = kraken.query_private('TradesHistory', {"ofs": "0"})["result"]["trades"]
    return trades[list(trades)[0]]

def getCurrentMargin():
    """
    Returns the percentage of increase/decrease in price since the last order.
    If the last order was sell so there is no current coin in our possesion then 
    it returns 0.
    ex. if we bought at 10 and now price is 0 this will return -10
    """
    lastTrade = getLastTrade()
    isInvested = lastTrade["type"] == "buy"
    if isInvested:
        tickerResult = kraken.query_public("Ticker", {"pair": cryptoCode})["result"]
        currentBtcPrice = tickerResult[list(tickerResult)[0]]["c"][0]
        lastTradePrice = lastTrade["price"]
        return  ((float(currentBtcPrice) - float(lastTradePrice)) / float(lastTradePrice)) * 100
    else:
        return 0

tickers = []

def getBitcoinTicker():
    return kraken.query_public("Ticker", {"pair": cryptoCode})["result"]["XXBTZGBP"]

def serializeTickers():
    openValue = []
    highValue = []
    lowValue = []
    closeValue = []
    volumeValue = []

    for ticker in tickers:
        openValue.append(float(ticker["o"]))
        highValue.append(float(ticker["h"][0]))
        lowValue.append(float(ticker["l"][1]))
        closeValue.append(float(ticker["c"][0]))
        volumeValue.append(float(ticker["v"][0]))

    return {
        "open": openValue,
        "high": highValue,
        "low": lowValue,
        "close": closeValue,
        "volume": volumeValue
    }


while True:
    currentTicker = getBitcoinTicker()
    tickers.append(currentTicker)
    if len(tickers) > 10:
        tickers.pop(0)

    pprint.pprint(obv.currentObv(serializeTickers()))
    time.sleep(10)
