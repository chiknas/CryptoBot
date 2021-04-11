import krakenex

kraken = krakenex.API()
kraken.load_key('kraken.key')

minimumBtcVolume = "0.0002"

print(kraken.query_public("Ticker", {"pair": "XBTGBP"}))

print(kraken.query_private('AddOrder', {
    "pair": "XBTGBP", 
    "volume": minimumBtcVolume,
    "type": "buy", 
    "ordertype": "market", 
    "leverage": "none",
    "starttm": "0",
    "expiretm": "+86400"
    }))