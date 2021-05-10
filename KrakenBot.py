import krakenex
import pprint
import time
from datetime import datetime
from ObvStrategy import ObvStrategy

# you are not allow to buy less than that
# current price for minimum around 9GBP
minimumBtcVolume = 0.0002
cryptoCode = "BTCGBP"
# how many periods to look at for the implemented strategy. 
# each period is 1hr.
periods = 6

# KRAKEN_DATA_LABELS
#   a: "Ask",
#   b: "Bid",
#   c: "Last Trade Closed",
#   v: "Volume",
#   l: "Low",
#   h: "High",
#   o: "Today Opening Price"

kraken = krakenex.API()
kraken.load_key('kraken.key')
obv = ObvStrategy()

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

def getCurrentTime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")

def printLineToFile(line):
    myFile = open("test_run.txt", "a")
    myFile.write(line + "\n")
    myFile.close()


while True:
    currentTicker = getBitcoinTicker()
    tickers.append(currentTicker)
    if len(tickers) > 360 * periods:
        tickers.pop(0)
        tradeSignal = obv.whatShouldIDo(serializeTickers())
        if tradeSignal == 1:
            printLineToFile("BUY. time is: " + getCurrentTime())
        elif tradeSignal == -1:
            printLineToFile("SELL. time is: " + getCurrentTime())

    time.sleep(10)
