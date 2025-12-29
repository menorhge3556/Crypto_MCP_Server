import ccxt
from .errors import ExchangeNotSupportedError


def get_exchange(name: str):
    name = name.lower()

    EXCHANGES = {
    "binance": ccxt.binance,
    "kraken": ccxt.kraken,
    "coinbase": ccxt.coinbase,
}
    
    if name not in EXCHANGES:
        raise ExchangeNotSupportedError(f"Exchange '{name}' is not supported.")
    
    return EXCHANGES[name]()  
